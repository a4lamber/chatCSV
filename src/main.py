import os
from dotenv import load_dotenv,find_dotenv
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import tempfile

def init_chatbot():
    # load env variables and error handling if key not found
    _ = load_dotenv(find_dotenv())
    open_api_key = os.getenv("OPENAI_API_KEY")
    
    if open_api_key is None or len(open_api_key) == 0:
        st.error("Please set your OpenAI API key in the environment variable OPENAI_API_KEY.")
        return
    else:
        print("OpenAI API key found.")




def main():
    init_chatbot()
    
    st.set_page_config(
        page_title="Chat with CSV",
    )
    
    st.header("Ask your CSV")
    
    user_csv = st.file_uploader(
        "Upload your CSV file", 
        type = ["csv"],
    )
    
    
    
    # check if uploaded, if yes, start llm
    if user_csv is not None:
        user_question = st.text_input("Ask a question about your csv")
        
        # create temp file来绕过csv的error "create_csv_agent function expecting its path parameter to be a string or list but instead receiving an UploadedFile object from Streamlit"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temporary_file:
            temporary_file.write(user_csv.getvalue())
            
        llm = OpenAI(temperature = 0)
        # agent = create_csv_agent(llm,
        #                          user_csv,
        #                          verbose = True)
        
         # initialize agent
        agent = create_csv_agent(llm=llm,
                                 path=temporary_file.name,
                                 verbose=True)

        # delete temp file
        os.unlink(temporary_file.name)
    
        # 检查用户是否提问
        if user_question is not None and user_question != "":
            st.write(f"Your questions was: {user_question}")
            
            response = agent(user_question)
            st.write(response)
            
            
            
if __name__ == "__main__":
    main()