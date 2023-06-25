from internal.model.my_response import my_response
import base64
import json
import traceback
from decimal import Decimal
import boto3
from datetime import datetime
from internal.model.multimedia_metadata import MultimediaMetadata
import os

multimedia_metadata_table_name = os.environ['MULTIMEDIA_METADATA_TABLE']
multimedia_bucket_name = os.environ['MULTIMEDIA_BUCKET']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(multimedia_metadata_table_name)
s3 = boto3.client('s3')


def delete_file(event, context):
    metadata_id = event['pathParameters']['fileID']

    update_expression = 'SET deleted = :val1'
    expression_attribute_values = {':val1': True}
    table.update_item(
        Key={"id": metadata_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    updated_item = table.get_item(Key={'id': metadata_id})['Item']
    file_name = updated_item['name']
    username = updated_item['username']
    s3.delete_object(
        Bucket=multimedia_bucket_name, Key=f'{username}/{file_name}'
    )

    return my_response(200, {"message": "Item deleted successfully!"})
