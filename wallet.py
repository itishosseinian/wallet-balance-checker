import requests
import json
from datetime import datetime

def format_balance(balance):
    # Divide by 1,000,000 to get the decimal part
    balance_decimal = balance / 1000000.0
    
    # Format the decimal balance with commas for thousands separators and 6 decimal places
    formatted_balance = '{:,.6f}'.format(balance_decimal)
    
    return formatted_balance
    
def balance_checker_data(wallet_address):

    url = f"https://apilist.tronscanapi.com/api/search/v2?term={wallet_address}"
    
    payload={}

    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'User-Agent':'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/527.33 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.26',
        'Connection':'keep-alive',
        'Content-Type':'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text) 
    data = data['address'][0]

    info = {
        'address': data['address'],
        'date_created':datetime.fromtimestamp(data['date_created']).strftime('%Y-%m-%d'),
        'balance':format_balance(data['balance']),
        'total_transactions':'{:,}'.format(data['total_transactions']),
    }

    print(info)

def last_transaction(wallet_address):

    url = f"https://apilist.tronscanapi.com/api/transaction?sort=-timestamp&count=true&limit=20&start=0&address={wallet_address}"

    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'en-US,en;q=0.9',
        'User-Agent':'Mozilla/2.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers)

    parsed_data = json.loads(response.text)

    for transaction in parsed_data['data']:
        if 'amount' in transaction['contractData']:
            ticket = transaction['contractData']
            ticket['amount'] = ticket['amount'] /1000000.0
            print(ticket)

balance_checker_data('TPs3X9wZMU63oMmNGrSuXQN9E2aF4qtRch')
last_transaction('TPs3X9wZMU63oMmNGrSuXQN9E2aF4qtRch')

