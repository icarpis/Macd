

def calc_cash_balance(INVEST_PERCENTAGE, start_cash_balance, df, begin_stock_val, end_stock_val, MOVING_STOP_LOSS):
    dates_list = []
    cash_list = []
    
    cash_list.append(start_cash_balance)
    dates_list.append(df["ActualDate"][0])
    
    cash = start_cash_balance  # start with start_cash_balance in cash
    shares = 0
    
    stop_loss_buy_cash = start_cash_balance  # start with start_cash_balance in cash
    stop_loss_buy_shares = 0

    static_cash = cash - ((cash * INVEST_PERCENTAGE)/100)
    static_shares = static_cash / begin_stock_val

    buy_amount = ((cash * INVEST_PERCENTAGE)/100)
    local_max = 0
    local_max_list = []
    after_buy = False
    moving_stop_loss_list = []
    moving_stop_loss_dates = []
    sell_idx = 0
    after_moving_stop_loss = False
    last_sell_cash = None
    num_of_success = 0
    num_of_sells = 0
    for i in range(len(df)):
        if (df["Close"][i] > local_max):
            local_max = df["Close"][i]

        if df["Buy"][i] == True:
            shares_to_buy = buy_amount / df["Close"][i]  # calculate number of shares to buy
            
            shares += shares_to_buy  # add shares to portfolio
            cash -= buy_amount
            
            stop_loss_buy_shares += shares_to_buy
            stop_loss_buy_cash -= buy_amount
            
            
            local_max = df["Close"][i]
            after_buy = True
        elif (df["Sell"][i] == True):
            cash_from_sale = shares * df["Close"][i]  # calculate cash from selling shares
            
            shares = 0
            cash += cash_from_sale
            
            if (not after_moving_stop_loss):
                stop_loss_buy_shares = 0
                stop_loss_buy_cash += cash_from_sale
                
            after_moving_stop_loss = False
        
            cash_list.append(cash)
            dates_list.append(df["ActualDate"][i])
            
            local_max_list.append(local_max)
            local_max = 0
            if (not after_buy) and (sell_idx == 0):
                sell_idx += 2
            else:
                sell_idx += 1
            
            after_buy = False
            
            num_of_sells+=1
            if (last_sell_cash != None):
                if (cash_from_sale > last_sell_cash):
                    num_of_success+=1

            last_sell_cash = cash_from_sale
            
        elif (after_buy and (local_max != 0) and (MOVING_STOP_LOSS != 0) and ((((local_max - df["Close"][i])/local_max) * 100) >= MOVING_STOP_LOSS)):
            moving_stop_loss_list.append(df["Close"][i])
            moving_stop_loss_dates.append(df["ActualDate"][i])
            #sell_signals["Close"][sell_idx] = df["Close"][i]
            after_buy = False
            
            print("<br>MOVING_STOP_LOSS_SELL_SIGNAL: " + str(df["ActualDate"][i]) + "  " + str(df["Close"][i]))
            
            cash_from_sale = stop_loss_buy_shares * df["Close"][i]  # calculate cash from selling shares
            
            stop_loss_buy_shares = 0
            stop_loss_buy_cash += cash_from_sale
           
            after_moving_stop_loss = True


    if (static_cash != 0):
        cash -= static_cash
        cash += (static_shares * end_stock_val)
        cash_list.append(cash)

    # Calculate final cash balance
    end_cash_balance = cash + shares * df["Close"][-1]
    
    success_rate = 0
    if (num_of_sells != 0):
        success_rate = num_of_success/num_of_sells

    return (end_cash_balance, stop_loss_buy_cash, stop_loss_buy_shares, moving_stop_loss_list, moving_stop_loss_dates, success_rate, cash_list, dates_list, local_max_list)
