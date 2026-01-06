from typing import TypedDict, List
class AgentState(TypedDict):
    input: str
    routes: list[str]
    output: str
