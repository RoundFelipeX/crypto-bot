from binance.client import Client
import pandas as pd
import time
from datetime import datetime

# Chaves da Testnet
API_KEY = 'N2b3utK7HwR4hOBInG65Sk7GThVgUJ1OKA1N7tSmEkMYG6MPa9ox5unhzDsZhE9g'
API_SECRET = '8TfQdeKxQJ5pjgOL0M0eYk8VdtgcKNM4aLRWrhx6mCq0U5yPX2qY33EmBPVczNRj'

# Conexão com a Binance Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

SYMBOL = 'BTCUSDT'
INTERVAL = Client.KLINE_INTERVAL_5MINUTE
QTD_BTC = 0.001  # valor fictício para teste

last_signal = 'WAIT'  # Guarda o último sinal

def obter_dados():
    candles = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=100)
    df = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    df.set_index('timestamp', inplace=True)
    return df[['close']]

def analisar_tendencia(df):
    df['SMA9'] = df['close'].rolling(window=9).mean()
    df['SMA21'] = df['close'].rolling(window=21).mean()

    if df['SMA9'].iloc[-2] < df['SMA21'].iloc[-2] and df['SMA9'].iloc[-1] > df['SMA21'].iloc[-1]:
        return 'BUY'
    elif df['SMA9'].iloc[-2] > df['SMA21'].iloc[-2] and df['SMA9'].iloc[-1] < df['SMA21'].iloc[-1]:
        return 'SELL'
    else:
        return 'WAIT'

def registrar_sinal(sinal, preco):
    with open('sinais.csv', 'a') as f:
        f.write(f"{datetime.now()},{sinal},{preco}\n")

def executar_ordem(sinal):
    try:
        if sinal == 'BUY':
            ordem = client.order_market_buy(symbol=SYMBOL, quantity=QTD_BTC)
            print("✅ ORDEM DE COMPRA ENVIADA (SIMULADA):", ordem['executedQty'], "BTC")
        elif sinal == 'SELL':
            ordem = client.order_market_sell(symbol=SYMBOL, quantity=QTD_BTC)
            print("✅ ORDEM DE VENDA ENVIADA (SIMULADA):", ordem['executedQty'], "BTC")
    except Exception as e:
        print("⚠️ Erro ao enviar ordem simulada:", e)

def executar_bot():
    global last_signal
    while True:
        try:
            df = obter_dados()
            sinal = analisar_tendencia(df)
            preco_atual = df['close'].iloc[-1]

            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sinal: {sinal} | Preço BTC: ${preco_atual:.2f}")
            print("-" * 50)

            if sinal != last_signal and sinal != 'WAIT':
                executar_ordem(sinal)
                registrar_sinal(sinal, preco_atual)
                last_signal = sinal

        except Exception as e:
            print("Erro no bot:", e)

        # Aguarda 15 segundos
        time.sleep(15)

if __name__ == "__main__":
    executar_bot()
