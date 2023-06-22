import boto3
import json
import base64
from botocore.exceptions import ClientError

from internal.model.multimedia_metadata import MultimediaMetadata

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('multimedia_metadata')


def upload_file(event, context):
    try:
        data = event['body']
        multimedia = MultimediaMetadata(**data)

        try:
            table.put_item(Item=multimedia.dict())
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps(str(e))
            }

        # region S3 Bucket
        s3 = boto3.client('s3')

        try:
            # Convert the base64 encoded data to bytes
            file_data = base64.b64decode(data['file_data'])

            # Upload the file to S3
            s3.put_object(
                Body=file_data,
                Bucket='multimedia-cloud-storage',  # replace with your bucket name
                Key=multimedia.username + '/' + multimedia.name
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps(str(e))
            }
        # endregion

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File uploaded successfully'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }