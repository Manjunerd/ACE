from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class AgentState(str, Enum):
    READY="READY"; LISTENING="LISTENING"; UNDERSTANDING="UNDERSTANDING"; OBSERVING="OBSERVING"; THINKING="THINKING"; ACTING="ACTING"; WAITING="WAITING"; CONFIRMATION_REQUIRED="CONFIRMATION_REQUIRED"; COMPLETED="COMPLETED"; FAILED="FAILED"; STOPPED="STOPPED"; PAUSED="PAUSED"

@dataclass
class Action:
    name: str
    args: dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentEvent:
    state: AgentState
    message: str
