import asyncio
from llama_index.core.tools import FunctionTool
from src.service.monday_service import MondayService

monday_svc = MondayService()

BOARD_ID_DEFAULT = '18420016813'


def create_worskpace_tool(workspace_name:str) -> str:
    """use only when the user ask to create a new workspace"""
    return asyncio.run(monday_svc.create_workspace(workspace_name))

def create_board_tool(boar_name:str, workspace_id: str = None) ->str:
    """use when the user ask you to make a new board, the worskpace id could be completely optional"""
    return asyncio.run(monday_svc.create_board(boar_name,workspace_id))


def add_item_tool(nombre_elemento: str) -> str:
    """
    Use this when the user wants to add, jot down, log, or create a task, 
    to-do item, note, or entry on their Monday board.
    The user simply states what they want to add; the board is already preconfigured by default.
    """
    return asyncio.run(monday_svc.add_item(BOARD_ID_DEFAULT, nombre_elemento))

def delete_item_tool(id_elemento: str) -> str:
    """Use this when the user explicitly asks to delete, erase, or remove a task or item using its numeric ID."""
    return asyncio.run(monday_svc.delete_item(id_elemento))

monday_tools = [
    FunctionTool.from_defaults(fn=create_worskpace_tool),
    FunctionTool.from_defaults(fn=create_board_tool),
    FunctionTool.from_defaults(fn=add_item_tool),
    FunctionTool.from_defaults(fn=delete_item_tool)
]