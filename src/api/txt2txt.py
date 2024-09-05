from copy import deepcopy
import os
from typing import Dict, List
from openai import AsyncOpenAI
from dotenv import load_dotenv

from api.models import (
    AnalysisScore,
    Conversation,
    ConversationAnalysis,
    ConversationOverallAnalysis,
)

load_dotenv()

openai_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://tryleetpro.com",
        "X-Title": "LeetPro - Practice Interviews Online",
    },
)


async def get_txt2txt_completion(messages: List[Dict[str, str]], model: str = "openai/gpt-4o-2024-08-06") -> str:
    chat_completion = await openai_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    print("OpenAI completion done")

    try:
        res = chat_completion.choices[0].message.content
        return res
    except Exception as e:
        print("Error getting completion", e)
        return ""
    




default_conversation_overall_analysis = ConversationOverallAnalysis(
    conversation=Conversation(
        messages=[],
    ),
    analysis=ConversationAnalysis(
        business_acumen=AnalysisScore(
            name="Business Acumen",
            description="Big tech PMs' major responsibility is growing a product. To do that intelligently, you have to understand how your product fits into larger business goals. Interviewers want to see your product design align with the company's mission - otherwise, your design isn't sustainable.",
            score=0,
            feedback="",
            human_name="Business Acumen",
        ),
        user_centricity=AnalysisScore(
            name="User-Centricity",
            description="One anchor point for good PM work is the company's business goals. The other is the end-users. Interviewers want to see you orient yourself to these two poles throughout - but at the end of the day, you can't lose by focusing on the customer.",
            score=0,
            feedback="",
            human_name="User-Centricity",
        ),
        product_vision=AnalysisScore(
            name="Product Vision",
            description="It's not enough to design a good product - good PMs play the long game because competitors move fast, and the landscape will always change. Interviewers look for you to articulate your vision for the product one, five, maybe even ten years into the future.",
            score=0,
            feedback="",
            human_name="Product Vision",
        ),
        clarifying_questions=AnalysisScore(
            name="Clarifying Questions",
            description="Designing a product is a problem-solving exercise. What problem are you trying to solve? To get at the root, you have to ask good questions.",
            score=0,
            feedback="",
            human_name="Clarifying Questions",
        ),
        ability_to_discuss_tradeoffs_and_possible_errors=AnalysisScore(
            name="Ability to Discuss Tradeoffs and Possible Errors",
            description="There will always be many possible opportunities to chase. The best way to arrive at a plan logically is to think through the tradeoffs of your decision -- and constantly check yourself for possible assumptions and errors. This will earn you big points in traditionally creative product design interviews.",
            score=0,
            feedback="",
            human_name="Ability to Discuss Tradeoffs and Possible Errors",
        ),
        passion_and_creativity=AnalysisScore(
            name="Passion and Creativity",
            description="Product questions are some of your best opportunities to show your culture fit. How? Get excited about the product! Interviewers want to see your passion for their company, and how you'll use that passion to fuel your creativity.",
            score=0,
            feedback="",
            human_name="Passion and Creativity",
        ),
        communication=AnalysisScore(
            name="Communication",
            description="Communication is assessed in every interview.",
            score=0,
            feedback="",
            human_name="Communication",
        ),
        collaboration=AnalysisScore(
            name="Collaboration",
            description="Product design interviews are a great opportunity to collaborate as your interviewer has the context that you need in order to make good decision. Some interviews can turn into a collaborative problem-solving exercise; be sure to lead, ask good questions, check assumptions, and check-in, and you can't go wrong.",
            score=0,
            feedback="",
            human_name="Collaboration",
        ),
    ),
    overall_score=0,
    overall_feedback="",
)

RUBRICS: dict[str, dict[str, str]] = {
    "business_acumen": {
        "human_name": "Business Acumen",
        "criteria": """
Very Weak or Missing: Failed to show an understanding of the context of the business.
Weak: Struggled to tie back to business goals or company mission.
Neutral: Discussion around business goals was unclear or flawed.
Strong: Clearly discussed business goals, positioning, industry trends.
Very Strong: Nuanced understanding of the landscape, insightful arguments, logical assumptions.
""",
        "description": "Big tech PMs' major responsibility is growing a product. To do that intelligently, you have to understand how your product fits into larger business goals. Interviewers want to see your product design align with the company's mission - otherwise, your design isn't sustainable.",
    },
    "user_centricity": {
        "human_name": "User-Centricity",
        "criteria": """
Very Weak or Missing: Failed to consider the end-user.
Weak: Struggled to anchor answer on end-users despite guidance.
Neutral: Attempted user-centric design, but missed key points.
Strong: Discussed pain points and opportunities, prioritized appropriately.
Very Strong: Analyzed users accurately and completely, prioritized effectively, and tied back to users throughout.
""",
        "description": "One anchor point for good PM work is the company's business goals. The other is the end-users. Interviewers want to see you orient yourself to these two poles throughout - but at the end of the day, you can't lose by focusing on the customer.",
    },
    "product_vision": {
        "human_name": "Product Vision",
        "criteria": """
Very Weak or Missing: Failed to discuss the future of the product.
Weak: Struggled to articulate a vision for the future.
Neutral: Laid out a possible future with some minor errors.
Strong: Displayed thoughtfulness and intuition in articulating the product vision.
Very Strong: Exemplary product intuition; strong perspective, compelling arguments backed by data and strongly tied to UX.
""",
        "description": "It's not enough to design a good product - good PMs play the long game because competitors move fast, and the landscape will always change. Interviewers look for you to articulate your vision for the product one, five, maybe even ten years into the future.",
    },
    "clarifying_questions": {
        "human_name": "Clarifying Questions",
        "criteria": """
Very Weak or Missing: Failed to ask questions and/or interact with the interviewer.
Weak: Struggled to ask the right questions and/or made assumptions without clarifying.
Neutral: Asked good clarifying questions, but missed key points.
Strong: Asked insightful questions, adapted design to fit.
Very Strong: Asked surprising and insightful questions, came up with high-quality, novel design(s).
""",
        "description": "Designing a product is a problem-solving exercise. What problem are you trying to solve? To get at the root, you have to ask good questions.",
    },
    "ability_to_discuss_tradeoffs_and_possible_errors": {
        "human_name": "Ability to Discuss Tradeoffs and Possible Errors",
        "criteria": """
Very Weak or Missing: Failed to mention tradeoffs and possible errors.
Weak: Mentioned tradeoffs, but failed to justify decisions when pressed and/or made incorrect judgment calls.
Neutral: Covered possible errors and tradeoffs, but could have made better choices.
Strong: Logical tradeoff discussion, correctly identified possible errors.
Very Strong: Deep knowledge and intuition around tradeoffs; alternatives offered, pros and cons neatly summarized.
""",
        "description": "There will always be many possible opportunities to chase. The best way to arrive at a plan logically is to think through the tradeoffs of your decision -- and constantly check yourself for possible assumptions and errors. This will earn you big points in traditionally creative product design interviews.",
    },
    "passion_and_creativity": {
        "human_name": "Passion and Creativity",
        "criteria": """
Very Weak or Missing: Failed to show enthusiasm or creative thinking.
Weak: Solutions were bland, and/or the candidate didn't show interest in the problem.
Neutral: Displayed interest and reasonable insight, but nothing exceptional.
Strong: Extensive knowledge, enthusiasm, and creativity on display throughout the interview.
Very Strong: Gave inspired answers; showed clear passion.
""",
        "description": "Product questions are some of your best opportunities to show your culture fit. How? Get excited about the product! Interviewers want to see your passion for their company, and how you'll use that passion to fuel your creativity.",
    },
    "communication": {
        "human_name": "Communication",
        "criteria": """
Very Weak or Missing: Failed to communicate clearly despite repeated prompts.
Weak: Poor communication throughout; interviewer had trouble following despite prompts.
Neutral: Communication varied. Clear in some areas but vague / incomplete in others.
Strong: Good communication skills; articulated thought process clearly and consistently.
Very Strong: Clear, proactive communication; anticipated questions, articulated reasons for decision, "checked-in" throughout.
""",
        "description": "Communication is assessed in every interview.",
    },
    "collaboration": {
        "human_name": "Collaboration",
        "criteria": """
Very Weak or Missing: Failed to take the lead, didn't respond to guidance.
Weak: Struggled to stay on track without guidance.
Neutral: Took the lead and performed well, but may have needed redirects or hints.
Strong: Effectively led the discussion and involved the interviewer throughout.
Very Strong: Took the lead and made exceptional use of the interviewer, the discussion was more collaboration than interview.
""",
        "description": "Product design interviews are a great opportunity to collaborate as your interviewer has the context that you need in order to make good decision. Some interviews can turn into a collaborative problem-solving exercise; be sure to lead, ask good questions, check assumptions, and check-in, and you can't go wrong.",
    },
}


def calculate_score(verdict: str) -> int:
    if "Very Weak or Missing" in verdict:
        return 20
    elif "Weak" in verdict:
        return 40
    elif "Neutral" in verdict:
        return 60
    elif "Strong" in verdict:
        return 80
    elif "Very Strong" in verdict:
        return 100
    else:
        return 0


async def analyze_conversation(
    conversation: Conversation,
) -> ConversationOverallAnalysis:


    analysis_model = "cohere/command-r-plus-08-2024"
    # Make a copy of default_conversation_overall_analysis
    conversation_overall_analysis = deepcopy(default_conversation_overall_analysis)

    # Add the conversation to the conversation_overall_analysis
    conversation_overall_analysis.conversation = conversation

    # Prepare messages for the LLM
    system_message = {
        "role": "system",
        "content": "You are an expert at evaluating product management interviews. Your task is to analyze a conversation and provide a grade based on specific criteria, along with justification from the conversation.",
    }

    # Iterate through each rubric criterion
    for criterion, rubric in RUBRICS.items():
        user_message = {
            "role": "user",
            "content": f"Please evaluate the following conversation based on the criterion '{criterion}'. Use the following rubric:\n\n{rubric}\n\nProvide your verdict (e.g. 'Very Weak or Missing', 'Strong') and justify it with specific examples from the conversation. Please provide your verdict on one line and justrification on two different lines. For justification, use direct quotes from the conversation when possible.",
        }

        # Prepare the conversation for the LLM
        # intentionally ignore system messages
        conversation_messages = ""
        for msg in conversation["messages"]:
            if msg["role"] == "user":
                conversation_messages += f"User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                conversation_messages += f"Assistant: {msg['content']}\n"

        # Combine all messages
        messages = [
            system_message,
            {"role": "user", "content": conversation_messages},
            user_message,
        ]

        print("messages", messages)
        # Get the LLM's analysis
        analysis_result = await get_txt2txt_completion(messages, model=analysis_model)
        print("analysis_result", analysis_result)

        # Parse the result (assuming the LLM returns the verdict in the first line and justification after)
        verdict, justification = analysis_result.split("\n", 1)
        verdict = verdict.strip()
        justification = justification.strip()

        # Map the criterion to the corresponding field in ConversationAnalysis
        field_mapping = {
            "business_acumen": "business_acumen",
            "user_centricity": "user_centricity",
            "product_vision": "product_vision",
            "clarifying_questions": "clarifying_questions",
            "ability_to_discuss_tradeoffs_and_possible_errors": "ability_to_discuss_tradeoffs_and_possible_errors",
            "passion_and_creativity": "passion_and_creativity",
            "communication": "communication",
            "collaboration": "collaboration",
        }

        field = field_mapping.get(criterion)
        if field:
            setattr(
                conversation_overall_analysis.analysis,
                field,
                AnalysisScore(
                    name=criterion,
                    description=rubric["criteria"],
                    human_name=rubric["human_name"],
                    score=calculate_score(verdict),
                    feedback=justification,
                ),
            )

    # Calculate overall score and feedback
    scores = [
        getattr(conversation_overall_analysis.analysis, field).score
        for field in field_mapping.values()
        if hasattr(conversation_overall_analysis.analysis, field)
    ]
    conversation_overall_analysis.overall_score = sum(scores) // len(scores)

    overall_feedback_message = {
        "role": "user",
        "content": "Based on your analysis of the conversation, please provide an overall feedback summary.",
    }
    messages = [
        system_message,
        {"role": "user", "content": conversation_messages},
        overall_feedback_message,
    ]

    conversation_overall_analysis.overall_feedback = await get_txt2txt_completion(
        messages,
        model=analysis_model,
    )

    return conversation_overall_analysis
