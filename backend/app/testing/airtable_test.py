import requests

# Airtable Base and Table ID from your URL
base_id = ""  # Extracted Base ID
table_id = ""  # Extracted Table ID

# Your Airtable Personal Access Token
api_key = ""  # Replace with your Airtable API token

# Airtable API URL
url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

# Request headers with the Authorization Bearer token
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Send GET request to fetch records from the table
response = requests.get(url, headers=headers)

# Handle the response
if response.status_code == 200:
    records = response.json()
    print(f"Successfully fetched {len(records['records'])} records.")
    print(records)
else:
    print(f"Failed to fetch records. Error: {response.status_code} - {response.text}")
# ____________________________________________________________________________________



from pyairtable import Table

# Replace with your Airtable API URL, API Key, and Base ID
AIRTABLE_API_KEY = ''
BASE_ID = ''
TABLE_NAME = 'test'  # Use your table name

# Initialize Airtable client
table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# Define test data
test_data = [
    {"fields": {"First Name": "John", "Last Name": "Doe", "Email": "john.doe@example.com", "Phone": "1234567890", "Company": "Tech Corp"}},
    {"fields": {"First Name": "Jane", "Last Name": "Smith", "Email": "jane.smith@example.com", "Phone": "0987654321", "Company": "InnovateX"}},
    {"fields": {"First Name": "Alice", "Last Name": "Johnson", "Email": "alice.johnson@example.com", "Phone": "1122334455", "Company": "DataTech"}}
]

# Insert records into Airtable
for record in test_data:
    response = table.create(record)
    print(f"Record inserted: {response['id']}")
