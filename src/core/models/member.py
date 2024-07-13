# src/models/member.py
from dataclasses import dataclass


@dataclass
class Member:
    email: str
    pgp_key_id: str
    is_pgp_verified: bool
    name: str
