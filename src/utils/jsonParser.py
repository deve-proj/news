import json
from ..models.post_model import post_model
import os
from dotenv import load_dotenv

load_dotenv()

def replace_image_name_to_url_in_post(post : post_model, post_id : str = ''):

    try:

        for image in list(filter(lambda block: block.type == 'image', post.content)):

            image.value = f'http://{os.getenv("MINIO_HOST")}{f":{os.getenv("MINIO_PORT")}" if os.getenv("MINIO_HOST") == 'localhost' else ''}/posts/{post_id}/{image.value}'

        post.preview_image = f'http://{os.getenv("MINIO_HOST")}{f":{os.getenv("MINIO_PORT")}" if os.getenv("MINIO_HOST") == 'localhost' else ''}/posts/{post_id}/{post.preview_image}'


        return post.model_dump()

    except Exception as e:

        raise Exception(e)