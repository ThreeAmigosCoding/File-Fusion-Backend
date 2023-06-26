import os
import traceback

import boto3
from boto3.dynamodb.conditions import Attr

from internal.model.my_response import my_response

dynamodb = boto3.resource('dynamodb')

album_content_table_name = os.environ['ALBUM_CONTENT_TABLE']
album_content_table = dynamodb.Table(album_content_table_name)


def remove_content(event, context):
    try:
        album_id = event['pathParameters']['albumId']
        file_id = event['pathParameters']['fileId']

        item = album_content_table.scan(
            FilterExpression=Attr('album').eq(album_id) & Attr('file').eq(file_id)
        )
        if not item['Items']:
            return my_response(500, {"message": "No such table row."})

        album_content = item['Items'][0]

        album_content_table.delete_item(
            Key={
                'id': album_content['id']
            }
        )

        return my_response(200, {"message": "File successfully removed."})

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
