# TalentScout - Intelligent Hiring Assistant Chatbot

TalentScout is a fictional recruitment agency specializing in technology placements. This chatbot streamlines the initial screening process by collecting key candidate information and generating technical questions tailored to their declared tech stack.

## 🚀 Features

- 📋 Collects candidate details:
  - upload resume
  - Name
  - Email
  - Phone Number
  - Tech Stack

- 🧠 Generates 1–2 relevant technical questions based on candidate's tech stack using a local LLM (LLaMA3 via Ollama).

- 💬 Interactive, context-aware conversation flow via Streamlit interface.

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama (LLaMA3)
- Local LLM serving (no OpenAI or hugging face  )

## 🧾 Installation

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the LLaMA3 model using Ollama**:
    ```bash
    ollama run llama3
    ```

3. **Launch the chatbot**:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```
.
├── app.py                # Main Streamlit UI
├── utils/
│   └── llm.py            # Handles LLM request to Ollama
├── requirements.txt
└── README.md
```

## ✅ Assignment Goals Met

- ✅ Information collection for hiring
- ✅ Technical question generation based on tech stack
- ✅ Local deployment using open LLM
- ✅ Clean Streamlit interface
- ✅ No paid API used (uses local Ollama with llama3)

## 📌 Note
Make sure Ollama is installed and running on your system before starting the app. Visit [https://ollama.com](https://ollama.com) for installation instructions.

---

**Submitted For**: AI/ML Internship Assignment – "TalentScout"


# TalentScout - Intelligent Hiring Assistant Chatbot 🤖

TalentScout is a cutting-edge AI-powered hiring assistant designed to streamline the initial candidate screening process for tech recruitment. By leveraging local Large Language Models (LLMs), it collects essential candidate information and generates tailored technical questions based on their declared tech stack, all within an interactive chat interface.

## ✨ Features

  * **📋 Candidate Information Collection**: Gathers crucial details like full name, email, phone number, years of experience, desired position(s), location, and tech stack.
  * **🧠 Intelligent Question Generation**: Dynamically creates 2 relevant technical interview questions based on the candidate's uploaded resume and specified tech stack using a local LLM (LLaMA3 via Ollama).
  * **💬 Interactive Chat Interface**: Provides a seamless and context-aware conversational flow powered by Streamlit.
  * **🚫 Local LLM Deployment**: Operates entirely with a local LLM, eliminating the need for external APIs (e.g., OpenAI, HuggingFace), ensuring data privacy and cost-effectiveness.
  * **✅ Resume Parsing**: Extracts text from uploaded PDF resumes to inform question generation and evaluation.
  * **📧 Email Validation**: Includes basic email format validation during candidate detail entry.

## 🛠️ Tech Stack

  * **Python**: The core programming language.
  * **Streamlit**: For building the interactive web application interface.
  * **Ollama**: Used to run the LLaMA3 large language model locally.
  * **PyPDF2**: For extracting text from PDF resumes.
  * **Requests**: For making API calls to the local Ollama server.

## 🚀 Getting Started

Follow these steps to set up and run TalentScout on your local machine.

### Prerequisites

  * **Python 3.8+**
  * **Ollama**: Ensure Ollama is installed and running on your system. You can download it from [https://ollama.com](https://ollama.com).

