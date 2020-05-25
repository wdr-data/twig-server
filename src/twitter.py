import os
import json
import urllib.parse
from base64 import b64encode

import boto3
import requests

dynamodb = boto3.resource("dynamodb")


def refresh_bearer():
    print("Refreshing bearer...")
    auth = {
        "key": urllib.parse.quote(os.environ["TWITTER_KEY"]),
        "secret": urllib.parse.quote(os.environ["TWITTER_SECRET"]),
    }
    auth_encoded = b64encode(bytes(f"{auth['key']}:{auth['secret']}", "ascii"))

    response = requests.post(
        url="https://api.twitter.com/oauth2/token",
        headers={"Authorization": f"Basic {auth_encoded.decode('ascii')}",},
        data={"grant_type": "client_credentials",},
    )

    data = response.json()
    bearer = data["access_token"]

    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])
    table.put_item(Item={"name": "bearer", "value": bearer})

    return bearer


def get_bearer():
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    try:
        bearer = table.get_item(Key={"name": "bearer"})["Item"]["value"]
    except:
        print("Refreshing bearer on first run")
        bearer = refresh_bearer()

    return bearer


def status(id):
    def api_call(bearer):
        return requests.get(
            "https://api.twitter.com/1.1/statuses/show.json",
            params={"id": id,},
            headers={"Authorization": f"Bearer {bearer}"},
        )

    bearer = get_bearer()
    try:
        response = api_call(bearer)
        assert bool(response)
    except:
        bearer = refresh_bearer()
        response = api_call(bearer)
        assert bool(response)

    return response.json()


if __name__ == "__main__":
    print(status("1264239670973673474"))
