from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import DiaryEntry, PersonalityScore
from backend.psychometrics import cluster_descriptions  
import requests
import os

recommendation_router = APIRouter(prefix="/recommend", tags=["Recommendations"])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@recommendation_router.get("/user/{user_id}")
def get_dynamic_recommendation(user_id: int, session: Session = Depends(get_session)):
    # Get latest diary entry (if any)
    diary_entry = session.exec(
        select(DiaryEntry).where(DiaryEntry.user_id == user_id)
        .order_by(DiaryEntry.created_at.desc())
    ).first()

    personality = session.exec(
        select(PersonalityScore).where(PersonalityScore.user_id == user_id)
        .order_by(PersonalityScore.id.desc())
    ).first()
    sentiment = diary_entry.sentiment.upper() if diary_entry else "NEUTRAL"
    diary_info = (
        f"The user recently wrote a diary expressing {sentiment.lower()} feelings."
        if diary_entry else "No diary entry is available. Assume a neutral emotional state."
    )
    cluster = personality.cluster if personality else "unknown"
    cluster_summary = (
        cluster_descriptions.get(cluster, "No psychometric profile is available.")
        if personality else "No psychometric profile is available. Assume an average balanced personality."
    )
    cluster_info = (
        f"Their personality profile matches: {cluster_summary}"
    )
    prompt = (
        f"{diary_info} {cluster_info} "
        f"Based on this, provide a supportive, empathetic mental wellness recommendation for them in 100 words"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a compassionate mental health assistant."},
            {"role": "user", "content": prompt}
        ],
    }

    try:
        response = requests.post(OPENROUTER_URL, json=data, headers=headers)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return {"error": "LLM API call failed", "details": str(e)}

    return {
        "sentiment": sentiment,
        "cluster": cluster,
        "cluster_description": cluster_summary,
        "generated_recommendation": reply
        }

# from fastapi import APIRouter, Depends
# from sqlmodel import Session, select
# from backend.database import get_session
# from backend.models import DiaryEntry, PersonalityScore
# from backend.psychometrics import cluster_descriptions  
# import requests
# import os

# recommendation_router = APIRouter(prefix="/recommend", tags=["Recommendations"])

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# @recommendation_router.get("/user/{user_id}")
# def get_dynamic_recommendation(user_id: int, session: Session = Depends(get_session)):
#     diary_entry = session.exec(
#         select(DiaryEntry).where(DiaryEntry.user_id == user_id)
#         .order_by(DiaryEntry.created_at.desc())
#     ).first()

#     personality = session.exec(
#         select(PersonalityScore).where(PersonalityScore.user_id == user_id)
#         .order_by(PersonalityScore.id.desc())
#     ).first()

#     if not diary_entry or not personality:
#         return {"error": "Insufficient data. Complete diary + psychometric test first."}

#     sentiment = diary_entry.sentiment.upper()
#     cluster = personality.cluster
#     cluster_summary = cluster_descriptions.get(cluster, "Unknown personality cluster.")

#     prompt = (
#         f"The user recently wrote a diary expressing {sentiment.lower()} feelings. "
#         f"Their personality profile matches {cluster_summary} "
#         f"Based on this, provide a supportive, empathetic mental wellness recommendation for them."
#     )
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "mistralai/mistral-7b-instruct",
#         "messages": [
#             {"role": "system", "content": "You are a compassionate mental health assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     }
#     response = requests.post(OPENROUTER_URL, json=data, headers=headers)

#     if response.status_code != 200:
#         return {
#             "error": f"LLM API error: {response.status_code}",
#             "details": response.json()
#         }
#     reply = response.json()["choices"][0]["message"]["content"]

#     return {
#         "sentiment": sentiment,
#         "cluster": cluster,
#         "cluster_description": cluster_summary,
#         "generated_recommendation": reply
#     }

# # from fastapi import APIRouter, Depends
# # from sqlmodel import Session, select
# # from backend.database import get_session
# # from backend.models import DiaryEntry, PersonalityScore

# # recommendation_router = APIRouter(prefix="/recommend", tags=["Recommendations"])

# # # Predefined messages for personality clusters
# # cluster_tips = {
# #     0: "You're likely self-reflective and reserved. Try journaling or meditation.",
# #     1: "You’re outgoing and curious. Consider group activities like yoga or a book club.",
# #     2: "You may be emotionally sensitive. Maintain a daily gratitude list and try breathing exercises."
# # }

# # # Sentiment-based tips
# # sentiment_tips = {
# #     "POSITIVE": "Keep doing what makes you happy! You can explore creative hobbies or help others.",
# #     "NEGATIVE": "It's okay to feel low. Talk to a friend or practice grounding exercises.",
# #     "NEUTRAL": "Try adding something uplifting to your routine—like nature walks or music."
# # }

# # @recommendation_router.get("/user/{user_id}")
# # def get_recommendation(user_id: int, session: Session = Depends(get_session)):
# #     diary_entry = session.exec(
# #         select(DiaryEntry).where(DiaryEntry.user_id == user_id)
# #         .order_by(DiaryEntry.created_at.desc())
# #     ).first()

# #     personality = session.exec(
# #         select(PersonalityScore).where(PersonalityScore.user_id == user_id)
# #         .order_by(PersonalityScore.id.desc())
# #     ).first()

# #     if not diary_entry or not personality:
# #         return {"error": "Insufficient data. Complete diary + psychometric test first."}

# #     mood_tip = sentiment_tips.get(diary_entry.sentiment.upper(), "Stay balanced and be kind to yourself.")
# #     profile_tip = cluster_tips.get(personality.cluster, "Take time to understand yourself better.")

# #     return {
# #         "mood_tip": mood_tip,
# #         "personality_tip": profile_tip,
# #         "final_message": f"{mood_tip} {profile_tip}"
# #     }
