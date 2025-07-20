import streamlit as st
import PyPDF2
import time
import re  # NEW: Importing the regular expression module
from utils.llm import ask_llm

# --- Session State Setup ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'candidate_data' not in st.session_state:
    st.session_state.candidate_data = {}
if 'questions' not in st.session_state:
    st.session_state.questions = ""
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = False

# --- Title ---
st.markdown("<h1 style='text-align: center; color: #ff6f61;'>TalentScout - AI Hiring Assistant</h1>", unsafe_allow_html=True)

# --- Initial Step: Welcome or Main Interface ---
if not st.session_state.candidate_data:
    st.info("Welcome to TalentScout! Please begin by uploading your resume and entering your details below.")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("1. Upload Resume")
            uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
            if uploaded_file:
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
                    st.session_state.resume_text = text
                    st.toast(f"✅ Resume '{uploaded_file.name}' uploaded successfully!")
                except Exception as e:
                    st.error(f"❌ Could not read the PDF. Error: {e}")

    with col2:
        with st.container(border=True):
            st.subheader("2. Enter Your Details")
            with st.form("candidate_form"):
                name = st.text_input("Your Full Name")
                email = st.text_input("Your Email")
                tech_stack = st.multiselect("Your Tech Stack", ["Python", "JavaScript", "Java", "C++", "React", "Node.js", "SQL", "AWS", "Docker"])
                submit_button = st.form_submit_button("✨ Generate Questions")

                if submit_button and name and email and tech_stack:
                    if not st.session_state.resume_text:
                        st.error("Please upload your resume first.")
                    else:
                        # --- NEW: Email Validation Logic ---
                        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_regex, email):
                            st.error("Invalid email format. Please enter a valid email address.")
                        else:
                            # If email is valid, proceed with the rest of the logic
                            st.session_state.candidate_data = {"name": name, "email": email, "tech_stack": tech_stack}
                            
                            progress_text = "Operation in progress. Please wait."
                            progress_bar = st.progress(0, text=progress_text)
                            
                            resume_context = st.session_state.resume_text.strip()
                            prompt = f"Generate 2 technical interview questions for a candidate skilled in: {', '.join(tech_stack)}. Resume:\n{resume_context}"

                            progress_bar.progress(30, text="Analyzing details...")
                            time.sleep(1)
                            
                            questions = ask_llm(prompt, persona="generator", stream=False)
                            st.session_state.questions = questions

                            progress_bar.progress(100, text="Done!")
                            time.sleep(0.5)
                            progress_bar.empty()

                            st.session_state.chat_history.append({"role": "user", "content": f"Submitted details for {name} with skills in {', '.join(tech_stack)}."})
                            st.session_state.chat_history.append({"role": "assistant", "content": f"Welcome {name}! Here are your interview questions:\n\n{questions}"})
                            st.rerun()

# --- Main Chat Interface (shown after initial submission) ---
else:
    # --- Sidebar Controls ---
    st.sidebar.title("Controls & Info")
    if st.session_state.resume_text:
        with st.sidebar.expander("📄 View Uploaded Resume"):
            st.text_area("", st.session_state.resume_text, height=300, disabled=True)
    
    if st.sidebar.button("🧹 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # --- Display Chat History ---
    st.markdown("### 📝 Interview & Chat History")
    for message in st.session_state.chat_history:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(name=message["role"], avatar=avatar):
            st.markdown(message["content"])

    # --- Interview Question Answer Form ---
    if st.session_state.questions and not st.session_state.questions_answered:
        st.markdown("---")
        st.subheader("3. Answer Your Questions")
        prompt = f"Evaluate the answer below by {st.session_state.candidate_data['name']}.\nQuestions:\n{st.session_state.questions}\nMy Answer is:"
        
        if answer := st.chat_input("Write your answers here and press Enter..."):
            st.session_state.questions_answered = True
            st.session_state.chat_history.append({"role": "user", "content": answer})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(answer)

            final_prompt = f"{prompt}\n\n{answer}\n\nCandidate's Resume for context:\n{st.session_state.resume_text}"
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Evaluating..."):
                    response = ask_llm(final_prompt, persona="evaluator", stream=True)
                    evaluation = st.write_stream(response)
            
            st.session_state.chat_history.append({"role": "assistant", "content": evaluation})
            st.rerun()

    # --- Context-Aware Chat Input ---
    if user_prompt := st.chat_input("Ask a follow-up question..."):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_prompt)

        context_parts = ["--- CANDIDATE RESUME ---\n" + st.session_state.resume_text if st.session_state.resume_text else ""]
        context_parts.append("\n--- CURRENT CONVERSATION ---")
        for msg in st.session_state.chat_history:
            context_parts.append(f"**{msg['role'].title()}**: {msg['content']}")
        full_context_prompt = "\n".join(context_parts)

        with st.chat_message("assistant", avatar="🤖"):
            response_generator = ask_llm(full_context_prompt, persona="chat", stream=True)
            full_response = st.write_stream(response_generator)
        
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})



