import grpc
from ...grpc import user_pb2, user_pb2_grpc
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

class BackendClient:

    def __init__(self, host : str = os.getenv("BACKEND_URL")):
    
        self.channel = grpc.insecure_channel(host)

        self.stub = user_pb2_grpc.UserGrpcStub(self.channel)

    def get_user(self, user_id : str):

        try:

            request = user_pb2.UserRequest(id=user_id)
            response = self.stub.GetUser(request)

            return response

        except Exception as e:

            raise Exception(e)
        
    def get_users(self, user_ids : List[str]):

        try:

            request = user_pb2.UserListRequest(ids=user_ids)
            response = self.stub.GetUsers(request)

            return list(response.users)

        except Exception as e:

            raise Exception(e)
        