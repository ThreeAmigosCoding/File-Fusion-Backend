import os
import traceback

import boto3
from boto3.dynamodb.conditions import Attr

from internal.model.album import Album
from internal.model.my_response import my_response

albums_table_name = os.environ['ALBUMS_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(albums_table_name)


def get_all_user_albums(event, context):
    try:
        email = event['pathParameters']['email']
        print("email", email)

        items = table.scan(
            FilterExpression=Attr('owner').eq(email) & Attr('deleted').eq(False)
        )
        print("items", items)
        albums_data = items['Items']
        print("albums_data", albums_data)
        albums = []

        for item in albums_data:
            album = Album(
                id=item['id'],
                name=item['name'],
                owner=item['owner'],
                deleted=bool(item['deleted']),
                parent=item['parent']
            )
            albums.append(album.to_dict())

        return my_response(200, albums)

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
