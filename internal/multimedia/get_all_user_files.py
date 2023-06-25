import json
import boto3
from botocore.config import Config

from internal.model.my_response import my_response
from boto3.dynamodb.conditions import Attr
from internal.model.multimedia_metadata import MultimediaDisplay
import os
from decimal import Decimal

multimedia_metadata_table_name = os.environ['MULTIMEDIA_METADATA_TABLE']
multimedia_bucket_name = os.environ['MULTIMEDIA_BUCKET']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(multimedia_metadata_table_name)
s3 = boto3.client('s3', config=Config(signature_version='s3v4'))


def get_all_user_files(event, context):
    username = event['pathParameters']['username']

    items = table.scan(
        FilterExpression=Attr('username').eq(username)
    )
    user_files_metadata = items['Items']

    print(user_files_metadata)

    # paginator = s3.get_paginator('list_objects_v2')
    #     # user_files = paginator.paginate(Bucket=multimedia_bucket_name, Prefix=username)

    user_files = s3.list_objects_v2(Bucket=multimedia_bucket_name, Prefix=username)

    print(user_files)

    multimedia_display_items = construct_response(user_files_metadata, user_files)
    if not multimedia_display_items:
        return my_response(500, {"message": "Something failed during response construction"})

    return my_response(200, multimedia_display_items)


def construct_response(user_files_metadata, user_files):
    multimedia_display_items = []
    if 'Contents' not in user_files:
        return multimedia_display_items

    user_files_contents = user_files['Contents']
    for item in user_files_metadata:
        data_url = ""
        for user_files_content in user_files_contents:
            if item['name'] in user_files_content['Key']:
                data_url = s3.generate_presigned_url('get_object',
                                                     Params={'Bucket': multimedia_bucket_name,
                                                             'Key': user_files_content['Key']},
                                                     ExpiresIn=86400)
                break

        multimedia_display_item = MultimediaDisplay(
            id=item['id'],
            name=item['name'],
            type=item['type'],
            size_in_kb=float(item['size_in_kb']),
            created_at=item['created_at'],
            last_changed=item['last_changed'],
            username=item['username'],
            description=item['description'],
            data_url=data_url
        )

        multimedia_display_items.append(multimedia_display_item.to_dict())

    return multimedia_display_items
