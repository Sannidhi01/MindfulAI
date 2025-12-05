import requests
import os
import uuid
from fastapi import APIRouter, Body

chatbot_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "my_api_key")

# Temporary in-memory conversation store
session_memory = {}

INSTRUCTION_BLOCK = """
You are a compassionate and emotionally intelligent mental health assistant.

Your role is to:
- Listen deeply and infer the user's emotional state even if not stated directly.
- Respond appropriately based on the tone and context of their message.

If the user expresses something happy or light: Respond briefly and joyfully. Congratulate them, match their excitement, and encourage positive reflection.
If the user expresses stress, sadness, loneliness, anger, fear, grief, or confusion: Respond warmly and gently, offering emotional support and small coping suggestions (like breathing, journaling, or reflection).
If emotions are mixed or unclear: Gently reflect their tone and invite them to explore more if they wish.

DO NOT:
- Over-explain or flood with techniques unless the user asks for them.
- Tell the user to “talk to someone else” or “see a therapist”.
- Give generic robotic answers.

Use a calm, human-like, empathetic tone. Keep replies appropriately short or deep based on what the user needs.
You are not supposed to answer anything not related to mental health or emotions, if the user wants any information other than what is related to mental health and emotion politely deny that you are a mental health assistant and you can only provide assistance to cope up with happy or sad situations.
Your support alone is meaningful. Continue the conversation:
"""

# Start a new session
@chatbot_router.post("/start")
def start_new_session():
    session_id = str(uuid.uuid4())
    session_memory[session_id] = []  # empty memory for this session
    return {"session_id": session_id}

# Continue a chat in existing session
@chatbot_router.post("/ask")
def ask_chatbot(
    message: str = Body(...),
    session_id: str = Body(...)
):
    # Ensure session exists
    if session_id not in session_memory:
        session_memory[session_id] = []

    # Add user message to session memory
    session_memory[session_id].append({"role": "user", "content": message})

    # Keep only the last 6 turns (3 exchanges)
    if len(session_memory[session_id]) > 6:
        session_memory[session_id] = session_memory[session_id][-6:]

    # Full prompt with system instruction
    messages = [{"role": "system", "content": INSTRUCTION_BLOCK}] + session_memory[session_id]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages,
        "max_tokens": 150
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)

    try:
        response_json = response.json()
        if "choices" not in response_json:
            print("\n API Error Response:", response_json)
            return {"reply": "Sorry, something went wrong with the AI response."}

        assistant_reply = response_json['choices'][0]['message']['content']
        session_memory[session_id].append({"role": "assistant", "content": assistant_reply})

        return {"reply": assistant_reply, "session_id": session_id}

    except Exception as e:
        print("\n Exception occurred:", e)
        return {"reply": "Something went wrong while processing your request."}
if __name__ == "__main__":
    # Start a new session
    import uuid
    session_id = str(uuid.uuid4())
    session_memory[session_id] = []

    print(f"\n New session started: {session_id}")
    print("Type 'exit' to end the chat.\n")

    while True:
        user_input = input(" You: ")

        if user_input.lower() == "exit":
            print(" Ending session. Goodbye!")
            break

        # Simulate a call to ask_chatbot
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            session_memory[session_id].append({"role": "user", "content": user_input})

            if len(session_memory[session_id]) > 6:
                session_memory[session_id] = session_memory[session_id][-6:]

            messages = [{"role": "system", "content": INSTRUCTION_BLOCK}] + session_memory[session_id]

            data = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": messages,
                "max_tokens": 150
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
            response_json = response.json()

            if "choices" not in response_json:
                print("\n API Error:", response_json)
                continue

            assistant_reply = response_json['choices'][0]['message']['content']
            session_memory[session_id].append({"role": "assistant", "content": assistant_reply})

            print(f"\n🤖 Assistant: {assistant_reply}\n")

        except Exception as e:
            print(" Error occurred:", e)
