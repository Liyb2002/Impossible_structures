"""
Generate Impossible Structure
"""
import json

import generate


def lambda_handler(event, context):
    # let params = event["queryStringParameters"]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "http://possibleimpossible.s3-website-us-east-1.amazonaws.com ",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
        "body": json.dumps("Hi Mom"),
    }
