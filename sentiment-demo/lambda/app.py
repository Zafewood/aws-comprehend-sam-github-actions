import json
import boto3

SENTIMENT_LANGUAGES = {
    "ar", "de", "en", "es", "fr", "hi", "it", "ja", "ko", "pt", "zh", "zh-TW", "tr"
}

def handler(event, context):

    client = boto3.client('comprehend')
    try:
        request = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        request = {}
    text = request.get("text", "").strip()

    if not text:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "https://legendary-rotary-phone-jq5prg6ggpw359x9-8000.app.github.dev"
            },
            "body": json.dumps({"error": "text is required"})
        }

    language = client.detect_dominant_language(Text=text)["Languages"][0]
    language_code = language["LanguageCode"]
    sentiment = None
    if language_code in SENTIMENT_LANGUAGES:
        sentiment = client.detect_sentiment(LanguageCode=language_code, Text=text)
    toxicity = {
        "supported": language_code == "en",
        "isToxic": False,
        "score": None,
        "labels": []
    }

    if toxicity["supported"]:
        toxicity_result = client.detect_toxic_content(
            TextSegments=[{"Text": text}],
            LanguageCode="en"
        )["ResultList"][0]
        toxicity["score"] = toxicity_result["Toxicity"]
        toxicity["isToxic"] = toxicity["score"] >= 0.5
        toxicity["labels"] = toxicity_result.get("Labels", [])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://legendary-rotary-phone-jq5prg6ggpw359x9-8000.app.github.dev"
        },
        "body": json.dumps({
            "language": language,
            "sentiment": sentiment["Sentiment"] if sentiment else None,
            "sentimentScore": sentiment["SentimentScore"] if sentiment else None,
            "toxicity": toxicity
        })
    }
