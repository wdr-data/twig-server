import json

from twig import twitter


def status(event, context):
    id = event["pathParameters"]["id"]
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(twitter.status(id)),
    }
    return response
