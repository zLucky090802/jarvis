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
    
    async def _ejecutar_query(self, query: str, variables: Optional[Dict[str, any]]):
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
    