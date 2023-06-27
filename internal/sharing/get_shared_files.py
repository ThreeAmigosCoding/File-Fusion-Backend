import os
import traceback
import boto3
from boto3.dynamodb.conditions import Attr

from internal.model.multimedia_metadata import MultimediaDisplay
from internal.model.my_response import my_response
from botocore.config import Config

share_table_name = os.environ['SHARE_TABLE_NAME']
multimedia_metadata_table_name = os.environ['MULTIMEDIA_METADATA_TABLE']
multimedia_bucket_name = os.environ['MULTIMEDIA_BUCKET']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(share_table_name)
multimedia_metadata_table = dynamodb.Table(multimedia_metadata_table_name)
s3 = boto3.client('s3', config=Config(signature_version='s3v4'))


def get_shared_files(event, context):
    try:
        email = event['pathParameters']['email']
        print(email)
        response = table.scan(
            FilterExpression=Attr('viewer').eq(email) & Attr('contentType').eq('file')
        )
        print(response)
        files_data = response['Items']
        files = []

        for data in files_data:
            response = multimedia_metadata_table.scan(
                FilterExpression=Attr('id').eq(data['contentId']) & Attr('deleted').ne(True)
            )
            if not response['Items']:
                continue
            file = response['Items'][0]
            print("file:", file)
            data_url = s3.generate_presigned_url('get_object',
                                                 Params={'Bucket': multimedia_bucket_name,
                                                         'Key': data['owner'] + "/" + file['name']},
                                                 ExpiresIn=86400)

            file_display = MultimediaDisplay(
                id=file['id'],
                name=file['name'],
                type=file['type'],
                size_in_kb=float(file['size_in_kb']),
                created_at=file['created_at'],
                last_changed=file['last_changed'],
                username=file['username'],
                description=file['description'],
                data_url=data_url
            )

            files.append(file_display.to_dict())
            print("files:", files)

        return my_response(200, files)

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})