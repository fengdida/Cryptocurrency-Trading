# Cryptocurrency-Trading
##A arbitrage strategy for the same products in different exchanges
The Strategy is to find the mismatch of the bid-ask of the same product in different exchange. As we can only make a immediately deal when we buy at the ask price and sell at the bid price, we need the bid price in one exchange greater than the ask price in another exchange.
The trading fee is about 0.1% for both exchanges, so the total trading cost for one pair including closing position is 0.4%
It's hard to get profit if we do not use leverage as the bid ask reversed spread should larger price*0.4%, so I added 10 leverage (the maximum in exchange).
Only leverage 10 can have enough reversed bid ask spread to trade

Further research:

Use multithreading to get the latest order book cocurrently
Trading cost including that the order we make may change the quantity of the bid-ask
risk management to capture abnormal move of the order book
REST api or Websocket
