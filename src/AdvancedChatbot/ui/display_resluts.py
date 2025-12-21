import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import uuid
 
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

class DisplayResults:
    def __init__(self,usecase,graph,input_message):
        self.usecase= usecase
        self.graph = graph
        self.input_message = input_message

    def display_results_on_chatbot(self):
        if "thread_id" not in st.session_state:
            st.session_state.thread_id = str(uuid.uuid4())
            
        config = {"configurable": {"thread_id": st.session_state.thread_id}}

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        if self.usecase =='Advanced Chatbot':
            # input_message = {"messages": [self.input_message]}
            human_msg = HumanMessage(content=self.input_message)
            st.session_state["messages"].append(human_msg)
            response = self.graph.invoke({"messages":st.session_state["messages"]},config=config)
            # Update memory with new messages
            st.session_state["messages"] = response["messages"]
            for message in st.session_state["messages"]:
                if not message.content:
                    continue
                if type(message)==HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)==AIMessage:
                    with st.chat_message("AI"):
                        st.write(message.content)
                # elif type(message)==ToolMessage:
                #     with st.chat_message("Tool"):
                #         st.write(message.content)