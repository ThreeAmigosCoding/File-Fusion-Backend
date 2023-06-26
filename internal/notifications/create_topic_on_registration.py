import boto3


def create_topic_on_registration(event, context):
    email = event['request']['userAttributes']['email']

    sns = boto3.client('sns')

    response = sns.create_topic(
        Name=f'{email}-notifications'
    )

    topic_arn = response['TopicArn']

    # Subscribe the user's email to the SNS topic
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
    return event
