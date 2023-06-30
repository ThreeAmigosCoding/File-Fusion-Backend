import os
import traceback
import uuid

import boto3
from boto3.dynamodb.conditions import Attr

from internal.model.my_response import my_response

dynamodb = boto3.resource('dynamodb')

album_content_table_name = os.environ['ALBUM_CONTENT_TABLE']
album_content_table = dynamodb.Table(album_content_table_name)


def add_to_album(event, context):
    try:
        album_id = event['pathParameters']['albumId']
        file_id = event['pathParameters']['fileId']

        response = album_content_table.scan(
            FilterExpression=Attr('file').eq(file_id) & Attr('album').eq(album_id)
        )

        if response['Items']:
            return my_response(400, {"message": "File is already in the album!"})

        album_content_table.put_item(Item={
            "id": str(uuid.uuid4()),
            "album": album_id,
            "file": file_id
        })

        return my_response(200, {"message": "File successfully added to album!"})

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})