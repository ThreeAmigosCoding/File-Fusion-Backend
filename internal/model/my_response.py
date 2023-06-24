import json


def my_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            "Access-Control-Allow-Origin": "http://localhost:4200",
            "Access-Control-Allow-Headers": "Authorization",
            "Access-Control-Allow-Credentials": True
        }
    }

