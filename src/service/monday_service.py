import os
import httpx
from typing import Optional, Dict, Any

class MondayService:
    def __init__(self):
        self.api_url = 'https://api.monday.com/v2'
        self.api_key = os.getenv('MONDAY_API_KEY')
        self.headers = {
            'Authorization': self.api_key,
            'Conten-Type' : 'application/json',
            'API-Version': '2026-07'
        }
    
    async def _execute_query(self, query: str, variables: Optional[Dict[str, any]]):
        """Metodo privado para centralizar las peticiones http a monday."""
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    json={"query": query, "variables": variables or {}},
                    headers=self.headers,
                    timeout=15.0
                )
                
                res_data = response.json()
                if 'errors' in res_data:
                    raise Exception(res_data['errors'][0]['message'])
                return res_data.get('data',{})
            except Exception as e:
                return {
                    'error': str(e)
                }
                
    async def create_workspace(self, name:str) ->str:
        query = """
        mutation ($name:String!){
            create_workspace (name:$name, kind: open){
                id
                name
            }
        }
        """
        
        data = await self._execute_query(query,{'name': name})
        if 'error' in data: return f'No puede crear el espacio de trabajo. {data['error']}'
        return f'Escpacio de trabajo {data['create_workspace']['name']} creado con ID: {data['create_workspace']['id']}'
    
    async def add_item(self, board_id: str, item_name: str) -> str:
        query = """
        mutation ($boardId: ID!, $itemName: String!) {
            create_item (board_id: $boardId, item_name: $itemName) {
                id
            }
        }
        """
        data = await self._ejecutar_query(query, {"boardId": board_id, "itemName": item_name})
        if "error" in data: return f"No pude agregar el elemento. {data['error']}"
        return f"Elemento '{item_name}' agregado exitosamente al tablero."
    
    async def delete_item(self, item_id: str) -> str:
        query = """
        mutation ($itemId: ID!) {
            delete_item (item_id: $itemId) {
                id
            }
        }
        """
        data = await self._ejecutar_query(query, {"itemId": item_id})
        if "error" in data: return f"No pude eliminar el elemento. {data['error']}"
        return f"Elemento con ID {item_id} eliminado correctamente."