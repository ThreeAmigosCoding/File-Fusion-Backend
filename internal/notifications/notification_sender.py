import json
import boto3


def send_notification(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    event_name = event['Records'][0]['eventName']

    user_email = object_key.split('/')[0]
    object_name = object_key.split('/')[1].split(';')[1]

    message = f'{event_name} has occurred on {object_name} in {bucket_name}.'

    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=f'arn:aws:sns:eu-central-1:140063786275:{user_email}-notifications',
        Message=message,
        Subject=f'Bucket {event_name} Notification'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }
