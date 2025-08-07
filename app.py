import streamlit as st
import ollama
from uuid import uuid4
import PyPDF2

st.set_page_config(page_title="Internal AI Assistant", layout="centered")

# Assign a unique session ID once per browser tab
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

# Initialize chat and file state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_text" not in st.session_state:
    st.session_state.uploaded_text = ""

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = ""

@st.cache_data(ttl=10)
def get_models():
    ollama_models = ollama.list()
    def clean_model_name(model):
        name, *tag = model.model.split(':')
        return name if tag and tag[0] == "latest" else model.model
    return [clean_model_name(model) for model in ollama_models.models]

# Sidebar: model selection + file upload
with st.sidebar:
    st.title("⚙️ Settings")
    selected_model = st.selectbox("Choose a model", get_models())

    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            extracted_text = "\n".join([page.extract_text() or "" for page in reader.pages])
        else:
            extracted_text = uploaded_file.read().decode("utf-8")

        st.session_state.uploaded_text = extracted_text[:3000]  # trim to avoid model overflow
        st.session_state.uploaded_file_name = uploaded_file.name

    if st.session_state.uploaded_file_name:
        st.info(f"📄 Uploaded: `{st.session_state.uploaded_file_name}`")

# Title
st.markdown("<h2 style='text-align: center;'>🧠 <span style='color:#3c474a;'>Internal AI Assistant</span></h2>", unsafe_allow_html=True)

# Show previous chat messages
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"""<div style="text-align:right;background-color:#D9FDD3;padding:10px;
            border-radius:10px;margin-bottom:5px"><strong>You:</strong> {msg["content"]}</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div style="text-align:left;background-color:#F1F0F0;padding:10px;
            border-radius:10px;margin-bottom:5px"><strong>AI:</strong> {msg["content"]}</div>""",
            unsafe_allow_html=True,
        )

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.markdown(
        f"""<div style="text-align:right;background-color:#D9FDD3;padding:10px;
        border-radius:10px;margin-bottom:5px"><strong>You:</strong> {user_input}</div>""",
        unsafe_allow_html=True,
    )

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    ai_container = st.empty()
    full_reply = ""

    # Compose system prompt with document context if available
    system_prompt = (
    "You are an internal AI Assistant. ")

    if st.session_state.uploaded_text:
        system_prompt += f"\nHere is a document uploaded by the user that may help you answer questions:\n{st.session_state.uploaded_text}"

    messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history

    try:
        stream = ollama.chat(model=selected_model, stream=True, messages=messages)

        for chunk in stream:
            full_reply += chunk["message"]["content"]
            ai_container.markdown(
                f"""<div style="text-align:left;background-color:#F1F0F0;padding:10px;
                border-radius:10px;margin-bottom:5px"><strong>AI:</strong> {full_reply}▌</div>""",
                unsafe_allow_html=True,
            )

        st.session_state.chat_history.append({"role": "assistant", "content": full_reply})

        ai_container.markdown(
            f"""<div style="text-align:left;background-color:#F1F0F0;padding:10px;
            border-radius:10px;margin-bottom:5px"><strong>AI:</strong> {full_reply}</div>""",
            unsafe_allow_html=True,
        )

    except Exception as e:
        ai_container.error(f"Error: {e}")
