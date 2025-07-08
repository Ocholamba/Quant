import numpy as np, pandas as pd, matplotlib.pyplot as plt

'''A Stock Portfolio Tracker is a program that manages data for multiple stocks(e.g.,prices,returns) and computes portfolio metrics(e.g.,total return, weighted
returns. I will be using a made-up data of stocks round the world for this project.'''

data = {'Date':['2025-07-01','2025-07-02','2025-07-03','2025-07-04','2025-07-05'], 'AAPL':[150,152,149,153,151],'GOOG':[2800,2810,2790,2820,2815],'MSFT':[300,298,301,303,302]}
#I will put this data in a dataframe using pandas
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'],format= '%Y-%m-%d')
#I will define a function that calculates returns
def rets(data_1):
    return round(data_1.pct_change(),4)
#I will add each stock returns to the dataframe
df['AAPL Ret'] = rets(df['AAPL'])
df['GOOG Ret'] = rets(df['GOOG'])
df['MSFT Ret'] = rets(df['MSFT'])
#I will introduce weights for each stock that sums to ~1. The weights is like a percentage of how much stock we have
weights = {'AAPL':0.5,'GOOG':0.3,'MSFT':0.2}
if abs(sum(weights.values())-1.0)>0.001: #Allow for small floatin point errors
    raise Exception('Error: Weights must sum to 1')
# We calculate the weighted returns for each stock which is the returns of the stock multiplied by its weight and add them to the dataframe
df['AAPL WR'] = df['AAPL Ret'] * weights['AAPL']
df['GOOG WR'] = df['GOOG Ret'] * weights['GOOG']
df['MSFT WR'] = df['MSFT Ret'] * weights['MSFT']
# We then add a 'Portfolio return' which is the net result (gain or loss) of all investents in a portfolio. It's the sum of all weighted returns
df['PoRe'] = df['AAPL WR'] + df['GOOG WR'] + df['MSFT WR']

''' Now we def a function that calculates the 'Sharpe Ratio' which is a metric used in finance to assess the risk-adjusted return of an investment or portfolio. 
It measures how much excess return an investment generates for each unit of risk taken, with higher Sharpe ratios indicating better risk-adjusted performance. 
Essentially, it helps investors understand if an investment's return is worth the risk involved. '''

def sharpe_ratio(returns,risk_free_rate):
    mean_returns = np.mean(returns)
    if risk_free_rate > 1 or risk_free_rate<0:
        raise Exception('Error: Rate must be converted from percentage to decimal')
    else:
        rate = risk_free_rate/252 # risk free rate for 252 working days
    sd = np.std(returns) # volatility which is a measure of risk
    return round((mean_returns-rate)/sd,4)
# Now we calculate the sharpe ratio of all returns using the same risk-free rate of 3% tho what we really need is the portfolio sharpe ratio
portfolio_sharpe = sharpe_ratio(df['PoRe'],0.03)
AAPL_sharpe = sharpe_ratio(df['AAPL Ret'],0.03)
GOOG_sharpe = sharpe_ratio(df['GOOG Ret'],0.03)
MSFT_sharpe = sharpe_ratio(df['MSFT Ret'],0.03)
print(f'Portfolio Sharpe: {portfolio_sharpe}\nAAPL Sharpe: {AAPL_sharpe}\nGOOG Sharpe: {GOOG_sharpe}\nMSFT Sharpe: {MSFT_sharpe}')

'''Now we def a function that calculates the 'Moving Average' which is a technical indicator used to smooth out price data and identify the direction of a 
trend in financial markets. It calculates the average price of an asset over a specific period, and as new price data becomes available, the average is 
recalculated, "moving" along with the price action. '''

def moving_average(data, window):
    if window > len(data.dropna()):
        raise Exception(f'Need at least {window} returns for {window} moving average ')
    return round(data.rolling(window=window).mean(),4)
# We add the portfolio Moving Average to the dataframe
try:
    df['Portfolio MA'] = moving_average(df['PoRe'],3)
    print(df)
except Exception as e:
    print(f'Error: {e}')

# We should show our data in a graph-like design
plt.plot(df['Date'],df['PoRe'],label = 'Portfolio Returns') # This shows PoRe for each day
plt.plot(df['Date'],df['Portfolio MA'], label = 'Portfolio MA') # This shows Portfolio MA for each day
plt.title('Portfolio Returns and 3 Day Moving Average') # This is the title of the graph
plt.xlabel('Date') # Title of X-axis
plt.ylabel('Returns') # Title of Y-axis
plt.xticks(rotation = 45) # rotates the X-axis
plt.savefig('Project 1.png') # saves the graph in a png file
plt.legend() # Distinguishes between the two lines for PoRe and Portfolio MA
plt.show() # shows the graph

# We finally save our data to a csv file
df.to_csv('Project 1.csv',index= False, header='Project 1 Data')

df_2 = pd.read_csv('Project 1.csv')
print(df_2)
