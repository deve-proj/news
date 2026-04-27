import aioboto3
from botocore.config import Config
import os
from dotenv import load_dotenv
from types_aiobotocore_s3 import S3Client
from fastapi import UploadFile, File

load_dotenv()

class MinioClient:


    async def get_client(self) -> S3Client:

        self.session = aioboto3.Session()

        config = Config(
            signature_version='s3v4',
            retries={'max_attempts': 3}
        )

        return self.session.client(
            's3',
            endpoint_url=f"http://{os.getenv("MINIO_HOST")}:{os.getenv("MINIO_PORT")}",
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
            config=config
        )

    async def get_all_buckets(self):

        async with await self.get_client() as s3:

            return await s3.list_buckets()
        

    async def upload_file(self, post_id : str, file : UploadFile = File(...), file_name : str = ""):

        async with (await self.get_client()) as s3:

            return await s3.put_object(
                Bucket="posts",
                Body=(await file.read()),
                Key=f"{post_id}/{file_name}",
                ContentType=file.content_type,
                ACL='public-read'
            )
        
    async def delete_post_files(self, post_id : str):

        prefix = f"{post_id}/"

        async with (await self.get_client()) as s3:

            paginator = s3.get_paginator('list_objects_v2')

            async for page in paginator.paginate(Bucket="posts", Prefix=prefix):

                if 'Contents' in page:

                    for obj in page['Contents']:

                        await s3.delete_object(Bucket="posts", Key=obj['Key'])