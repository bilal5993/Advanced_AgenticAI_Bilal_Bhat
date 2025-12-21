from langgraph.graph import StateGraph,START,END
from src.AdvancedChatbot.state.state_graph import State
from langgraph.prebuilt import tools_condition,ToolNode
# from src.AdvancedChatbot.Tools.search_tool import get_tools,create_tool_node
from src.AdvancedChatbot.nodes.advacnced_chatbot import AdvancedChatbotNode
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from src.AdvancedChatbot.Tools.search_tool import DevelopTools


class AdvancedChatbotGraph:
    def __init__(self,llm,):
        self.llm=llm
        self.builder=StateGraph(State)

    def advanced_build_graph(self):
        # call nodes
        obj=DevelopTools()
        tools = obj.main_function()
        tools_node=obj.create_tool_node(tools)
        nodes=AdvancedChatbotNode(self.llm)
        chatbot_node= nodes.create_advanced_chabotNode(tools)
        validate_node =nodes.create_validate_node()
        
        # add nodes
        self.builder.add_node("chatbot_node",chatbot_node)
        self.builder.add_node("validate_node",validate_node)
        self.builder.add_node("tools", tools_node)
        
        # Add edges
        self.builder.add_edge(START, "chatbot_node")
        self.builder.add_conditional_edges("chatbot_node",tools_condition)
        # self.builder.add_edge(tools,"tools_node")
        self.builder.add_edge("tools", "chatbot_node")
        self.builder.add_edge("chatbot_node", "validate_node")
        self.builder.add_conditional_edges("validate_node",nodes.route_after_validation,{"valid":END, "invalid":"chatbot_node"} )

        

    def call_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Advanced Chatbot":
            self.advanced_build_graph()

        # if usecase == "Basic Chatbot":
        #     self.basic_chatbot_build_graph()
        
        # if usecase == "Chatbot with Web":
        #     self.chatbot_with_tools_build_graph()
        
        # if usecase == "AI News":
        #     self.ai_news_builder_graph()
        
        # complie the graph
        memory=MemorySaver()
        graph= self.builder.compile(checkpointer=memory)
        # display(Image(graph.get_graph().draw_mermaid_png()))

        return graph


