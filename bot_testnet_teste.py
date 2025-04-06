from binance.client import Client
import pandas as pd
import time
from datetime import datetime
# === CONFIGURAÇÕES INICIAIS ===
API_KEY = 'N2b3utK7HwR4hOBInG65Sk7GThVgUJ1OKA1N7tSmEkMYG6MPa9ox5unhzDsZhE9g'
API_SECRET = '8TfQdeKxQJ5pjgOL0M0eYk8VdtgcKNM4aLRWrhx6mCq0U5yPX2qY33EmBPVczNRj'

client = Client(API_KEY, API_SECRET)

# === FUNÇÃO PARA COLETAR DADOS HISTÓRICOS ===
def get_historical_data(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_4H, limit=100):
    candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[['timestamp', 'close']]

# === FUNÇÃO PARA CALCULAR MÉDIAS MÓVEIS ===
def apply_moving_averages(df):
    df['MA9'] = df['close'].rolling(window=9).mean()
    df['MA21'] = df['close'].rolling(window=21).mean()
    return df

# === FUNÇÃO PARA IDENTIFICAR O SINAL ===
def check_for_signal(df):
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    if prev_row['MA9'] < prev_row['MA21'] and last_row['MA9'] > last_row['MA21']:
        return "COMPRA"
    elif prev_row['MA9'] > prev_row['MA21'] and last_row['MA9'] < last_row['MA21']:
        return "VENDA"
    else:
        return "MANTER"

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    print("Bot de Análise de Tendência Iniciado...")
    df = get_historical_data()
    df = apply_moving_averages(df)
    sinal = check_for_signal(df)
    print(f"Sinal atual: {sinal}")