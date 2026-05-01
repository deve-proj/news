from aiodataloader import DataLoader
from typing import List, Dict, Any
from ...clients.backend.backendClient import BackendClient

class UserLoader(DataLoader):
    
    def __init__(self, backend_client : BackendClient):
        super().__init__()
        self.backend_client = backend_client
    
    async def batch_load_fn(self, user_ids: List[str]) -> List[Dict]:

        users = self.backend_client.get_users(user_ids)

        users_map = {user.id: user for user in users}

        return [users_map.get(uid) for uid in user_ids]