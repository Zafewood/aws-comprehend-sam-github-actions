import os
import json
import boto3

def handler(event, context):

    client = boto3.client('comprehend')
    body = event["body"]
    sentiment = client.detect_sentiment(LanguageCode = "en", Text = body)
    return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "sentiment": sentiment["Sentiment"],
                "sentimentScore": sentiment["SentimentScore"]
            })
    }
