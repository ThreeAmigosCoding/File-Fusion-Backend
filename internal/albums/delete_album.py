import base64
import json
import os
import traceback

import boto3

from internal.model.my_response import my_response

albums_table_name = os.environ['ALBUMS_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(albums_table_name)


def delete_album(event, context):
    try:
        album_id = event['pathParameters']['albumId']
        update_expression = 'SET deleted = :val1'
        expression_attribute_values = {':val1': True}
        table.update_item(
            Key={"id": album_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        return my_response(200, {"message": "Album deleted successfully!"});

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
