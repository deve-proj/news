import grpc
from ...grpc import user_pb2, user_pb2_grpc
from dotenv import load_dotenv
import os

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