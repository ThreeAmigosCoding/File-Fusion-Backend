import base64
import json
import os
import traceback
from decimal import Decimal

import boto3
import uuid
from datetime import datetime

from internal.model.multimedia_metadata import MultimediaMetadata
from internal.model.my_response import my_response

album_content_table_name = os.environ['ALBUM_CONTENT_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('multimedia_metadata')

album_content_table = dynamodb.Table(album_content_table_name)


def upload_file(event, context):
    try:

        username = event['pathParameters']['username']

        print("body", event['body'])

        event['body'] = base64.b64decode(event['body'])

        print(event['body'])

        body = json.loads(event['body'])
        base64_string = body['file']
        file_name = body['name']
        size_in_kb = Decimal(body['size'])  # size in KB
        file_extension = body['extension']
        album_id = body['albumId']

        file_content = base64.b64decode(base64_string)

        multimedia_id = str(uuid.uuid4())

        # Create a MultimediaMetadata object
        multimedia = MultimediaMetadata(
            id=multimedia_id,
            name=file_name,
            type=file_extension,
            size_in_kb=size_in_kb,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_changed=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            username=username,
            description=''
        )

        # Write the metadata to the DynamoDB table
        table.put_item(Item=multimedia.to_dict())

        if album_id != "":
            add_to_album(multimedia_id, album_id)

        # Upload the file to the S3 bucket
        s3 = boto3.client('s3')
        s3.put_object(
            Body=file_content,
            Bucket='multimedia-cloud-storage',  # replace with your bucket name
            Key=f'{username}/{file_name}'
        )

        return my_response(200, {"message": "File uploaded successfully"})
    except Exception as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})


def add_to_album(multimedia_id, album_id):
    album_content_table.put_item(Item={
        "id": str(uuid.uuid4()),
        "album": album_id,
        "file": multimedia_id
    })
