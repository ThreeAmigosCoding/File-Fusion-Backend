import os
import traceback

import boto3
from boto3.dynamodb.conditions import Attr

from internal.model.my_response import my_response

dynamodb = boto3.resource('dynamodb')

album_content_table_name = os.environ['ALBUM_CONTENT_TABLE']
albums_table_name = os.environ['ALBUMS_TABLE']

albums_table = dynamodb.Table(albums_table_name)
album_content_table = dynamodb.Table(album_content_table_name)


def get_available_albums(event, context):
    try:
        file_id = event['pathParameters']['fileId']

        # Get all albums which include the file
        response = album_content_table.scan(
            FilterExpression=Attr('file').eq(file_id)
        )

        included_albums = []
        for album_content in response['Items']:
            included_albums.append(album_content['album'])

        # Get all albums
        response = albums_table.scan(
            FilterExpression=Attr('deleted').eq(False)
        )

        not_included_albums = []
        for album in response['Items']:
            if album['id'] not in included_albums:
                not_included_albums.append(album)

        return my_response(200, not_included_albums)

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
