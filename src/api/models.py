"""
Data models for the LeetPro application.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Message:
    role: str
    content: str
    timestamp: Optional[datetime] = None
    id: Optional[str] = None

@dataclass
class Conversation:
    messages: List[Message]

@dataclass
class AnalysisScore:
    name: str
    human_name: str
    description: str
    score: int
    feedback: str

@dataclass
class ConversationAnalysis:
    business_acumen: Optional[AnalysisScore] = None
    user_centricity: Optional[AnalysisScore] = None
    product_vision: Optional[AnalysisScore] = None
    clarifying_questions: Optional[AnalysisScore] = None
    ability_to_discuss_tradeoffs_and_possible_errors: Optional[AnalysisScore] = None
    passion_and_creativity: Optional[AnalysisScore] = None
    communication: Optional[AnalysisScore] = None
    collaboration: Optional[AnalysisScore] = None

@dataclass
class ConversationOverallAnalysis:
    conversation: Conversation
    analysis: Optional[ConversationAnalysis] = None
    overall_score: Optional[int] = None
    overall_feedback: Optional[str] = None
