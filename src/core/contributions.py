# src/core/contributions.py
import argparse
import json
import os
import re
import subprocess
import tempfile
import uuid
from datetime import datetime
from importlib import metadata
from typing import Any, Dict, List, Optional, Union

import gnupg
from appdirs import user_cache_dir
from dotenv import load_dotenv
from git import GitCommandError, Repo
from github import Github

from src.core.logging import TRACE, logger

# Load environment variables
load_dotenv()

# Initialize GPG
gpg = gnupg.GPG()

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
if not GITHUB_API_KEY:
    logger.error("GITHUB_API_KEY not set in environment variables")


def get_commit_info(commit: Any) -> Dict[str, Union[str, int, bool, float]]:
    """Extract relevant information from a commit object."""
    commit_info: Dict[str, Union[str, int, bool, float]] = {}
    for attr in dir(commit):
        if not attr.startswith("_") and not callable(getattr(commit, attr)):
            value = getattr(commit, attr)
            if isinstance(value, (str, int, bool, float)):
                commit_info[attr] = value
            elif isinstance(value, (list, tuple)):
                commit_info[attr] = str(value)
    return commit_info


def get_repo_url() -> Optional[str]:
    """Get the repository URL from the project metadata."""
    try:
        project_urls = metadata.metadata("mailsocial").get_all("Project-URL", [])
        for url_entry in project_urls:
            key, url = url_entry.split(",", 1)
            if key.strip().lower() == "source":
                return url.strip()
        raise ValueError("Source URL not found in project metadata")
    except Exception as e:
        logger.error(f"Error retrieving repository URL from metadata: {e}")
        return None


def get_repo_path() -> str:
    """Get the path to the local repository."""
    cache_dir = user_cache_dir("mailsocial")
    repo_path = os.path.join(cache_dir, "repo")
    return repo_path


def clone_or_pull_repo(repo_url: str, repo_path: str) -> Repo:
    """Clone the repository if it doesn't exist, or pull if it does."""
    if os.path.exists(repo_path):
        logger.info("Repository already exists. Pulling latest changes...")
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        logger.info("Cloning repository...")
        os.makedirs(os.path.dirname(repo_path), exist_ok=True)
        Repo.clone_from(repo_url, repo_path)
    return Repo(repo_path)


def extract_signature_details(commit_sha: str, repo_path: str) -> Optional[Dict[str, Any]]:
    """Extract the PGP signature details of a commit and convert to JSON."""
    try:
        # Run the git log command with show-signature option
        command = ["git", "log", "--show-signature", "-1", commit_sha]
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Git command failed with error: {result.stderr}")
            return None

        # Parse the output to extract signature details
        output = result.stdout
        logger.debug(f"Git command output:\n{output}")

        commit_info: Dict[str, Any] = {}
        commit_info["commit"] = commit_sha

        # Extract GPG signature information
        signature_match = re.search(
            r"gpg: Signature made (.*)\ngpg:.*using (.*) key ([\w]+)", output
        )
        if signature_match:
            commit_info["signature_date"] = signature_match.group(1).strip()
            commit_info["key_type"] = signature_match.group(2).strip()
            commit_info["key_id"] = signature_match.group(3).strip()
        else:
            logger.error("GPG signature details not found.")
            return None

        # Extract author information
        author_match = re.search(r"Author:\s+(.*)", output)
        if author_match:
            commit_info["author"] = author_match.group(1).strip()

        # Extract all email addresses
        emails = re.findall(r"<([^>]+)>", output)
        commit_info["emails"] = emails

        # Convert the commit info to JSON
        commit_info_json = json.dumps(commit_info, indent=4)
        logger.info(f"Commit Info JSON:\n{commit_info_json}")
        return commit_info
    except Exception as e:
        logger.error(f"Error extracting signature details: {e}")
        return None


def compare_with_keyserver(key_id: str, emails: List[str]) -> bool:
    """Compare the extracted emails with the PGP key on the keyserver."""
    try:
        # Lookup the PGP key on the key server
        key_data = gpg.recv_keys("keyserver.ubuntu.com", key_id)

        # List the keys and extract UIDs
        key = gpg.list_keys(keys=key_id)[0]
        key_emails = []
        for uid in key["uids"]:
            email_match = re.search(r"<([^>]+)>", uid)
            if email_match:
                key_emails.append(email_match.group(1).strip())
        logger.info(f"Emails from key server: {key_emails}")

        # Compare the emails
        emails_match = set(emails) == set(key_emails)
        logger.info(f"Emails match: {emails_match}")
        return emails_match
    except Exception as e:
        logger.error(f"Error comparing with keyserver: {e}")
        return False


def verify_pgp_signature(commit: Any, repo_path: str) -> Optional[str]:
    """Verify the PGP signature of a commit and extract the key ID."""
    try:
        if hasattr(commit, "gpgsig"):
            commit_info = extract_signature_details(commit.hexsha, repo_path)
            if not commit_info:
                return None

            emails_match = compare_with_keyserver(
                commit_info["key_id"], commit_info["emails"]
            )
            if emails_match:
                logger.info(f"Emails match for PGP key ID: {commit_info['key_id']}")
            else:
                logger.warning(
                    f"Emails do not match for PGP key ID: {commit_info['key_id']}"
                )

            return commit_info["key_id"] if emails_match else None
        else:
            logger.info(f"No PGP signature found for commit {commit.hexsha}")
        return None
    except Exception as e:
        logger.error(f"Error verifying PGP signature for commit {commit.hexsha}: {e}")
        return None


def analyze_commits(repo: Repo, repo_path: str) -> Dict[str, Any]:
    """Analyze commits and calculate contribution percentages."""
    identities: Dict[str, Dict[str, Any]] = {}
    outstanding_commits: Dict[str, Dict[str, Any]] = {}
    total_loc = 0
    for commit in repo.iter_commits():
        commit_info = get_commit_info(commit)
        logger.log(TRACE, f"Commit info: {commit_info}")
        key_id = verify_pgp_signature(commit, repo_path)
        if key_id:
            author_email = commit.author.email.lower()
            if author_email not in identities:
                identities[author_email] = {
                    "id": str(uuid.uuid4()),
                    "email": author_email,
                    "name": commit.author.name,
                    "pgp_key_id": key_id,
                    "github_username": None,
                    "verified": True,
                    "contribution_percentage": 0.0,
                    "last_used_timestamp": commit.committed_date,
                }
            # Update the lines of code count
            if commit.parents:
                diff = repo.git.diff(
                    commit.parents[0], commit, "--numstat", "--no-renames"
                ).strip()
                for line in diff.split("\n"):
                    if line:
                        parts = line.split()
                        if len(parts) >= 2 and parts[0].isdigit():
                            loc = int(parts[0])
                            identities[author_email]["contribution_percentage"] += loc
                            total_loc += loc
            else:
                # Handle the initial commit (no parents)
                diff = repo.git.diff_tree(
                    "--numstat", "--no-renames", "--root", commit.hexsha
                ).strip()
                for line in diff.split("\n"):
                    if line:
                        parts = line.split()
                        if len(parts) >= 2 and parts[0].isdigit():
                            loc = int(parts[0])
                            identities[author_email]["contribution_percentage"] += loc
                            total_loc += loc
        else:
            outstanding_commits[commit.hexsha] = commit_info

    # Calculate the contribution percentages
    for identity in identities.values():
        identity["contribution_percentage"] = (
            (identity["contribution_percentage"] / total_loc) * 100
            if total_loc > 0
            else 0
        )

    contributions = {
        "identities": identities,
        "outstanding_commits": outstanding_commits,
    }
    return contributions


def get_final_contributors_list(contributions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Aggregate identities by PGP ID or GitHub username and calculate ranks."""
    aggregated_contributors: Dict[str, Dict[str, Any]] = {}
    for identity in contributions["identities"].values():
        key = identity["pgp_key_id"] or identity["github_username"]
        if not key or not identity["verified"]:
            continue
        if key not in aggregated_contributors:
            aggregated_contributors[key] = {
                "name": identity["name"],
                "emails": set(),
                "contribution_percentage": 0.0,
                "last_used_timestamp": 0,
            }
        aggregated_contributors[key]["emails"].add(identity["email"])
        aggregated_contributors[key]["contribution_percentage"] += identity[
            "contribution_percentage"
        ]
        aggregated_contributors[key]["last_used_timestamp"] = max(
            aggregated_contributors[key]["last_used_timestamp"],
            identity["last_used_timestamp"],
        )

    final_contributors: List[Dict[str, Any]] = []
    for contributor in aggregated_contributors.values():
        final_contributors.append(
            {
                "name": contributor["name"],
                "emails": list(contributor["emails"]),
                "rank": calculate_rank(contributor["contribution_percentage"]),
            }
        )

    return final_contributors


def calculate_rank(percentage: float) -> str:
    if percentage < 1:
        return "Newbie"
    elif percentage < 5:
        return "Amateur"
    elif percentage < 10:
        return "Contributor"
    elif percentage < 25:
        return "Co-Maintainer"
    elif percentage < 50:
        return "Maintainer"
    else:
        return "Lead Maintainer"


def load_contributions(file_path: str) -> Optional[Dict[str, Any]]:
    """Load contributions from a JSON file."""
    try:
        with open(file_path, "r") as file:
            contributions: Dict[str, Any] = json.load(file)
        logger.info(f"Contributions loaded from {file_path}")
        return contributions
    except Exception as e:
        logger.error(f"Error loading contributions from {file_path}: {e}")
        return None


def main() -> None:
    repo_url = get_repo_url()
    if not repo_url:
        logger.error("Repository URL not found")
        return

    repo_path = get_repo_path()
    repo = clone_or_pull_repo(repo_url, repo_path)
    contributions = analyze_commits(repo, repo_path)

    # Save the contributions to a JSON file
    contributions_file = ".contributions.json"
    try:
        with open(contributions_file, "w") as file:
            json.dump(contributions, file, indent=4)
        logger.info(f"Contributions saved to {contributions_file}")
    except Exception as e:
        logger.error(f"Error saving contributions to {contributions_file}: {e}")

    # Print out the final contribution statistics
    for email, identity in contributions["identities"].items():
        logger.info(f"Contributor: {identity['name']} ({email})")
        logger.info(f"PGP Key ID: {identity['pgp_key_id']}")
        logger.info(
            f"Contribution Percentage: {identity['contribution_percentage']:.2f}%"
        )
        logger.info("")

    # Handle outstanding commits
    if contributions["outstanding_commits"]:
        logger.warning("There are outstanding commits with unverified signatures:")
        for commit_sha, commit_info in contributions["outstanding_commits"].items():
            logger.warning(f"Commit {commit_sha}: {commit_info}")

    # Get the final contributors list
    loaded_contributions = load_contributions(contributions_file)
    if loaded_contributions:
        final_contributors = get_final_contributors_list(loaded_contributions)
        logger.info("Final Contributors List:")
        for contributor in final_contributors:
            logger.info(
                f"Name: {contributor['name']}, Emails: {contributor['emails']}, Rank: {contributor['rank']}"
            )


if __name__ == "__main__":
    main()
