import json
import re

from twig import twitter


def status(event, context):
    # Load status from API
    try:
        id = event["pathParameters"]["id"]
        status = twitter.status(id)
        status_code = 200
        body = json.dumps(status)
    except:
        status_code = 500
        body = json.dumps({"error": "Unspecified error"})

    # Check request origin and set CORS header accordingly
    headers = {}

    allowed_origins = ["^https?://localhost(:\d+)?$", "^https://wdrtwig.netlify.app$"]
    origin = event["headers"].get("origin")

    if not origin:
        cors_acao_value = None
    elif any(re.match(allowed_origin, origin) for allowed_origin in allowed_origins):
        cors_acao_value = origin
    else:
        cors_acao_value = None

    if cors_acao_value:
        headers["Access-Control-Allow-Origin"] = "*"
        headers["Access-Control-Allow-Credentials"] = True

    # Build response
    response = {
        "statusCode": status_code,
        "headers": headers,
        "body": body,
    }
    return response
