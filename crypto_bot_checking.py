'''
exchange checking price bot
'''


import ccxt

# Set the exchange and the symbol
exchange = ccxt.binance()
symbol = "BTC/USDT"

# Set the authentication credentials
exchange.apiKey = "your_api_key"
exchange.secret = "your_api_secret"

# Load the order book
order_book = exchange.fetch_order_book(symbol)

# Calculate the bid and ask prices
bid_price = order_book['bids'][0][0] if len(order_book['bids']) > 0 else None
ask_price = order_book['asks'][0][0] if len(order_book['asks']) > 0 else None

# Print the bid and ask prices
print(f"Bid price: {bid_price}")
print(f"Ask price: {ask_price}")
