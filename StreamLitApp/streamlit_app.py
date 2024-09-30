import streamlit as st
import subprocess
import re

# Function for query preprocessing
def preprocess_prompt(prompt: str) -> str:
    # Example preprocessing: lowercasing and stripping unnecessary characters
    prompt = prompt.lower().strip()
    prompt = re.sub(r'[^\w\s]', '', prompt)  # Remove punctuation
    
    # Add a financial context to the prompt
    financial_context = "You are a financial advisor. Please provide advice related to the following query: "
    return financial_context + prompt

# Function for response post-processing
def postprocess_response(response: str) -> str:
    response = re.sub(r'<\|endoftext\|>', '', response)  # Clean end of text token
    return response.strip()

# Streamlit UI
st.title("Financial Advisor Chatbot")
st.write("Ask your finance-related questions! Get personalized financial advice.")

# Create a session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Tabs for conversation and history
tab1, tab2 = st.tabs(["Chat", "Conversation History"])

with tab1:
    # User input
    user_input = st.text_input("Enter your finance-related question:")
    
    if user_input:
        # Preprocess the user input
        preprocessed_input = preprocess_prompt(user_input)

        # Run the LLaMA 3.2 model using subprocess and ensure UTF-8 encoding
        try:
            result = subprocess.Popen(
                ['ollama', 'run', 'llama3.2'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
            )
            
            # Send the preprocessed prompt to the process and get the response
            output, error = result.communicate(input=preprocessed_input)

            # Post-process the response
            cleaned_output = postprocess_response(output)

            # Store the conversation in chat history
            if result.returncode == 0:
                # Append both user input and chatbot response to chat history
                st.session_state.chat_history.append({"user": user_input, "chatbot": cleaned_output})
                st.write(f"Chatbot: {cleaned_output}")
            else:
                st.error(f"Error: {error.strip()}")

        except Exception as e:
            st.error(f"Exception occurred: {str(e)}")

with tab2:
    st.write("### Conversation History")
    if st.session_state.chat_history:
        for i, chat in enumerate(st.session_state.chat_history):
            st.write(f"**User:** {chat['user']}")
            st.write(f"**Chatbot:** {chat['chatbot']}")
    else:
        st.write("No conversation history available.")




