import json
from ..models.createPost import create_post_model
import os
from dotenv import load_dotenv

load_dotenv()

def replace_image_name_to_url_in_post(post : create_post_model, post_id : str = ''):

    for image in list(filter(lambda block: block.type == 'image', post.post.content)):

        image.value = f'http://{os.getenv("MINIO_HOST")}{f":{os.getenv("MINIO_PORT")}" if os.getenv("MINIO_HOST") == 'localhost' else ''}/posts/{post_id}/{image.value}'

    return post.post.model_dump()