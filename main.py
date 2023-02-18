from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up Google Analytics API credentials
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '/path/to/your/key/file.json' # replace with your own key file location
VIEW_ID = 'YOUR_VIEW_ID' # replace with your own view ID

credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE_LOCATION, scopes=SCOPES)

# Connect to the Google Analytics API
analytics = build('analyticsreporting', 'v4', credentials=credentials)

# Query for transaction data
query = {
    'viewId': VIEW_ID,
    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
    'metrics': [{'expression': 'ga:transactionRevenue'}],
    'dimensions': [{'name': 'ga:dimension1'}, {'name': 'ga:productName'}],
    'filtersExpression': 'ga:transactions>0'
}

# Retrieve and process the data
try:
    response = analytics.reports().batchGet(body={'reportRequests': [query]}).execute()
    data = response['reports'][0]['data']['rows']
    customer_revenue = {}
    for row in data:
        customer_id = row['dimensions'][0]
        product_revenue = float(row['metrics'][0]['values'][0])
        if customer_id not in customer_revenue:
            customer_revenue[customer_id] = 0
        customer_revenue[customer_id] += product_revenue
    top_customers = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)[:10]
    print('Top 10 customers by revenue:')
    for customer in top_customers:
        print(f'{customer[0]}: ${customer[1]:.2f}')
except HttpError as error:
    print(f'Report request failed: {error}')
