# MindfulAI – Your AI-powered Mental Health Companion

MindfulAI is an intelligent mental health assistance platform designed to support users in monitoring their emotional well-being. By leveraging AI, sentiment analysis, and psychometric profiling, MindfulAI provides personalized insights, recommendations, and a conversational companion to improve mental health outcomes.

---

## 🌟 Features

- **Chatbot for Mental Health Support**  
  Engage in empathetic conversations with an AI chatbot trained to respond to mood and emotional states.

- **Diary Logging & Sentiment Analysis**  
  Users can log daily entries, and MindfulAI analyzes sentiment to track emotional trends over time.

- **Psychometric Analysis**  
  Uses K-Prototypes clustering and personality quizzes to categorize users into different personalities to offer tailored recommendations.

- **Personalized Recommendations**  
  Suggests activities, resources, and coping strategies based on mood trends and psychometric profile.

- **User Management**  
  Supports secure login/signup and stores user-specific data for personalized tracking.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)  
- **Database:** MySQL (SQLModel ORM)  
- **Machine Learning:** Hugging Face Transformer - cardiffnlp/twitter-roberta-base-sentiment ( NLP ), Scikit-learn (KModes), NumPy, Pandas
- **OpenRouter API LLM:** mistralai/mistral-7b-instruct
- **Frontend:** HTML, CSS, JavaScript  
- **APIs:** Custom endpoints for diary logging, chatbot interaction, and recommendation retrieval

---

## ⚡ How It Works

1. **User Signup/Login** – Secure authentication to manage personal data.  
2. **Chatbot Interaction** – Users can converse with the AI, which detects sentiment in real-time.  
3. **Diary Entries** – Daily logs are analyzed for sentiment and emotional trends.  
4. **Psychometric Assessment** – Personality quiz and clustering classify users into mental health profiles.  
5. **Recommendations** – Tailored suggestions are generated based on mood trends and psychometric results.  
