from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('ratings_reviews_analysis.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/start-analysis', methods=['POST'])
def start_analysis():
    data = request.json
    brand = data['brand']
    product = data['product']
    averageRating = data['averageRating']
    totalRatings = data['totalRatings']
    ratingDistribution = data['ratingDistribution']
    # Process the data as needed for your application
    return jsonify({"message": "Analysis started"}), 200