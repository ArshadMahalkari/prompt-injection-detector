from __future__ import annotations
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AttackCategory(str, Enum):
    DIRECT_INJECTION = "direct_injection"
    INDIRECT_INJECTION = "indirect_injection"
    JAILBREAK = "jailbreak"
    OBFUSCATED = "obfuscated"
    NONE = "none"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    NONE = "none"


# ── Observation ──────────────────────────────────────────────────────────────

class PromptInjectionObservation(BaseModel):
    """What the agent sees at each step."""
    task_id: str = Field(..., description="Unique task identifier")
    task_description: str = Field(..., description="What the agent must do")
    system_prompt: Optional[str] = Field(None, description="System prompt being evaluated (if any)")
    user_input: str = Field(..., description="User-supplied input to analyse")
    context: Optional[str] = Field(None, description="Additional context (e.g. document content fed to LLM)")
    step: int = Field(..., description="Current step number within episode")
    max_steps: int = Field(..., description="Maximum steps allowed in episode")
    previous_feedback: Optional[str] = Field(None, description="Feedback from previous step if multi-step")


# ── Action ────────────────────────────────────────────────────────────────────

class PromptInjectionAction(BaseModel):
    """What the agent submits as its analysis."""
    is_injection: bool = Field(..., description="True if agent believes this is a prompt injection attempt")
    attack_category: AttackCategory = Field(
        ..., description="Category of attack detected, or 'none' if clean"
    )
    severity: Severity = Field(
        ..., description="Estimated severity of the attack, or 'none' if clean"
    )
    explanation: str = Field(
        ..., description="Agent's explanation of why this is or isn't an injection"
    )
    malicious_fragment: Optional[str] = Field(
        None, description="The specific fragment the agent identified as malicious"
    )
    recommended_action: str = Field(
        ..., description="What should be done: block, sanitize, allow, or flag-for-review"
    )


# ── Reward ────────────────────────────────────────────────────────────────────

class PromptInjectionReward(BaseModel):
    """Granular reward breakdown so reward is dense, not sparse."""
    detection_score: float = Field(..., ge=0.0, le=0.4, description="Correct is_injection verdict (0–0.4)")
    category_score: float = Field(..., ge=0.0, le=0.2, description="Correct attack category (0–0.2)")
    severity_score: float = Field(..., ge=0.0, le=0.15, description="Correct severity level (0–0.15)")
    fragment_score: float = Field(..., ge=0.0, le=0.15, description="Malicious fragment correctly identified (0–0.15)")
    recommendation_score: float = Field(..., ge=0.0, le=0.1, description="Correct recommended action (0–0.1)")
    total: float = Field(..., ge=0.0, le=1.0, description="Sum of all component scores")

    @classmethod
    def zero(cls) -> "PromptInjectionReward":
        return cls(
            detection_score=0.0,
            category_score=0.0,
            severity_score=0.0,
            fragment_score=0.0,
            recommendation_score=0.0,
            total=0.0,
        )


# ── Episode state (returned by state()) ──────────────────────────────────────

class EpisodeState(BaseModel):
    current_task_id: str
    step: int
    done: bool
    last_reward: Optional[float]
    cumulative_reward: float
    task_ids: List[str]
