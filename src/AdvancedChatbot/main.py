from  src.AdvancedChatbot.ui.loadui  import LoadStreamliUI
from pathlib import Path
import streamlit as st
from src.AdvancedChatbot.graph_workflows.graph_workflow import AdvancedChatbotGraph
from src.AdvancedChatbot.LLMs.GroqLLM import GroqLLM
from src.AdvancedChatbot.ui.display_resluts import DisplayResults

def Advanced_agentic_app():

    # Load streamlit ui 
    # base_dir = Path(__file__).resolve().parent
    # path = base_dir/"configuragion.ini"
    app_ui= LoadStreamliUI()

     # First, check login
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        app_ui.login()  # Show login form
        return     # Stop until user logs i
    
    user_inputs=app_ui.loadui()

    # Validate user_inputs
    if not user_inputs:
        st.error("Error: Failed to load user input from the UI.")
        return
    try:
        input_message = st.chat_input("Enter your message:")
        if input_message:
            groq_object=GroqLLM(user_inputs)
            llm=groq_object.get_llm_model()
            graph= AdvancedChatbotGraph(llm)
            graph =graph.call_graph(user_inputs["your_usecase"])
            DisplayResults(user_inputs["your_usecase"],graph,input_message).display_results_on_chatbot()

    except Exception as e:
        st.error(f"Results were not displayed due to error: {e}")
