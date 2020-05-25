import json

from twig import twitter


def status(event, context):
    id = event["pathParameters"]["id"]
    response = {"statusCode": 200, "body": json.dumps(twitter.status(id))}
    return response
