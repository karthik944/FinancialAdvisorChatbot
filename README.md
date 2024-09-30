# FinancialAdvisorChatbot
A Customised Financial Advisor Chatbot

Local LLM Setup and Interaction
1. Download Ollama from https://github.com/ollama/ollama 
2. Run "ollama run llama3.2" to verify the installation. 

Alternative LLM installation
<!-- Choosing GPT-2 as the alternate LLM, Many other LLM's are part of hugging face transformers library -->
1. Use GPT-2 by installing hugging face’s transformers library
2. Run the command “pip install transformers torch” to install transformers and torch library.
<!-- Optional but suggested to install datasets -->
3. Run “pip install datasets” to install dataset
4. Once Setup is done, create a file and load your preferred LLM(GPT-2 here) from hugging face’s transformers library.
5. Use the command “python  file_name.py Your_Prompt_here” to ask GPT-2 your prompt.


Command-Line Interaction Using Curl
<!-- Using FastApi to implement Command-Line Interaction Using Curl commands. -->
1. Run “pip install fastapi uvicorn” to install FastAPI
2. Create a python file to load your LLMs using FastAPI.
3. Run the file to host your LLM’s in the local system.
4. Once hosted open a new cmd prompt(preferably not powershell script) and run your curl commands.


StreamLit setup and installation
<!-- Choosing streamlit for UI of the chatbot -->
1. Run command “pip install streamlit” to install StreamLit.
2. Create a python file “file_name.py” and write the code to handle UI and backend logic.
3. Run command "streamlit run file_name.py" to host the chatbot in your local machine.

