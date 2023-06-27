import os
import traceback
import boto3
from boto3.dynamodb.conditions import Attr
from internal.model.my_response import my_response

share_table_name = os.environ['SHARE_TABLE_NAME']
albums_table_name = os.environ['ALBUMS_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(share_table_name)
albums_table = dynamodb.Table(albums_table_name)


def get_shared_albums(event, context):
    try:
        email = event['pathParameters']['email']

        response = table.scan(
            FilterExpression=Attr('viewer').eq(email) & Attr('contentType').eq('album')
        )
        albums_data = response['Items']
        albums = []

        for data in albums_data:
            response = albums_table.scan(
                FilterExpression=Attr('id').eq(data['contentId']) & Attr('deleted').eq(False)
            )
            if not response['Items']:
                continue
            albums.append(response['Items'][0])

        return my_response(200, albums)

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})