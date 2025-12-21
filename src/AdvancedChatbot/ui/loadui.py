import streamlit as st
import os
from src.AdvancedChatbot.ui.read_inifile import ReadIni
class LoadStreamliUI:
    def __init__(self):
        self.config =ReadIni()
        self.user_inputs ={}

    def login(self):
        """Login form using Streamlit secrets"""
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_btn = st.sidebar.button("Login")

        if login_btn:
            users = st.secrets["users"]
            if username in users and password == users[username]:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                # Auto-populate GROQ API key from secrets
                st.session_state["GROQ_API_KEY"] = st.secrets["GROQ"]["api_key"]
                st.session_state["TAVILY_API_KEY"] = st.secrets["GROQ"]["tavily_api_key"]
                st.session_state["HF_KEY"] = st.secrets["GROQ"]["hf_key"]
                # st.success(f"Logged in as {username}")
            else:
                st.session_state["logged_in"] = False
                st.error("Invalid username or password")


    def loadui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.markdown("<i style='color:gray;'>This chatbot has been developed by <b>Bilal Bhat</b> and will be continuously enhanced into a more advanced agentic AI system. It is currently in an active development phase.</i>",
                    unsafe_allow_html=True)
        # Check if user is logged in
        if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
            self.login()
            return  # Stop loading rest of UI until login succeeds

        
        with st.sidebar:
            # Get options from configuragion.ini file
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            groq_models = self.config.get_groq_moldes()
            
            # LLM selection
            self.user_inputs["llm_type"] = st.selectbox("Select LLM type", llm_options)

            if self.user_inputs["llm_type"] =='Groq':
                # groq models selection
                self.user_inputs["llm_model"] = st.selectbox("Select LLM Model", groq_models)
                # select your usecase
                self.user_inputs["your_usecase"] = st.selectbox("Select Your Usecase", usecase_options)

                if self.user_inputs["your_usecase"] == "Advanced Chatbot":
                    self.user_inputs["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]
                    self.user_inputs["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]
                    self.user_inputs["HF_KEY"] = st.session_state["HF_KEY"]
                    st.text_input("API Key",value=self.user_inputs["GROQ_API_KEY"],type="password",disabled=True) 
                    os.environ["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]
                    st.text_input("Tavily API Key",value=self.user_inputs["TAVILY_API_KEY"] ,type="password",disabled=True)
                    os.environ["HF_KEY"]=st.session_state["HF_KEY"]
                    st.text_input("HF API Key",value=self.user_inputs["HF_KEY"],type="password",disabled=True)

                    # Validate API key
                    if not self.user_inputs["GROQ_API_KEY"]:
                        st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")

        return self.user_inputs  

            

             

    
