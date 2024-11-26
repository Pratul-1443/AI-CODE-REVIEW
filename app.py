import streamlit as st
import google.generativeai as genai


f = open("keys/gemini.txt")

key = f.read()

genai.configure(api_key=key)

sys_prompt = """You are a helpful AI Code Reviewer for Python and Other programming Languages like C,C++,Java etc.
                Users will submit their Python code for review and receive feedback on potential bugs along with suggestions for fixes.
                You should be user-friendly, flexible, fast responce, efficient, and provide accurate bug reports and fixed code snippets.
                You are expected to reply in as much detail as possible in easy words and fast.
                Make sure to take example while explaining a concept.

                The response should follow the below conditions.
                1. Response should start with a Big and bold font that says "Debug Code".
                2. Then a brief report of the bug in the code, with the headline "Bugs Summary" and start with the sentence "The bugs in the code are:".
                3. After the bug report, a snippet of the correct code should be given as a response with the header "Fixed Code". The fixed code snippet should be inside a box with proper coding structure (no extra characters, only the fixed code).
                
                In case a user asks any question outside the programming code scope,
                politely decline the request and tell them to ask the question from the Python code domain only."""

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

st.title("_:blue[AI Code Reviewer.....]_")
st.markdown("<small>Powered by Spark</small>", unsafe_allow_html=True) 
st.subheader("Enter your Python code for review:")
user_code = st.text_area("Enter you Python code here....", height=100)

if st.button("Generate Review"):
    if user_code.strip():
        with st.spinner("Reviewing your code..."):
            try:
                response = model.generate_content(user_code)

                st.markdown("## Code Review")
                
                response_text = response.text

                if "Bug Report" in response_text:
                    bug_report = response_text.split("Bug Report")[1].split("Fixed Code")[0].strip()
                    st.markdown("### Bug Report")
                    st.write(bug_report)

                if "Fixed Code" in response_text:
                    fixed_code = response_text.split("Fixed Code")[1].strip()

                    fixed_code_cleaned = fixed_code.replace("```", "").replace("python", "").strip()

                    st.markdown("### Fixed Code")
                    st.code(fixed_code_cleaned)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter some Python code!")