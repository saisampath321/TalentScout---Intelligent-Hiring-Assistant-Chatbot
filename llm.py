# llm.py (Improved Version)
import requests
import json
import time

# Define different personas for different tasks
PERSONAS = {
    "interviewer": """You are TalentScout, an AI Hiring Assistant behaving like a professional recruiter or technical interviewer. Your job is to ask intelligent, open-ended interview questions based on the full context of the conversation and the candidate's resume.
RULES:
- Only ask one question at a time.
- Do NOT answer questions yourself, but guide the conversation.
- Focus on assessing the candidate's abilities.
- NEVER say you're a language model.""",

    "generator": """You are a helpful AI assistant. Your task is to generate technical interview questions based on the provided topic.
RULES:
- Generate the exact number of questions requested.
- The questions should be clear, relevant, and well-formatted.""",

    "evaluator": """You are an expert AI assistant. Your task is to evaluate a candidate's answer to an interview question based on their resume and the provided context.
RULES:
- Provide a constructive, professional evaluation in markdown.
- Be fair and objective.
- Explain the strengths and weaknesses of the answer.""",
    
    # A persona for general chat that can answer questions
    "chat": "You are TalentScout, a helpful AI hiring assistant. Your goal is to help the candidate by answering their questions clearly and concisely based on the provided conversation context."
}

def ask_llm(prompt, persona="chat", stream=False):
    """
    Calls the local LLM with a specific persona and streaming option.
    """
    try:
        system_instruction = PERSONAS.get(persona, PERSONAS["chat"])
        full_prompt = f"{system_instruction}\n\nUser: {prompt.strip()}\nAI:"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": full_prompt,
                "stream": stream
            },
            stream=stream  # Pass stream argument to requests
        )
        response.raise_for_status()  # Raise an exception for bad status codes (like 404 or 500)

        if stream:
            def response_generator():
                for chunk in response.iter_lines():
                    if chunk:
                        data = json.loads(chunk)
                        yield data.get("response", "")
                        # The model might stop responding with a 'done' key
                        if data.get("done"):
                            break
            return response_generator()
        else:
            # Handle non-streaming response
            full_content = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    full_content += data.get("response", "")
                    if data.get("done"):
                        break
            return full_content

    except requests.exceptions.RequestException as e:
        # Handle connection errors gracefully in the UI
        return f"Connection Error: Could not connect to the AI model at http://localhost:11434. Please ensure Ollama is running. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
