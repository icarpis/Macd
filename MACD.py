from datetime import datetime as dt
import sys
import io
import datetime



def print_signals(buy_signals, sell_signals, local_max_list):
    buy_signals = buy_signals.reset_index()[["Date", "Close"]]
    sell_signals = sell_signals.reset_index()[["Date", "Close"]]
    buy_signals["Signal Type"] = "Buy"
    sell_signals["Signal Type"] = "Sell"

    import pandas as pd
    signals = pd.concat([buy_signals, sell_signals]).sort_values(by="Date").reset_index(drop=True)

    # print buy signals
    idx = 1
    print("<br><br>Signals:<br>")
    last_buy = 0
    i = 0
    for index, row in signals.iterrows():
        txt = ""
        if (row["Signal Type"] == "Buy"):
            last_buy = row['Close']
            print(str(idx) + ". Buy Signal: ")
        else:
            if (last_buy == 0):
                print(str(idx) + ". Sell Signal: ")
            else:
                print(" ; Sell Signal: ")
                
            idx+=1
            if (last_buy != 0):
                diff = float(row['Close']) - float(last_buy)
                diff_perc = "{:.4f}".format(100*((diff) / float(last_buy))) + " %)"

                color = "red"
                if (diff > 0):
                    color = "green"
                    diff_perc = " (+" + diff_perc
                else:
                    diff_perc = " (" + diff_perc
                
                txt = " ; local_max: " + "{:.2f}".format(local_max_list[i]) + " ; <p style=\"display:inline;color:" + color + ";\">Diff: " + "{:.2f}".format(diff) + diff_perc + "</p><br>"
                i+=1
            else:
                txt = "<br>"

        print("{} - {:.2f}".format(row['Date'].strftime('%Y-%m-%d'), row['Close']))
        print(txt)


# Calculate MACD indicator
def MACD(df, a, b, c):
    df["EMA_12"] = df["Close"].ewm(span=a, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=b, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal"] = df["MACD"].ewm(span=c, adjust=False).mean()
    df["Histogram"] = df["MACD"] - df["Signal"]

    # Buy and sell signals
    df["Buy"] = (df["MACD"] > df["Signal"]) & (df["MACD"].shift() < df["Signal"].shift())
    df["Sell"] = (df["MACD"] < df["Signal"]) & (df["MACD"].shift() > df["Signal"].shift())


    exp1 = df['Close'].ewm(span=a, adjust=False).mean()
    exp2 = df['Close'].ewm(span=b, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=c, adjust=False).mean()
    hist = macd - signal

    return (df, macd, signal, hist)


def handle_stock(stock_list):
    import plotly.graph_objs as go

    # Create figure
    fig = go.Figure()
    
    for STOCK_NAME in stock_list:
        print("Stock Name: " + STOCK_NAME + "<br>")
        stock_ticker = STOCK_NAME
        
        START_DATE = sys.argv[2].split("-")
        START_YEAR = int(START_DATE[0])
        START_MONTH = int(START_DATE[1])
        START_DAY = int(START_DATE[2])
        
        END_DATE = sys.argv[3].split("-")
        END_YEAR = int(END_DATE[0])
        END_MONTH = int(END_DATE[1])
        END_DAY = int(END_DATE[2])

        INVEST_PERCENTAGE = 100
        if (len(sys.argv) >= 6):
            INVEST_PERCENTAGE = int(sys.argv[5])
        
        
        MOVING_STOP_LOSS = int(sys.argv[6])
        
        import pytz
        tz = pytz.timezone("Israel")
        start_date = tz.localize(dt(START_YEAR,START_MONTH, START_DAY))
        end_date = tz.localize(dt(END_YEAR,END_MONTH, END_DAY) + datetime.timedelta(days=1))
        from dateutil.relativedelta import relativedelta
        import yfinance as yf
        stock_data = yf.download(stock_ticker, start=start_date - relativedelta(years=1), end=end_date)

        (df, macd, signal, hist) = MACD(stock_data, 12, 26, 9)

        df["ActualDate"] = df.index
        import numpy as np
        df = df.loc[(df['ActualDate'] >= np.datetime64(start_date)) & (df['ActualDate'] <= np.datetime64(end_date))]

        # Add trace for stock price
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name=STOCK_NAME + " Stock Price"))

        # Add trace for MACD
        fig.add_trace(go.Scatter(x=df.index, y=macd, name=STOCK_NAME + " MACD"))

        # Add trace for signal
        fig.add_trace(go.Scatter(x=df.index, y=signal, name=STOCK_NAME + " Signal"))

        # Add trace for histogram
        fig.add_trace(go.Bar(x=df.index, y=hist, name=STOCK_NAME + " Histogram"))

        # Add buy and sell signals
        buy_signals = df[(macd > signal) & (macd.shift() < signal.shift())]
        sell_signals = df[(macd < signal) & (macd.shift() > signal.shift())]

        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals["Close"], mode="markers", marker=dict(symbol="triangle-up", size=10, color="green"), name=STOCK_NAME + " Buy"))
        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals["Close"], mode="markers", marker=dict(symbol="triangle-down", size=10, color="red"), name=STOCK_NAME + " Sell"))

        import public.calc_cash
        start_cash_balance = 100
        (end_cash_balance, stop_loss_buy_cash, stop_loss_buy_shares, moving_stop_loss_list, moving_stop_loss_dates, success_rate, cash_list, dates_list, local_max_list) = public.calc_cash.calc_cash_balance(INVEST_PERCENTAGE, start_cash_balance, df, stock_data["Close"][0], stock_data["Close"][-1], MOVING_STOP_LOSS)

        
        fig.add_trace(go.Scatter(x=moving_stop_loss_dates, y=moving_stop_loss_list, mode="markers", marker=dict(symbol="triangle-down", size=10, color="brown"), name=STOCK_NAME + " Moving Stop-Loss"))

        # Calculate MACD profit
        macd_profit = end_cash_balance - start_cash_balance

        stop_loss_buy_end_cash_balance = stop_loss_buy_cash + stop_loss_buy_shares * df["Close"][-1]

        stop_loss_buy_profit = stop_loss_buy_end_cash_balance - start_cash_balance


        print_signals(buy_signals, sell_signals, local_max_list)
        
        

        print("<br><br><br>Stock Name: " + STOCK_NAME + "<br>")
        print("Start Date: " + sys.argv[2])
        print("<br>End Date: " + sys.argv[3])
        
        print("<br><br>Cash Investment Precentage on Buy Signal: {}%<br>".format(INVEST_PERCENTAGE))
        
        print("<br>MACD Profit: {:.2f} %<br>".format(macd_profit))
        
        if (MOVING_STOP_LOSS != 0):
            print("<br>MACD Stop-Loss Profit: {:.2f} %<br>".format(stop_loss_buy_profit))

        start_cash_balance_shares = start_cash_balance / df["Close"][0]
        passive_investment_profit = start_cash_balance_shares * df["Close"][-1] - start_cash_balance
        print("Passive Investment Profit: {:.2f} % <br>".format(passive_investment_profit))
        
        print("Success Rate: {:.2f} %<br><br><br>".format((success_rate) * 100))
            
        fig.add_trace(go.Scatter(x=dates_list, y=cash_list, name=STOCK_NAME + " Cash"))
    return fig

def main():
    try:
        stock_list = []
        # Load stock data
        stock_list.append(sys.argv[1].upper())
        
        if (len(sys.argv) >= 5):
            if (sys.argv[4] != "-"):
                stock_list.append(sys.argv[4].upper())

        fig = handle_stock(stock_list)

        print('<br><br>' + fig.to_html(full_html=False, include_plotlyjs='cdn'))

    except Exception as er:
        print("<br><br>ERROR!!!!!!!!!!!!!!<br>")
        print(er)
    except:
        print("<br><br>ERROR!!!!!!!!!!!!!!")

if __name__ == "__main__":
    sys.exit(main())