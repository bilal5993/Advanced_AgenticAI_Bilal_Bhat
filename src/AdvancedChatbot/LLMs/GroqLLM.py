import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_inputs):
        self.user_inputs=user_inputs

    def get_llm_model(self):
        try:
            groq_api_key=self.user_inputs["GROQ_API_KEY"]
            selected_groq_model=self.user_inputs["llm_model"]
            if groq_api_key=='' and os.environ["GROQ_API_KEY"] =='':
                st.error("Please Enter the Groq API KEY")
            else:
                llm=ChatGroq(api_key=groq_api_key,model=selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error Ocuured With Exception : {e}")
        return llm