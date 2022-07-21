import numpy as np
import pandas as pd
from scipy.stats import norm

# RETURNS
def cumulative_returns(returns):
    return np.exp(returns.cumsum())

def annualized_returns_percentage(returns):
    return f'{np.round(annualized_returns(returns) * 100, 2)}%'

def annualized_returns(returns):
    return returns.mean() * 252

# VOLATILITY
def annualized_volatility_percentage(returns):
    return f'{np.round(annualized_volatility(returns) * 100, 2)}%'

def annualized_volatility(returns):
    return returns.std() * np.sqrt(252)

# PORTFOLIO EFFICIENCY
def sharpe_ratio(returns, risk_free_rate):
    # Risk free rate is already annualized
    
    sharpe_ratio = (annualized_returns(returns) - (risk_free_rate / 100)) / annualized_volatility(returns) 
    return sharpe_ratio

# MAXIMUM DRAWDOWN
def max_drawdown(returns):
    cumulative_ret = cumulative_returns(returns)
    cumulative_ret = pd.Series(cumulative_ret) * 100 # In order to use some built in functions
    max_return = cumulative_ret.cummax()
    mdd = cumulative_ret.sub(max_return).div(max_return).min()
    return mdd
    
# CALMAR RATIO
def calmar_ratio(returns):
    mdd = max_drawdown(returns)
    if mdd < 0:
        cm = annualized_returns(returns) / abs(mdd)
    else:
        return np.nan

    if np.isinf(cm):
        return np.nan

    return cm

# INFORMATION RATIO
def IR(returns, benchmark):
    active_returns = returns - benchmark
    tracking_error = active_returns.std(ddof=1) * np.sqrt(252)
    ir = (annualized_returns(returns) - annualized_returns(benchmark)) / tracking_error
    return ir

# MODIGLIANI RATIO
def M2(returns, benchmark, risk_free_rate):
     benchmark_volatility = benchmark.std() * np.sqrt(252)
     m2_ratio = sharpe_ratio(returns, risk_free_rate) * benchmark_volatility + (risk_free_rate / 100)
     return m2_ratio

# VALUE AT RISK
def VaR(returns):
    #returns_y = annualized_returns(returns)
    #volatility_y = annualized_volatility(returns)
    #VaR_90 = norm.ppf(1-0.9, returns_y, volatility_y)
    #VaR_95 = norm.ppf(1-0.95, returns_y, volatility_y)
    #VaR_99 = norm.ppf(1-0.99, returns_y, volatility_y)
    
    # HERE WE KEPT THE DAILY RETURNS
    VaR_90 = norm.ppf(1-0.9, returns.mean(), returns.std())
    VaR_95 = norm.ppf(1-0.95, returns.mean(), returns.std())
    VaR_99 = norm.ppf(1-0.99, returns.mean(), returns.std())
    return VaR_90, VaR_95, VaR_99

def get_base_metrics(portfolio_name, portfolio_returns):
    portfolio_returns = np.array(portfolio_returns)
    metrics = pd.DataFrame(columns=['Portfolio Title', 'Annualized Returns', 'Annualized Volatility'])
    metrics.loc[0] = [portfolio_name, annualized_returns_percentage(portfolio_returns), annualized_volatility_percentage(portfolio_returns)]
    return metrics

def get_advanced_metrics(portfolio_name, portfolio_returns, benchmark, risk_free_rate):
    portfolio_returns = np.array(portfolio_returns)
    benchmark = np.array(benchmark)
    metrics = pd.DataFrame(columns=['Portfolio Title', 'Sharpe Ratio', 'MDD', 'CL', 'Var 90', 'Var 95', 'Var 99', 'IR', 'M2'])
    VaRs = VaR(portfolio_returns)
    metrics.loc[0] = [
        portfolio_name, 
        sharpe_ratio(portfolio_returns, risk_free_rate), 
        max_drawdown(portfolio_returns), 
        calmar_ratio(portfolio_returns),
        VaRs[0],
        VaRs[1],
        VaRs[2],
        IR(portfolio_returns, benchmark),
        M2(portfolio_returns, benchmark, risk_free_rate)
    ]
    return metrics
