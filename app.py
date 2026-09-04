import json
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Load FAQ data
# -----------------------------

with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)


questions = [faq["question"] for faq in faqs]
answers = [faq["answer"] for faq in faqs]


# -----------------------------
# Convert questions into numbers
# -----------------------------

vectorizer = TfidfVectorizer()

question_vectors = vectorizer.fit_transform(questions)


# -----------------------------
# Function to find the answer
# -----------------------------

def get_answer(user_question):

    user_vector = vectorizer.transform([user_question])

    similarity_scores = cosine_similarity(
        user_vector,
        question_vectors
    )

    best_match_index = similarity_scores.argmax()

    best_score = similarity_scores[0][best_match_index]

    if best_score < 0.2:
        return "Sorry, I don't understand that question. Please try asking something related to our FAQs."

    return answers[best_match_index]


# -----------------------------
# Website design
# -----------------------------

st.set_page_config(
    page_title="AI FAQ Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI FAQ Chatbot")

st.write(
    "Ask me a question and I will try to find the best answer!"
)


# -----------------------------
# User input
# -----------------------------

user_question = st.text_input(
    "Ask your question:"
)


# -----------------------------
# Chatbot response
# -----------------------------

if st.button("Ask Chatbot"):

    if user_question.strip() == "":
        st.warning("Please type a question first.")

    else:
        answer = get_answer(user_question)

        st.subheader("🤖 Chatbot:")
        st.write(answer)