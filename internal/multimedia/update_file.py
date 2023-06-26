
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


def update_file(event, context):
    try:
        metadata_id = event['pathParameters']['fileID']
        event['body'] = base64.b64decode(event['body'])

        response = table.get_item(
            Key={
                'id': metadata_id
            }
        )
        metadata_row = response['Item']
        old_file_name = metadata_row['name']
        created_at = metadata_row['created_at']

        body = json.loads(event['body'])
        base64_string = body['file']
        file_name = metadata_id + ";" + body['name']
        size_in_kb = Decimal(body['size'])
        description = body['description']
        username = body['username']
        file_extension = body['extension']

        # Create a MultimediaMetadata object
        multimedia = MultimediaMetadata(
            id=metadata_id,
            name=file_name,
            type=file_extension,
            size_in_kb=size_in_kb,
            created_at=created_at,
            last_changed=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            username=username,
            description=description
        )

        # Write the metadata to the DynamoDB table
        table.put_item(Item=multimedia.to_dict())

        # If there is no new file to be updated
        if old_file_name == file_name and base64_string == "":
            message = f'Update has occurred on {file_name} in {multimedia_metadata_table_name}.'
            sns = boto3.client('sns')
            response = sns.publish(
                TopicArn=f'arn:aws:sns:eu-central-1:140063786275:{username}-notifications',
                Message=message,
                Subject='Update Notification'
            )
            return my_response(200, {"message": "File updated successfully"})

        if old_file_name != file_name and base64_string == "":
            s3_copy = boto3.resource('s3')
            copy_source = {'Bucket': multimedia_bucket_name, 'Key': f'{username}/{old_file_name}'}
            s3_copy.meta.client.copy(copy_source, multimedia_bucket_name, f'{username}/{file_name}')
            s3_copy.Object(multimedia_bucket_name, f'{username}/{old_file_name}').delete()
            return my_response(200, {"message": "File updated successfully"})

        # If there is new file to be updated
        s3.delete_object(
            Bucket=multimedia_bucket_name, Key=f'{username}/{old_file_name}'
        )
        file_content = base64.b64decode(base64_string)
        s3.put_object(
            Body=file_content,
            Bucket=multimedia_bucket_name,  # replace with your bucket name
            Key=f'{username}/{file_name}'
        )
        return my_response(200, {"message": "File updated successfully"})
    except Exception as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})

