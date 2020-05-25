from .twitter import status


def status(event, context):
    id = event["pathParameters"]["id"]
    response = {"statusCode": 200, "body": json.dumps(status(id))}
    return response
