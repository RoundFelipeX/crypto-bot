from binance.client import Client
import time

API_KEY = 'N2b3utK7HwR4hOBInG65Sk7GThVgUJ1OKA1N7tSmEkMYG6MPa9ox5unhzDsZhE9g'
API_SECRET = '8TfQdeKxQJ5pjgOL0M0eYk8VdtgcKNM4aLRWrhx6mCq0U5yPX2qY33EmBPVczNRj'

client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

symbol = 'BTCUSDT'

while True:
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        price = ticker['price']
        print(f'Preço do BTC (Testnet): ${price}')
    except Exception as e:
        print(f'Erro ao buscar preço: {e}')
    
    time.sleep(10)  # espera 10 segundos
