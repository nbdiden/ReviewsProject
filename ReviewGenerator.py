import json
import random
from datetime import datetime, timedelta
import anthropic
import os


def load_input_reviews():
    with open('input_reviews.json', 'r') as f:
        return json.load(f)

def generate_review(product, brand, style, rating, anthropic_api_key, model="claude-3-opus-20240229"):

    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

    rating_sentiment = "Negative" if rating < 3 else "Neutral" if rating == 3 else "Positive"
    date = (datetime.now() - timedelta(days=random.randint(1,365))).strftime("Reviewed in the United States on %B %d, %Y")
    author = "Author" + str(random.randint(1,1000))
    
    input_reviews = load_input_reviews()
    similar_reviews = [review for review in input_reviews if abs(int(review['rating']) - rating) <= 1]
    system_prompt = json.dumps(similar_reviews, indent=4)
    
    # Generate title and body using Claude AI
    title_prompt = f"Generate a review title for a product with a rating of {rating}"
    title_message = anthropic_client.messages.create(
        model=model, 
        system=system_prompt,
        messages=[
            {"role": "user", "content": title_prompt}
        ], 
        max_tokens=10
    )
    
    title = title_message.content.__getitem__(0).text

    body_prompt = f"Generate a review body for a product with a rating of {rating}"
    body_message = anthropic_client.messages.create(
        model=model, 
        system=system_prompt,
        messages=[
            {"role": "user", "content": body_prompt}
        ], 
        max_tokens=200
    )

    body = body_message.content.__getitem__(0).text
    
    title_length = len(title)
    body_length = len(body)
    
    return {
        "object": "object_review",
        "id": str(random.randint(1,1000)),
        "product": product,
        "brand": brand,
        "rating": str(rating),
        "rating_sentiment": rating_sentiment,
        "style": style,
        "date": date,
        "author": author,
        "title_length": str(title_length),
        "title": title,
        "body_length": str(body_length),
        "body": body,
    }

def populate_json_file(product, brand, style, rating, num_reviews, output_file):
    reviews = [generate_review(product, brand, style, rating) for _ in range(num_reviews)]
    with open(output_file, 'w') as f:
        json.dump(reviews, f, indent=4)

# Example usage with a file, for standalone testing
if __name__ == '__main__':
    product = "Silver Infused Pillowcases"
    brand = "Silver Goose"
    style = "Black"
    rating = 4
    num_reviews = 4
    with open('output_reviews.json', 'w') as output_file:
        populate_json_file(product, brand, style, rating, num_reviews, output_file)