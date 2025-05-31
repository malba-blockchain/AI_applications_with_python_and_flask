"""
Sentiment Analysis Module

This module provides functionality to analyze the sentiment of text using
Watson NLP sentiment analysis service.
"""
import json
import requests


def sentiment_analyzer(text_to_analyse):
    """
    Analyze the sentiment of the given text using Watson NLP service.
    
    Args:
        text_to_analyse (str): The text to analyze for sentiment
        
    Returns:
        dict: A dictionary containing 'label' and 'score' keys with sentiment results
    """
    url = ('https://sn-watson-sentiment-bert.labs.skills.network/v1/'
           'watson.runtime.nlp.v1/NlpService/SentimentPredict')
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=myobj, headers=header, timeout=30)
    formatted_response = json.loads(response.text)

    # Initialize variables to avoid possible undefined usage
    label = None
    score = None

    if response.status_code == 200:
        label = formatted_response['documentSentiment']['label']
        score = formatted_response['documentSentiment']['score']
    elif response.status_code == 500:
        label = None
        score = None
    return {'label': label, 'score': score}
    