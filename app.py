import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI-powered Virtual Tutor", page_icon="🎓", layout="centered")

# Header with emoji icon instead of logo image
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.markdown("<h1 style='font-size: 48px;'>🎓</h1>", unsafe_allow_html=True)
with col2:
    st.title("AI TUTOR")

st.markdown("<div style='text-align: center; font-style: italic; margin-bottom: 20px;'>Accessible learning for every student, anytime, anywhere.</div>", unsafe_allow_html=True)

# Sidebar for API key
st.sidebar.header("🔐 API Access")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# User info form
with st.form("user_form"):
    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Email Address")
    subject = st.selectbox("📚 Choose a subject", ["General", "Math", "English", "Science"])
    submitted = st.form_submit_button("Start Tutoring")

if submitted and api_key:
    client = OpenAI(api_key=api_key)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.success(f"Welcome, {name}! Let's start learning {subject}.")

    st.markdown("---")
    st.subheader("Ask your tutor anything:")

    starter_questions = {
        "Math": ["What is the Pythagorean theorem?", "How do I solve quadratic equations?"],
        "English": ["What's a noun?", "How do I write a good essay introduction?"],
        "Science": ["What is photosynthesis?", "Explain Newton’s First Law."],
        "General": ["How can I study effectively?", "What's the best way to revise?"]
    }

    # Show starter questions buttons
    for q in starter_questions.get(subject, []):
        if st.button(q):
            st.session_state.user_input = q
            st.session_state.submit_q = True

    user_input = st.text_input("Type your question here:", key="input_field")
    ask_button = st.button("Ask", key="ask_button")

    if ask_button or st.session_state.get("submit_q"):
        user_input = user_input or st.session_state.get("user_input", "")
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a helpful virtual tutor specialized in {subject}."},
                    *st.session_state.chat_history,
                    {"role": "user", "content": user_input}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            answer = response.choices[0].message.content

            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

            st.markdown(f"**Tutor:** {answer}")
            st.session_state.submit_q = False

        except Exception as e:
            st.error(f"API error: {e}")

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("🗂️ Chat History")
        for i in range(0, len(st.session_state.chat_history), 2):
            user_msg = st.session_state.chat_history[i]["content"]
            assistant_msg = st.session_state.chat_history[i + 1]["content"]
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**Tutor:** {assistant_msg}")

elif submitted and not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
else:
    st.info("Please fill in your name, email, subject, and enter API key to begin.")
