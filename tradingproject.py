

def readdata(filename):  #This function opens and reads in the csv file
    infile = open(filename, 'r')
    data = infile.readlines()
    infile.close()
    return data


def parse_csv(result):  #result is the data we got from the csv file
    date = []           #This function returns the list of all data in the file
    open1 = []          #All in their different categories
    high = []
    low = []
    close = []
    adj_close = []
    volume = []
    alldata = [date, open1, high, low, close, adj_close, volume]
    for i in range(1, len(result)):
        Date, Open, High, Low, Close, Adj_Close, Volume = result[i].split(',')
        high.append(eval(High))
        date.append(Date)
        open1.append(eval(Open))
        low.append(eval(Low))
        close.append(eval(Close))
        adj_close.append(eval(Adj_Close))
        volume.append(eval(Volume))
    return alldata


def get_price(data, col, day):  #This function returns
    if col == 'open':           #the price in col's category
        price = (data[1])[day-1]  #At the corresponding day
    if col == 'high':
        price = (data[2])[day-1]
    if col == 'low':
        price = (data[3])[day-1]
    if col == 'close':
        price = (data[4])[day-1]
    if col == 'adj_close':
        price = (data[5])[day-1]
    if col == 'volume':
        price = (data[6])[day-1]
    return price


def test_data(filename, col, day):
    """A test function to query the data loaded into your program.
    Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.
        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.
             The string arguments MUST be LOWERCASE!
        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.
    Returns:
        A value selected for the stock on some particular day, in some
        column col.
    """
    result = readdata(filename)
    data = parse_csv(result)
    price = get_price(data, col, day)
    return price



def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.
       Args:
           funds: An account balance, a float; it is a value of how much money you have,
                  currently.
           stocks: An int, representing the number of stock you currently own.
           qty: An int, representing how many stock you wish to buy or sell.
           price: An float reflecting a price of a single stock.
           buy: This option parameter, if set to true, will initiate a buy.
           sell: This option parameter, if set to true, will initiate a sell.
       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.
           Error condition #1: If the `buy` and `sell` keyword parameters are both set to true,
           or both false. We print an error message, and then return
           the `funds` and `stocks` parameters unaltered. This is an ambiguous
           transaction request!
           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  We print an error message,
           and then return the `funds` and `stocks` parameters unaltered. This
           is an ambiguous transaction request!
    """
    cost = price * qty
    if buy != sell:
        if buy is True and sell is False:
            if funds >= cost:
                cash_balance = funds - cost
                stocks_owned = stocks + qty
                print("Bought {0} stocks at ${1:0.2f}".format(qty, price), end="\n")
                print("  Actual stock owned: {0} stocks and cash balance: ${1:0.2f}".format(stocks_owned, cash_balance), end="\n")
                return float(cash_balance), int(stocks_owned)
            else:
                print("INSUFFICIENT FUNDS: ", end="")
                print("purchase of {0} at ${1:0.2f} ".format(qty, price), end="")
                print("requires {0},but ${1} available!".format(cost, funds))
                return funds, stocks
        if sell is True and buy is False:
            if stocks >= qty:
                cash_balance = funds + cost
                stocks_owned = stocks - qty
                print("Sold {0} stocks at ${1:0.2f}".format(qty, price), end="\n")
                print("  Actual stock owned: {0} stocks and cash balance: ${1:0.2f}".format(stocks_owned, cash_balance), end="\n")
                return float(cash_balance), int(stocks_owned)
            else:
                print("INSUFFICIENT STOCK: ", end="")
                print("{0} stocks owned, but selling {1}!".format(stocks, qty))
                return funds, stocks
    if (buy is True and sell is True) or (buy is False and sell is False):
        print("Ambigious transaction! Can't determine whether to buy or sell.")
        print("No action performed.")
        return funds, stocks


def moving_average_function(dat):

    cash_balance = 100000
    stock_owned = 0
    for i in range(len(dat)-20):
        average = sum(dat[i:i+19+1])/20
        price = dat[i+19+1]
        if price != dat[-1]:
            if price >= 1.05 * average:
                if stock_owned >= 10:
                    cash_balance, stock_owned = transact(cash_balance,
                                                         stock_owned,
                                                         10, price, sell=True)
                else:
                    pass
            if price <= 0.95 * average:
                if 10 * price <= cash_balance:
                    cash_balance, stock_owned = transact(cash_balance,
                                                         stock_owned,
                                                         10, price, buy=True)
                else:
                    pass
        if price == dat[-1]:
            cash_balance, stock_owned = transact(cash_balance,
                                                 stock_owned,
                                                 stock_owned, price, sell=True)
    return stock_owned, int(cash_balance)


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.
    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - We buy shares if the current day price is 5%, or more, lower than the moving average.
    - We sell shares if the current day price is 5% higher, or more than the moving average.
    - We buy, or sell 10 stocks per transaction.
    Args:
        A filename, as a string.
    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.
    Prints:
        Nothing.
    """

    result = readdata(filename)
    data = parse_csv(result)
    dat = data[4]
    stock_owned, cash_balance = moving_average_function(dat)
    return stock_owned, int(cash_balance)


def scalping_algo(filename):
    """This function implements the student's custom trading algorithm.
    Using the CSV stock data that should be loaded into your program, use
    that data to make decisions using your own custome trading algorithm.

    Args:
        A filename, as a string.
    Algorithm:
   Inspired by the Scalping algorithm which is a Day trading method.
   A scalper basically buys stocks at the beginning of a day and can sell them the same day if the price increases by a certain percentage in order to make profit.
   .Instead of trading twice or multiple time a day, my algorithm will make the user buy stocks on the first day, and will hold those stocks until a price on a future day is 20% higher than the price at which the user bought the stocks and sell them.
   .After selling , it will wait until the price of stock on a future day is 15% less than the price at which he lastly sold stocks to buy new stocks.
   .After buying , the program will look for the next price that is  20% higher than the price at which it lastly bought to sell.
   .This will repeat until the last day of data where it sells all the stocks left.
   .And the function will return of course, the cash balance and the stock owned ( which will be 0).
    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.
    Prints:
        Nothing.
    """

    result = readdata(filename)
    data = parse_csv(result)
    dat = data[4]
    action = "buy"
    price = 0.0
    cash_balance = 100000
    stock_owned = 0
    for i in range(len(dat)):
        if dat[i] == dat[0]:
            cash_balance, stock_owned = transact(cash_balance,
                                                 stock_owned,
                                                 200, dat[i], buy=True)
            action = "Sell"
            price = dat[i]
        if dat[i] != dat[0] and dat[i] != dat[-1]:
            if action == "buy":
                if dat[i] >= 1.20 * price:
                    if stock_owned >= 200:
                        cash_balance, stock_owned = transact(cash_balance,
                                                             stock_owned, 200,
                                                             dat[i], sell=True)
                        action = "Sell"
                        price = dat[i]
                    else:
                        action = "buy"
                else:
                    continue
            if action == "Sell":
                if dat[i] <= 0.75 * price:
                    if cash_balance >= dat[i] * 200:
                        cash_balance, stock_owned = transact(cash_balance,
                                                             stock_owned, 200,
                                                             dat[i], buy=True)
                        action = "buy"
                        price = dat[i]
                    else:
                        action = "Sell"
                else:
                    continue
        if dat[i] == dat[-1]:
            cash_balance, stock_owned = transact(cash_balance, stock_owned,
                                                 stock_owned, dat[i], sell=True)
    return stock_owned, int(cash_balance)


def main():

    filename = input("Enter a filename for stock data (CSV format): ")

    alg1_stocks, alg1_balance = alg_moving_average(filename)
    print("The results using moving average are : {0} unit in stock and ${1} as cash balance.".
          format(alg1_stocks, alg1_balance))

    alg2_stocks, alg2_balance = scalping_algo(filename)

    print("The results using the scalping method are :"
          "{0} unit in stock and ${1} as cash balance."
          .format(alg2_stocks, alg2_balance))

if __name__ == '__main__':
    main()