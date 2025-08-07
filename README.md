# Offline AI Assistant

A simple yet powerful Streamlit-based AI assistant that allows users to interact with locally running large language models (via Ollama) and optionally reference uploaded documents for context.
The app is available to run on a local server or directly on a local system, ensuring full control and data privacy.
It's also deployable for multiple users, making it suitable for internal team environments.

---

## Features

- Ask questions to an AI model (streamed responses)
- Upload `.pdf` or `.txt` files to provide extra context to the model
- Select from multiple local Ollama models
- Maintains conversational memory within a session
- User-friendly interface with styled chat bubbles

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM Backend**: [Ollama](https://ollama.com/) (for running local models like gpt-oss, LLaMA, Mistral, Phi, etc.)
- **PDF Parsing**: `PyPDF2`
- **Unique Session Tracking**: `uuid4`

---

## Installation

1. **Create and activate a virtual environment (optional but recommended):y**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Clone the repository**:
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Start your Ollama server and pull a model:(If Ollama model(s) are already installed, skip this step - All models will be listed on the app)**:
   ```bash
   ollama run phi  # or mistral, llama2, etc.

5. **Run the Streamlit app:**:
   ```bash
   streamlit run app.py

## File Upload Support
- Upload .pdf or .txt documents to add custom context for your questions.
- The first 3000 characters are passed as context to the AI.

## Local-Only Deployment
- This application runs entirely locally, ensuring your documents and chat history are not sent to any external server.


## 🙋‍♂️ Author
Developed by Kian Babanezhad
