import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from internal.model.my_response import my_response
import traceback

client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_YIWsc8z0P'

family_member_table_name = "family_member_invitation"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(family_member_table_name)


def send_invite(event, context):
    ses_client = boto3.client('ses')  # Use your region

    sender = event['pathParameters']['inviterEmail']
    recipient = event['pathParameters']['invitedEmail']
    if not check_for_invitation(recipient):
        return my_response(400, {"message": "Cannot invite, user already exists!"})
    subject = "File Fusion cloud platform invitation"
    body_text = f"{sender} invited you to join File Fusion cloud platform!"
    body_html = f"""<h2> {sender} invited you to join File fusion platform </h2> 
                <br> <a href='http://localhost:4200/regiserAsMember/{sender}/{recipient}'>Join!</a> """
    charset = "UTF-8"

    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )

        return my_response(200, {"message": f"User {recipient} was invited to join File Fusion platform!"})
    except ClientError as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})


def check_for_invitation(recipient):
    try:
        client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=recipient
        )
        return False
    except ClientError:
        pass

    response = table.scan(
        FilterExpression=Attr('email').eq(recipient) & Attr('status').ne('declined')
    )
    items = response['Items']
    if len(items) > 0:
        return False

    return True

