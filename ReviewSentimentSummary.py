import json
import anthropic
import os

def analyze_and_summarize_reviews(input_file, output_file, anthropic_api_key):
    # Initialize the Anthropic client
    # Replace it with:
    anthropic_client = anthropic.Anthropic(
        max_retries=5,
        timeout=20.0,
        api_key=anthropic_api_key
        )

    # Load the reviews from the JSON file
    with open('input_reviews.json', 'r') as file:
        reviews = json.load(file)

    # Iterate over each review
    for review in reviews:
        # Create a message for Claude to analyze the sentiment of the review body
        sentiment_message = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            temperature=0.0,
            messages=[
                {"role": "user", "content": f"What is the sentiment of this text, positive, neutral or negative (one word answer please): Title: '{review['title']}' Body: '{review['body']}'?"}
            ]
        )

        # Extract the sentiment from Claude's response
        sentiment = sentiment_message.content.__getitem__(0).text

        # Add the sentiment to the review
        review['review_sentiment'] = sentiment

        # Create a message for Claude to generate a summary of the review
        summary_message = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            temperature=0.0,
            messages=[
                {"role": "user", "content": f"Please summarize this review in a single sentence: Title: '{review['title']}' Body: '{review['body']}'"}
            ]
        )

        # Extract the summary from Claude's response
        summary = summary_message.content.__getitem__(0).text

        # Add the summary to the review
        review['review_summary'] = summary

    # Save the updated reviews back to the JSON file
    with open('input_reviews.json', 'w') as file:
        json.dump(reviews, file, indent=4)