import base64
import json
import os
import traceback
import uuid

import boto3
from boto3.dynamodb.conditions import Attr

from internal.model.album import Album
from internal.model.my_response import my_response

albums_table_name = os.environ['ALBUMS_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(albums_table_name)


def create_album(event, context):
    try:
        email = event['pathParameters']['email']
        event['body'] = base64.b64decode(event['body'])

        body = json.loads(event['body'])
        name = body['name']
        owner = body['owner']
        deleted = False
        parent = body['parent']

        if name == "":
            return my_response(400, {"message": "Invalid name"})
        if owner == "" or owner != email:
            return my_response(400, {"message": "Invalid owner"})

        response = table.scan(
            FilterExpression=Attr('owner').eq(owner) & Attr('name').eq(name)
        )
        existing_albums = response['Items']

        if existing_albums:
            return my_response(400, {"message": "An album with the same name and owner already exists."})

        album = Album(
                id=str(uuid.uuid4()),
                name=name,
                owner=owner,
                deleted=deleted,
                parent=parent
            )

        table.put_item(Item=album.to_dict())

        return my_response(200, {"message": "Album created successfully"})

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
