from huobi.client.market import MarketClient
from huobi.utils import *
from kucoin.client import Market
import time

#times: trading times 
#rates: fee rates
#symbol: the product, must be the same product
#leverage: leverage level

def Pnl(times=10,rates=[0.001,0.001],symbol=['btcusdt','BTC-USDT'],leverage=10):
    client_h = MarketClient()
    symbol_h, symbol_k = symbol
    depth_size = 1

    client_k = Market(url='https://api.kucoin.com')
    account_h=[0,0]
    account_k=[0,0]
    profit=0
    fees=0
    fee_h, fee_k=rates #kucoin: 0.1%, huobi: 0.1%
    market_price=client_h.get_market_detail(symbol_h).close
    spread=(fee_h+fee_k)*2*market_price/leverage
    #trade 10 times(default)
    while times:
        order_h = client_h.get_pricedepth(symbol_h, 'step0', depth_size)
        order_k = client_k.get_part_order(20,symbol_k)
    
        price_h_a, amount_h_a = order_h.asks[0].price, order_h.asks[0].amount
        price_h_b, amount_h_b = order_h.bids[0].price, order_h.bids[0].amount
    
        price_k_a, amount_k_a = float(order_k['bids'][0][0]), float(order_k['bids'][0][1])
        price_k_b, amount_k_b = float(order_k['asks'][0][0]), float(order_k['asks'][0][1])


        if price_h_a <= (price_k_b-spread):
            min_a=min(amount_h_a, amount_k_b)
            print("Huobi buy: ",price_h_a)
            print("Kucoin sell: ",price_k_b)
            print("Amount: ",min_a)
            account_h[0]+=price_h_a*min_a
            account_h[1]+=min_a
            account_k[0]-=price_k_b*min_a
            account_k[1]-=min_a
            fees+=price_h_a*min_a*fee_h+price_k_b*min_a*fee_k
            times-=1
        elif (price_h_b-spread) >= price_k_a:
            min_a=min(amount_k_a, amount_h_b)
            print("Kucoin buy: ",price_k_a)
            print("Huobi sell: ",price_h_b)
            print("Amount: ",min_a)
            account_h[0]-=price_h_b*min_a
            account_h[1]-=min_a
            account_k[0]+=price_k_a*min_a
            account_k[1]+=min_a
            fees+=price_h_b*min_a*fee_h+price_k_a*min_a*fee_k
            times-=1
        time.sleep(0.01)
    #close position when the bid-ask between 2 exchanges return normal
    while True:
        order_h = client_h.get_pricedepth(symbol_h, 'step0', depth_size)
        order_k = client_k.get_part_order(20,symbol_k)
    
        price_h_a, amount_h_a = order_h.asks[0].price, order_h.asks[0].amount
        price_h_b, amount_h_b = order_h.bids[0].price, order_h.bids[0].amount
    
        price_k_a, amount_k_a = float(order_k['bids'][0][0]), float(order_k['bids'][0][1])
        price_k_b, amount_k_b = float(order_k['asks'][0][0]), float(order_k['asks'][0][1])
        if price_k_a>=price_h_b and price_k_b<=price_h_a: #when normal: both bid < ask 
            if account_h[1]>0:
                close_price=price_h_b
                profit+=close_price*account_h[1]-account_h[0]
                fees+=close_price*abs(account_h[1])*fee_h
            else:
                close_price=price_h_a
                profit+=close_price*account_h[1]-account_h[0]
                fees+=close_price*abs(account_h[1])*fee_h
            if account_k[1]>0:
                close_price=price_k_b
                profit+=close_price*account_k[1]-account_k[0]
                fees+=close_price*abs(account_k[1])*fee_k
            else:
                close_price=price_k_a
                profit+=close_price*account_k[1]-account_k[0]
                fees+=close_price*abs(account_k[1])*fee_k
            break
        time.sleep(0.01)
    return [profit*leverage, fees]
rst=Pnl() #BTC USDT
print(f"Total profit: {rst[0]}, total trading cost: {rst[1]}, netting: {rst[0]-rst[1]}")