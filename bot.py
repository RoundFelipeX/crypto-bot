from binance.client import Client
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

last_signal = 'WAIT'

def obter_dados():
    candles = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=100)
    closes = [float(candle[4]) for candle in candles]
    timestamps = [int(candle[0]) for candle in candles]
    return closes, timestamps

def calcular_sma(valores, periodo):
    if len(valores) < periodo:
        return None
    return sum(valores[-periodo:]) / periodo

def analisar_tendencia(closes):
    sma9_antes = calcular_sma(closes[:-1], 9)
    sma21_antes = calcular_sma(closes[:-1], 21)
    sma9_agora = calcular_sma(closes, 9)
    sma21_agora = calcular_sma(closes, 21)

    if sma9_antes and sma21_antes:
        if sma9_antes < sma21_antes and sma9_agora > sma21_agora:
            return 'BUY'
        elif sma9_antes > sma21_antes and sma9_agora < sma21_agora:
            return 'SELL'
    return 'WAIT'

def registrar_sinal(sinal, preco):
    try:
        with open('sinais.csv', 'a') as f:
            f.write(f"{datetime.now()},{sinal},{preco}\n")
    except Exception as e:
        print("Erro ao registrar sinal:", e)

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
            closes, timestamps = obter_dados()
            preco_atual = closes[-1]
            sinal = analisar_tendencia(closes)

            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sinal: {sinal} | Preço BTC: ${preco_atual:.2f}")
            print("-" * 50)

            if sinal != last_signal and sinal != 'WAIT':
                executar_ordem(sinal)
                registrar_sinal(sinal, preco_atual)
                last_signal = sinal

        except Exception as e:
            print("Erro no bot:", e)

        time.sleep(15)

if __name__ == "__main__":
    executar_bot()
