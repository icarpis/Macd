import pandas as pd
import yfinance as yf
import numpy as np
import pytz
from datetime import datetime as dt
import sys
import io
import plotly.graph_objs as go
import datetime

    

  
def main():
    try:
        # Load stock data
        STOCK_NAME = sys.argv[1]
        print("Stock Name: " + STOCK_NAME + "<br>")
        stock_ticker = STOCK_NAME
        
        START_DATE = sys.argv[2].split("_")
        START_YEAR = int(START_DATE[0])
        START_MONTH = int(START_DATE[1])
        START_DAY = int(START_DATE[2])
        
        END_DATE = sys.argv[3].split("_")
        END_YEAR = int(END_DATE[0])
        END_MONTH = int(END_DATE[1])
        END_DAY = int(END_DATE[2])
        
        tz = pytz.timezone("Israel")
        start_date = tz.localize(dt(START_YEAR,START_MONTH, START_DAY))
        end_date = tz.localize(dt(END_YEAR,END_MONTH, END_DAY) + datetime.timedelta(days=1))
        stock_data = yf.download(stock_ticker, start=start_date, end=end_date)

        # Calculate MACD indicator
        def MACD(df, a, b, c):
            df["EMA_12"] = df["Close"].ewm(span=a, min_periods=a).mean()
            df["EMA_26"] = df["Close"].ewm(span=b, min_periods=b).mean()
            df["MACD"] = df["EMA_12"] - df["EMA_26"]
            df["Signal"] = df["MACD"].ewm(span=c, min_periods=c).mean()
            df["Histogram"] = df["MACD"] - df["Signal"]
            return df

        df = MACD(stock_data, 12, 26, 9)


        # Buy and sell signals
        df["Buy"] = (df["MACD"] > df["Signal"]) & (df["MACD"].shift() < df["Signal"].shift())
        df["Sell"] = (df["MACD"] < df["Signal"]) & (df["MACD"].shift() > df["Signal"].shift())


        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        hist = macd - signal

        # Create figure
        fig = go.Figure()

        # Add trace for stock price
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Stock Price"))

        # Add trace for MACD
        fig.add_trace(go.Scatter(x=df.index, y=macd, name="MACD"))

        # Add trace for signal
        fig.add_trace(go.Scatter(x=df.index, y=signal, name="Signal"))

        # Add trace for histogram
        fig.add_trace(go.Bar(x=df.index, y=hist, name="Histogram"))

        # Add buy and sell signals
        buy_signals = df[(macd > signal) & (macd.shift() < signal.shift())]
        sell_signals = df[(macd < signal) & (macd.shift() > signal.shift())]

        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals["Close"], mode="markers", marker=dict(symbol="triangle-up", size=10, color="green"), name="Buy"))
        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals["Close"], mode="markers", marker=dict(symbol="triangle-down", size=10, color="red"), name="Sell"))


        # Print buy and sell signals
        print("<br>Buy signals:<br>")
        print(df[df["Buy"]]["Close"])
        print("<br><br>Sell signals:<br>")
        print(df[df["Sell"]]["Close"])

        df["Date"] = df.index

        first_investment = 100

        dates_list = []
        cash_list = []
        cash_list.append(first_investment)
        dates_list.append(df["Date"][0])


        last_sell_cash = None
        success_rate = 0
        num_of_sells = 0

        cash = first_investment  # start with first_investment in cash
        shares = 0
        for i in range(len(df)):
            if df["Buy"][i] == True:
                shares_to_buy = cash / df["Close"][i]  # calculate number of shares to buy
                shares += shares_to_buy  # add shares to portfolio
                cash = 0
                #dates_list.append(df["Date"][i])
            elif df["Sell"][i] == True:
                cash_from_sale = shares * df["Close"][i]  # calculate cash from selling shares
                shares = 0
                cash += cash_from_sale
                cash_list.append(cash)
                dates_list.append(df["Date"][i])
                
                num_of_sells+=1
                if (last_sell_cash != None):
                    if (cash_from_sale > last_sell_cash):
                        success_rate+=1
                
                last_sell_cash = cash_from_sale

        # Calculate final investment value
        final_investment = cash + shares * df["Close"][-1]

        # Calculate profit
        profit = final_investment - first_investment

        # Print final investment value and profit
        print("<br><br><br>Start Date: " + sys.argv[2])
        print("<br>End Date: " + sys.argv[3])
        print("<br><br>Profit: {:.2f} %<br>".format(profit))

        first_investment_shares = first_investment / df["Close"][0]
        passive_investment_profit = first_investment_shares * df["Close"][-1] - first_investment
        print("Passive Investment Profit: {:.2f} %<br>".format(passive_investment_profit))
        
        print("Success Rate: {:.2f} %<br>".format((success_rate/num_of_sells) * 100))
        
        fig.add_trace(go.Scatter(x=dates_list, y=cash_list, name="Cash"))
        
        print('<br><br>' + fig.to_html(full_html=False, include_plotlyjs='cdn'))

    except Exception as er:
        print("<br><br>ERROR!!!!!!!!!!!!!!<br>")
        print(er)
    except:
        print("<br><br>ERROR!!!!!!!!!!!!!!")

if __name__ == "__main__":
    sys.exit(main())