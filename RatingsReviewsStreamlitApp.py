import streamlit as st
from RatingDistributionCalculator import calculate_rating_distribution
from ReviewGenerator import populate_json_file
from CSVtoJSONConverter import convert_csv_to_json  # Import the convert function
from ReviewSentimentSummary import analyze_and_summarize_reviews
from anthropic import Anthropic
import json  # Import json for handling JSON data
import os

# Title and Description
st.title('Ratings & Reviews Analysis')
st.write('Comprehensive insights into ratings and reviews for informed decision-making.')

# Brand Input
brand = st.text_input('Brand', placeholder="Enter Brand Name")

# Product Input
product = st.text_input('Product', placeholder="Enter Product Name")

# Collect additional inputs for review generation
num_reviews = st.number_input('Number of Reviews to Generate', min_value=1, max_value=10000, value=5)

rating = st.slider('Rating for Generated Reviews', min_value=1, max_value=5, step=0.1)

# Path for temporary output file
output_file_path = 'generated_reviews.json'

# Rating Distribution Inputs
st.subheader('Rating Distribution')
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    dist_1_upper = st.text_input('5 Stars Upper Bound', key='5_upper')
    dist_1_lower = st.text_input('5 Stars Lower Bound', key='5_lower')
with col2:
    dist_2_upper = st.text_input('4 Stars Upper Bound', key='4_upper')
    dist_2_lower = st.text_input('4 Stars Lower Bound', key='4_lower')
with col3:
    dist_3_upper = st.text_input('3 Stars Upper Bound', key='3_upper')
    dist_3_lower = st.text_input('3 Stars Lower Bound', key='3_lower')
with col4:
    dist_4_upper = st.text_input('2 Stars Upper Bound', key='2_upper')
    dist_4_lower = st.text_input('2 Stars Lower Bound', key='2_lower')
with col5:
    dist_5_upper = st.text_input('1 Star Upper Bound', key='1_upper')
    dist_5_lower = st.text_input('1 Star Lower Bound', key='1_lower')

# Convert bounds input from user into a list of tuples
def parse_bounds_input(upper_bounds, lower_bounds):
    bounds = []
    for ub, lb in zip(upper_bounds, lower_bounds):
        try:
            bounds.append((float(lb), float(ub)))
        except ValueError:  # In case of conversion error
            st.error("Please enter valid numeric bounds")
            return None
    return bounds

# Collect bounds input from the user
upper_bounds = [dist_5_upper, dist_4_upper, dist_3_upper, dist_2_upper, dist_1_upper]
lower_bounds = [dist_5_lower, dist_4_lower, dist_3_lower, dist_2_lower, dist_1_lower]
bounds = parse_bounds_input(upper_bounds, lower_bounds)

if bounds and st.button('Calculate Distribution'):
    # Call the distribution calculation function
    distribution = calculate_rating_distribution(rating, num_reviews, bounds)
    # Display the calculated distribution
    for i, count in enumerate(distribution, 1):
        st.write(f"{i} star: {count}")
        
st.subheader('Settings')
passkey = st.text_input('Passkey', type='password')

# File Uploader
uploaded_file = st.file_uploader("Upload Reviews (CSV)", type=['csv'])

# Process uploaded file
if uploaded_file is not None:
    # Convert CSV file to JSON
    json_data = convert_csv_to_json(uploaded_file)

    with open('input_reviews.json', 'w') as json_file:
        json_file.write(json_data)

    # New Step: Call analyze_and_summarize_reviews
    analyze_and_summarize_reviews('input_reviews.json', 'updated_input_reviews.json')

# Start Analysis Button
if st.button('Generate Reviews'):
    # Call the function to populate the JSON file with generated reviews
    populate_json_file(product, brand, "Default Style", rating, num_reviews, output_file_path)

    # Read and display the generated reviews or offer download
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r') as file:
            generated_reviews = json.load(file)
            st.json(generated_reviews)  # Display the reviews in the app
        
        # Alternatively, offer the file for download
        with open(output_file_path, 'rb') as file:
            st.download_button(
                label="Download Generated Reviews",
                data=file,
                file_name="generated_reviews.json",
                mime="application/json"
            )

        # Clean up: Delete the temporary file after displaying/offering download
        os.remove(output_file_path)

# Note: You need to implement the backend logic for processing the inputs and conducting the analysis.