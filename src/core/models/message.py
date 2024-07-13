from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from src.core.models.member import Member


class MessageStatus(Enum):
    """
    Enum representing the status of a message.

    Attributes
    ----------
    DRAFT : str
        The message is saved as a draft and has not been sent yet.
    SENT : str
        The message has been sent but not yet read by the recipient.
    READ : str
        The message has been sent and read by the recipient.
    LOCAL_ONLY : str
        The message is saved locally and not synchronized with the server.
    OUTBOX : str
        The message is saved to the outbox, waiting to be sent.
    """

    DRAFT = "Draft"
    SENT = "Sent"
    READ = "Read"
    LOCAL_ONLY = "Local Only"
    OUTBOX = "Outbox"


@dataclass
class Message:
    recipients: List[Member]
    sender: Member
    content: str
    timestamp: datetime
    status: MessageStatus
