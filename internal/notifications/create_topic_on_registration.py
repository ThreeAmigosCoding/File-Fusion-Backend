import boto3


def create_topic_on_registration(event, context):
    email = event['request']['userAttributes']['email']
    sanitized_email = email.replace('@', '').replace('.', '')

    sns = boto3.client('sns')

    response = sns.create_topic(
        Name=f'{sanitized_email}-notifications'
    )

    topic_arn = response['TopicArn']

    # Subscribe the user's email to the SNS topic
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )

    event['response']['autoConfirmUser'] = True
    event['response']['autoVerifyEmail'] = True
    return event
