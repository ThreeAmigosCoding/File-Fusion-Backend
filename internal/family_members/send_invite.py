import boto3
from botocore.exceptions import ClientError
from internal.model.my_response import my_response
import traceback


def send_invite(event, context):
    ses_client = boto3.client('ses')  # Use your region

    sender = event['pathParameters']['inviterEmail']
    recipient = event['pathParameters']['invitedEmail']
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
