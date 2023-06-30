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

    verify_ses_email(email)

    event['response']['autoConfirmUser'] = True
    event['response']['autoVerifyEmail'] = True
    return event


def verify_ses_email(email):
    ses_client = boto3.client('ses')  # Use your region
    email_to_verify = email
    response = ses_client.verify_email_identity(
        EmailAddress=email_to_verify,
    )
    return
