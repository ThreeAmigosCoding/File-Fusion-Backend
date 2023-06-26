import os
import traceback

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config

from internal.model.multimedia_metadata import MultimediaMetadata, MultimediaDisplay
from internal.model.my_response import my_response

multimedia_metadata_table_name = os.environ['MULTIMEDIA_METADATA_TABLE']
multimedia_bucket_name = os.environ['MULTIMEDIA_BUCKET']
albums_table_name = os.environ['ALBUMS_TABLE']
album_content_table_name = os.environ['ALBUM_CONTENT_TABLE']

dynamodb = boto3.resource('dynamodb')
multimedia_metadata_table_name = dynamodb.Table(multimedia_metadata_table_name)
s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

albums_table = dynamodb.Table(albums_table_name)
album_content_table = dynamodb.Table(album_content_table_name)


def get_album_content(event, context):
    try:
        email = event['pathParameters']['email']
        album_id = event['pathParameters']['albumId']

        items = album_content_table.scan(
            FilterExpression=Attr('album').eq(album_id)
        )
        album_contents = items['Items']
        print("album_contents:", album_contents)
        multimedia_display_items = []

        for album_content in album_contents:
            item = multimedia_metadata_table_name.scan(
                FilterExpression=Attr('id').eq(album_content['file']) & Attr('deleted').ne(True)
            )
            multimedia_item = item['Items'][0]
            print("multimedia_item:", multimedia_item)
            data_url = s3.generate_presigned_url('get_object',
                                                 Params={'Bucket': multimedia_bucket_name,
                                                         'Key': email + "/" + multimedia_item['name']},
                                                 ExpiresIn=86400)

            print("data_url:", data_url)

            multimedia_display_item = MultimediaDisplay(
                id=multimedia_item['id'],
                name=multimedia_item['name'],
                type=multimedia_item['type'],
                size_in_kb=float(multimedia_item['size_in_kb']),
                created_at=multimedia_item['created_at'],
                last_changed=multimedia_item['last_changed'],
                username=multimedia_item['username'],
                description=multimedia_item['description'],
                data_url=data_url
            )

            multimedia_display_items.append(multimedia_display_item.to_dict())

            print("multimedia_display_items:", multimedia_display_items)

        return my_response(200, multimedia_display_items)

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
