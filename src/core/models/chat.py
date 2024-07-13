# src/models/chat.py
from dataclasses import dataclass
from typing import List
from src.core.models.message import Message
from src.core.models.member import Member

@dataclass
class Chat:
    title: str
    members: List[Member]
    messages: List[Message]
