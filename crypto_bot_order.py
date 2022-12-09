# Import the Binance Python library
from binance.client import Client

# Create a Binance client using your API key and secret
client = Client("API_KEY", "API_SECRET")

# Define the parameters for your bot
symbol = "BTCUSDT" # The symbol for the market you want to trade on
quantity = 1 # The amount of the asset you want to buy or sell
price = 10000 # The price at which you want to buy or sell

# Place an order to buy or sell the asset
order = client.order_limit_buy(
  symbol=symbol,
  quantity=quantity,
  price=price
)

# Print the details of the order
print(order)
