# from typing_extensions import List, Literal
from typing import Literal, Annotated,TypedDict,List
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represents the state of graph structure
    """
    messages:Annotated[List,add_messages]
    validation: str