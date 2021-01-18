from Controller.controller import Controller as ctrl


def main():
    Controller = ctrl()
    try: 
        new_order = Controller.broker.binance_client.order_limit_buy(symbol="BNBBTC",quantity=1,price=0.0012)
    except:
        print("No Balance")
    all_prices = Controller.broker.getAllTickers()
    all_assets = Controller.broker.getTotalBalances()
    total_usd_value = Controller.broker.getTotalUsdValue()

    pass


if __name__ == '__main__':
    main()

