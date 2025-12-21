from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import Iterable
from typing import Iterable
from functools import reduce
import operator

# def get_tools():
#     """
#     Return the list of tools to be used in the chatbot
#     """
#     tools=[TavilySearchResults(max_results=1)]
#     return tools

# def create_tool_node(tools):
#     """
#     creates and returns a tool node for the graph
#     """
#     return ToolNode(tools=tools)

load_dotenv()
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")

class DevelopTools:
    def __init__(self):
        self.tools=[]

    def get_mathmatical_functions_tool(self):
        """
        Performs basic arithmetic operations (addition, subtraction,
        multiplication, and division) on a given set of numbers and
        returns the computed result.
        """
        
        def sum_numbers(numbers: Iterable[float]) -> float:
            """
            Adds multiple numbers together and returns the total.
            Accepts any iterable (list, tuple, set, range, etc.).
            """
            self.tools.append(sum(numbers))
    
        def subtracts_numbers(a:int,b:int) -> int:
            """
            Adds multiple numbers together and returns the total.
            Accepts any iterable (list, tuple, set, range, etc.).
            """
            self.tools.append(a-b)
        
        def multiply_numbers(numbers: Iterable[float]) -> float:
            """
            Multiplies multiple numbers together and returns the product.
            Accepts any iterable (list, tuple, set, range, etc.).
            """
            try:
                self.tools.append(reduce(operator.mul, numbers, 1))
            except TypeError:
                raise ValueError("All elements must be numeric")

        def divide_numbers(numbers: Iterable[float]) -> float:
            """
            Divides numbers sequentially from left to right.
            Example:
                [100, 2, 5] → 100 / 2 / 5 = 10
            Accepts any iterable (list, tuple, range, etc.).
            """
            numbers = list(numbers)

            if len(numbers) < 2:
                raise ValueError("At least two numbers are required for division")

            result = numbers[0]
            for n in numbers[1:]:
                if n == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                result /= n
            
            self.tools.append(result)
        self.tools
    
    def create_tool_node(self,tools):
        """
        creates and returns a tool node for the graph
        """
        return ToolNode(tools=tools)


    @staticmethod
    def get_tavily_tool():
        """
        Return a tavily tool to be used in the chatbot after searching from tavily
        """
        tavily_tool=TavilySearchResults(max_results=1)
        return tavily_tool
    
    @staticmethod
    def get_scientists_tool():
        """
        Returns a tool that provides verified personal and background details
        about the creator (Data Scientist) of the chatbot.

        The information is dynamically retrieved from a ChromaDB knowledge base
        and can be used by the chatbot to answer questions such as:
        - Who created you?
        -Who created this chatbot?
        - Who is the owner of this chatbot?
        - Tell me about your creator

        This tool ensures consistent, accurate, and context-aware responses
        by deriving the creator’s details directly from the stored vector data.
        """

        loader=TextLoader('about_creator.txt')
        docs=loader.load()
        text_splitter=CharacterTextSplitter(chunk_size=500,chunk_overlap=0)
        documents= text_splitter.split_documents(docs)

        embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
       

        ## Add alll these text to vectordb
        vectorstore=Chroma.from_documents(
            documents=documents,
            embedding=embeddings
        )
        retriever=vectorstore.as_retriever()

        ### Retriever To Retriever Tools
        retriever_tool=retriever.as_tool(
            name="retriever_vector_db_blog",
            description="Search and run information about personal details"
        )
        return retriever_tool
    
    
    def main_function(self):
        tools=[]
        tavily_tool = self.get_tavily_tool()
        retriever_tool = self.get_scientists_tool()
        tools.append(tavily_tool)
        tools.append(retriever_tool)
        math_tools = self.get_mathmatical_functions_tool()
        if math_tools:
            tools.extend(math_tools)

        return tools
    
    

            