import csv
import json
from io import StringIO

def convert_csv_to_json(file_stream):
    # Convert bytes data to string
    file_stream.seek(0)  # Go to the start of the file-like object
    string_data = file_stream.read().decode('utf-8')  # Decode bytes to string

    # Convert string data to StringIO
    csv_file = StringIO(string_data)

    # Read CSV and convert to JSON
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

    # Convert to JSON string
    json_str = json.dumps(data, indent=4)

    return json_str