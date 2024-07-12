import os
import json
from git import Repo, GitCommandError
from appdirs import user_cache_dir
import argparse
from importlib import metadata
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
if not GITHUB_API_KEY:
    raise ValueError("GITHUB_API_KEY not set in environment variables")

gh = Github(GITHUB_API_KEY)

def get_repo_url():
    """Get the repository URL from the project metadata."""
    try:
        project_urls = metadata.metadata('mailsocial').get_all('Project-URL', [])
        for url_entry in project_urls:
            key, url = url_entry.split(',', 1)
            if key.strip().lower() == 'source':
                return url.strip()
        raise ValueError("Source URL not found in project metadata")
    except Exception as e:
        print(f"Error retrieving repository URL from metadata: {e}")
        return None

def get_repo_path():
    """Get the path to the local repository."""
    cache_dir = user_cache_dir("mailsocial")
    repo_path = os.path.join(cache_dir, "repo")
    return repo_path

def clone_or_pull_repo(repo_url, repo_path):
    """Clone the repository if it doesn't exist, or pull if it does."""
    if os.path.exists(repo_path):
        print("Repository already exists. Pulling latest changes...")
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        print("Cloning repository...")
        os.makedirs(os.path.dirname(repo_path), exist_ok=True)
        Repo.clone_from(repo_url, repo_path)
    return Repo(repo_path)

def get_github_user_data(author_email):
    """Retrieve GitHub user data by email."""
    try:
        users = gh.search_users(f"{author_email} in:email")
        for user in users:
            if user.email and user.email.lower() == author_email.lower():
                return user
        return None
    except Exception as e:
        print(f"Error retrieving GitHub user data for {author_email}: {e}")
        return None

def analyze_commits(repo):
    """Analyze commits and calculate contribution percentages."""
    contributors = {}
    total_loc = 0

    try:
        for commit in repo.iter_commits():
            author_name = commit.author.name
            author_email = commit.author.email

            if not author_email:
                continue

            user = get_github_user_data(author_email)
            if user:
                user_id = str(user.id)
                verified = user.name == author_name and user.email == author_email
            else:
                user_id = author_email  # Fallback to email as user ID
                verified = False

            if user_id not in contributors:
                contributors[user_id] = {"identities": [], "verified": False, "total_contribution_percentage": 0.0}

            if verified and user_id == str(user.id):
                contributors[user_id]["verified"] = True

            identity = next((i for i in contributors[user_id]["identities"] if i["email"] == author_email), None)
            if not identity:
                identity = {"email": author_email, "name": author_name, "email_verified": verified, "contribution_percentage": 0.0}
                contributors[user_id]["identities"].append(identity)

            # Count lines of code changed in Python files
            for file in commit.stats.files:
                if file.endswith('.py'):
                    loc_changed = commit.stats.files[file]['lines']
                    identity["contribution_percentage"] += loc_changed
                    total_loc += loc_changed

        # Calculate percentages
        for user_id, data in contributors.items():
            user_total = sum(i["contribution_percentage"] for i in data["identities"])
            data["total_contribution_percentage"] = (user_total / total_loc) * 100
            for identity in data["identities"]:
                identity["contribution_percentage"] = (identity["contribution_percentage"] / total_loc) * 100

    except GitCommandError as e:
        print(f"An error occurred while analyzing commits: {e}")
        return None

    return contributors

def generate_credits_file(contributors, output_path):
    """Generate the .credits.json file."""
    with open(output_path, 'w') as f:
        json.dump(contributors, f, indent=2)
    print(f"Credits file generated: {output_path}")

def main(output_path):
    repo_url = get_repo_url()
    if not repo_url:
        print("Failed to retrieve repository URL. Exiting.")
        return

    repo_path = get_repo_path()
    repo = clone_or_pull_repo(repo_url, repo_path)
    contributors = analyze_commits(repo)
    
    if contributors:
        generate_credits_file(contributors, output_path)
    else:
        print("Failed to generate credits file due to an error in commit analysis.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate credits file from Git repository")
    parser.add_argument("--output", default=".credits.json", help="Output path for the credits file (default: .credits.json)")
    args = parser.parse_args()

    main(args.output)
