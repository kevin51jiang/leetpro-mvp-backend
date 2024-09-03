"""
Conversation-related operations for the LeetPro application.
"""

import dataclasses
from datetime import datetime
import json
import aiofiles
from api.models import Conversation, ConversationOverallAnalysis
from api.utils import generate_uuid
from api.txt2txt import analyze_conversation


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

async def save_conversation(conversation: Conversation) -> str:
    """
    Save a conversation to a file.

    Args:
        conversation (Conversation): The conversation to save.

    Returns:
        str: The generated conversation ID.
    """
    conversation_id = generate_uuid()
    async with aiofiles.open(f"public/analyze/{conversation_id}.json", "w") as f:
        await f.write(
            json.dumps({"conversation": conversation}, cls=EnhancedJSONEncoder)
        )
    return conversation_id


async def get_conversation_analysis(
    conversation_id: str,
) -> ConversationOverallAnalysis | None:
    """
    Retrieve and analyze a saved conversation.

    Args:
        conversation_id (str): The ID of the conversation to analyze.

    Returns:
        ConversationOverallAnalysis: The analysis results for the conversation.
    """
    try:
        async with aiofiles.open(f"public/analyze/{conversation_id}.json", "r") as f:
            data = await f.read()
            json_data = json.loads(data)
    except FileNotFoundError:
        return None

    if not json_data.get("analysis"):
        analysis = await analyze_conversation(json_data["conversation"])

        json_data["analysis"] = analysis.analysis
        json_data["overall_score"] = analysis.overall_score
        json_data["overall_feedback"] = analysis.overall_feedback

        async with aiofiles.open(f"public/analyze/{conversation_id}.json", "wt") as f:
            await f.write(json.dumps(json_data, cls=EnhancedJSONEncoder))

    return ConversationOverallAnalysis(**json_data)
