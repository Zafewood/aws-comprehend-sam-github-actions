import os
import json
import boto3

def handler(event, context):

    client = boto3.client('comprehend')
    request = json.loads(event.get("body") or "{}")
    text = request.get("text", "").strip()

    if not text:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "text is required"})
        }

    sentiment = client.detect_sentiment(LanguageCode="en", Text=text)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "sentiment": sentiment["Sentiment"],
            "sentimentScore": sentiment["SentimentScore"]
        })
    }
