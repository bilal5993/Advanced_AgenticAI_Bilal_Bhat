from src.AdvancedChatbot.state.state_graph import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage,SystemMessage 
from typing import Literal

class AdvancedChatbotNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self,llm):
        self.llm = llm

    # def process(self, state: State) -> dict:
    #     """
    #     Processes the input state and generates a response with tool integration.
    #     """
    #     user_input = state["messages"][-1] if state["messages"] else ""
    #     llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

    #     # Simulate tool-specific logic
    #     tools_response = f"Tool integration for: '{user_input}'"

    #     return {"messages": [llm_response, tools_response]}
    

    def create_advanced_chabotNode(self, tools):
        """
        Returns a chatbot node function.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            res=llm_with_tools.invoke(state["messages"])
            return {"messages": [res]}

        return chatbot_node
    
    def create_validate_node(self):

        prompt = ChatPromptTemplate.from_messages([
            ("system","""
            "Decide whether the chatbot response correctly answers the user question. "
            "Reply ONLY with 'valid' or 'invalid'."
             """ ),
            ("user",
            "Question:\n{question}\n\nAnswer:\n{answer}")
        ])

        def validate_node(state: State):
            question = state["messages"][-2].content
            answer = state["messages"][-1].content


            formatted_prompt = prompt.invoke({
                "question": question,
                "answer": answer
            })

            result = self.llm.invoke(formatted_prompt)

            state["validation"] = result.content.strip().lower()
            return state

        return validate_node
    
    # Routing
    @staticmethod
    def route_after_validation(state: State) -> Literal["valid","invalid"]:
        return state["validation"]
