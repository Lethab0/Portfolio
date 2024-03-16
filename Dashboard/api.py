import requests

url1 = 'https://api.coingecko.com/api/v3/simple/price?ids=Ethereum&vs_currencies=zar'
url2 = 'https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=zar&days=1'

# Send request to the first URL
response1 = requests.get(url1)

# Check if the request was successful (status code 200)
if response1.status_code == 200:
    # Parse JSON response
    data1 = response1.json()
    # Extract the price of Ethereum in ZAR
    ethereum_price_zar = data1['ethereum']['zar']
    print(f'The price of Ethereum in ZAR is {ethereum_price_zar}')
else:
    print('Error:', response1.status_code)

# Send request to the second URL
response2 = requests.get(url2)

## Check if the request was successful (status code 200)
if response2.status_code == 200:
    # Parse JSON response
    data2 = response2.json()
    # Extract the last 10 prices from the response
    prices = data2['prices'][-10:]  # Get the last 10 prices
    print('Second number in each of the 10 price lists:')
    for price in prices:
        second_number = price[1]  # Access the second number in each price list
        print(second_number)
else:
    print('Error:', response2.status_code)


