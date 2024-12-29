import pandas as pd
import numpy as np
import talib

def calculate_technical_indicators(df):
    """
    Funkcja generuje DataFrame z dodatkowymi wskaźnikami technicznymi.
    """
    
    general_timeperiods = [3, 5, 7, 14, 20, 28]
    averages_timeperiods = [3, 5, 7, 14, 20]
    macd_timeperiods = [[12, 9], [6, 9]]
    ema_fast_timeperiod = 9
    ema_slow_timeperiod = 21
    boilinger_timeperiod = [20, 2]
    stochastic_timeperiods = [14, 3]
    stochastic_rsi_timeperiods = [14, 3]
    psar_acceleration = 0.02
    psar_maximum = 0.2
        
    rsi_buy_value = 30
    rsi_sell_value = 70
    cci_buy_value = -100
    cci_sell_value = 100
    mfi_buy_value = 30
    mfi_sell_value = 70
    stoch_buy_value = 20
    stoch_sell_value = 80
        
    adx_strong_trend = 25
    adx_weak_trend = 20
    adx_no_trend = 5
    
    success_threshold = 5
    drop_threshold = -2
    
    result = df.copy()
    
    result['close'] = pd.to_numeric(result['close'], errors='coerce')
    result[f'close_rising'] = result[f'close'].diff() > 0
    result[f'close_dropping'] = result[f'close'].diff() < 0
    result['close_change'] = result['close'].diff()
    result['close_pct_change'] = result['close'].pct_change() * 100
    for avg_period in averages_timeperiods:
        result[f'close_ma_{avg_period}'] = result['close'].rolling(window=avg_period).mean()
        result[f'close_rising_in_avg_period_{avg_period}'] = result['close'] > result[f'close_ma_{avg_period}']
        result[f'close_dropping_in_avg_period_{avg_period}'] = result['close'] < result[f'close_ma_{avg_period}']
        result[f'close_change_vs_ma_{avg_period}'] = result['close'] - result[f'close_ma_{avg_period}']
        result[f'close_pct_change_vs_ma_{avg_period}'] = (result['close'] - result[f'close_ma_{avg_period}']) / result[f'close_ma_{avg_period}'] * 100
        result[f'close_in_{avg_period}_avg_periods_rising'] = result['close'].shift(-avg_period) > result['close']
        result[f'close_in_{avg_period}_avg_periods_dropping'] = result['close'].shift(-avg_period) < result['close']
        result[f'close_change_in_{avg_period}_avg_periods'] = result['close'].shift(-avg_period) - result['close']
        result[f'close_pct_change_in_{avg_period}_avg_periods'] = (result['close'].shift(-avg_period) - result['close']) / result['close'] * 100
        
        result[f'max_close_in_{avg_period}'] = result[f'close_ma_{avg_period}'].rolling(window=avg_period).max()
        result[f'min_close_in_{avg_period}'] = result[f'close_ma_{avg_period}'].rolling(window=avg_period).min()
        
        result[f'close_trade_success_{avg_period}'] = (
            ((result[f'max_close_in_{avg_period}'] - result['close']) / result['close'] * 100 >= success_threshold) & 
            ((result[f'min_close_in_{avg_period}'] - result['close']) / result['close'] * 100 > drop_threshold)
        )

    result['high'] = pd.to_numeric(result['high'], errors='coerce')
    result[f'high_rising'] = result[f'high'].diff() > 0
    result[f'high_dropping'] = result[f'high'].diff() < 0
    result['high_change'] = result['high'].diff()
    result['high_pct_change'] = result['high'].pct_change() * 100
    for avg_period in averages_timeperiods:
        result[f'high_ma_{avg_period}'] = result['high'].rolling(window=avg_period).mean()
        result[f'high_rising_in_avg_period_{avg_period}'] = result['high'] > result[f'high_ma_{avg_period}']
        result[f'high_dropping_in_avg_period_{avg_period}'] = result['high'] < result[f'high_ma_{avg_period}']
        result[f'high_change_vs_ma_{avg_period}'] = result['high'] - result[f'high_ma_{avg_period}']
        result[f'high_pct_change_vs_ma_{avg_period}'] = (result['high'] - result[f'high_ma_{avg_period}']) / result[f'high_ma_{avg_period}'] * 100
        result[f'high_in_{avg_period}_avg_periods_rising'] = result['high'].shift(-avg_period) > result['high']
        result[f'high_in_{avg_period}_avg_periods_dropping'] = result['high'].shift(-avg_period) < result['high']
        result[f'high_change_in_{avg_period}_avg_periods'] = result['high'].shift(-avg_period) - result['high']
        result[f'high_pct_change_in_{avg_period}_avg_periods'] = (result['high'].shift(-avg_period) - result['high']) / result['high'] * 100
        
    result['low'] = pd.to_numeric(result['low'], errors='coerce')
    result[f'low_rising'] = result[f'low'].diff() > 0
    result[f'low_dropping'] = result[f'low'].diff() < 0
    result['low_change'] = result['low'].diff()
    result['low_pct_change'] = result['low'].pct_change() * 100
    for avg_period in averages_timeperiods:
        result[f'low_ma_{avg_period}'] = result['low'].rolling(window=avg_period).mean()
        result[f'low_rising_in_avg_period_{avg_period}'] = result['low'] > result[f'low_ma_{avg_period}']
        result[f'low_dropping_in_avg_period_{avg_period}'] = result['low'] < result[f'low_ma_{avg_period}']
        result[f'low_change_vs_ma_{avg_period}'] = result['low'] - result[f'low_ma_{avg_period}']
        result[f'low_pct_change_vs_ma_{avg_period}'] = (result['low'] - result[f'low_ma_{avg_period}']) / result[f'low_ma_{avg_period}'] * 100
        result[f'low_in_{avg_period}_avg_periods_rising'] = result['low'].shift(-avg_period) > result['low']
        result[f'low_in_{avg_period}_avg_periods_dropping'] = result['low'].shift(-avg_period) < result['low']
        result[f'low_change_in_{avg_period}_avg_periods'] = result['low'].shift(-avg_period) - result['low']
        result[f'low_pct_change_in_{avg_period}_avg_periods'] = (result['low'].shift(-avg_period) - result['low']) / result['low'] * 100
        
    result['volume'] = pd.to_numeric(result['volume'], errors='coerce')
    result[f'volume_rising'] = result[f'volume'].diff() > 0
    result[f'volume_dropping'] = result[f'volume'].diff() < 0
    result['volume_change'] = result['volume'].diff()
    result['volume_pct_change'] = result['volume'].pct_change() * 100
    for avg_period in averages_timeperiods:
        result[f'volume_ma_{avg_period}'] = result['volume'].rolling(window=avg_period).mean()
        result[f'volume_rising_in_avg_period_{avg_period}'] = result['volume'] > result[f'volume_ma_{avg_period}']
        result[f'volume_dropping_in_avg_period_{avg_period}'] = result['volume'] < result[f'volume_ma_{avg_period}']
        result[f'volume_change_vs_ma_{avg_period}'] = result['volume'] - result[f'volume_ma_{avg_period}']
        result[f'volume_pct_change_vs_ma_{avg_period}'] = (result['volume'] - result[f'volume_ma_{avg_period}']) / result[f'volume_ma_{avg_period}'] * 100

    result['open_time'] = pd.to_datetime(result['open_time'], unit='ms')
    result['open_time_hour'] = result['open_time'].dt.hour  # Godzina transakcji
    result['open_time_weekday'] = result['open_time'].dt.weekday  # Dzień tygodnia (0 = poniedziałek)
    result['open_time_month'] = result['open_time'].dt.month  # Miesiąc
    result['open_time_is_weekend'] = result['weekday'].isin([5, 6]).astype(int)  # 5 = sobota, 6 = niedziela
    # Sprawdzamy, czy formacja pojawia się w godzinach porannych (np. 9-12)
    result['hammer_morning'] = (result['hammer'] & (result['open_time_hour'] >= 9) & (result['open_time_hour'] <= 12)).astype(int)
    result['morning_star_morning'] = (result['morning_star'] & (result['open_time_hour'] >= 9) & (result['open_time_hour'] <= 12)).astype(int)
    result['bullish_engulfing_morning'] = (result['bullish_engulfing'] & (result['open_time_hour'] >= 9) & (result['open_time_hour'] <= 12)).astype(int)
    # Sprawdzamy, czy formacje pojawiają się w weekendy (5 = sobota, 6 = niedziela)
    result['hammer_weekend'] = (result['hammer'] & result['open_time_weekday'].isin([5, 6])).astype(int)
    result['morning_star_weekend'] = (result['morning_star'] & result['open_time_weekday'].isin([5, 6])).astype(int)
    result['bullish_engulfing_weekend'] = (result['bullish_engulfing'] & result['open_time_weekday'].isin([5, 6])).astype(int)
    #itp

    result['close_time'] = pd.to_datetime(result['close_time'], unit='ms')
    result['close_time_hour'] = result['close_time'].dt.hour  # Godzina transakcji
    result['close_time_weekday'] = result['close_time'].dt.weekday  # Dzień tygodnia (0 = poniedziałek)
    result['close_time_month'] = result['close_time'].dt.month  # Miesiąc
    result['close_time_is_weekend'] = result['weekday'].isin([5, 6]).astype(int)  # 5 = sobota, 6 = niedziela
    
    # Oblicz RSI dla różnych okresów
    for period in general_timeperiods:
        result[f'rsi_{period}'] = talib.RSI(
            result['close'], 
            timeperiod=period
            )
        result[f'rsi_{period}_rising'] = result[f'rsi_{period}'].diff() > 0
        result[f'rsi_{period}_dropping'] = result[f'rsi_{period}'].diff() < 0
        result[f'rsi_{period}_change'] = result[f'rsi_{period}'].diff()
        result[f'rsi_{period}_pct_change'] = result[f'rsi_{period}'].pct_change() * 100
        result[f'rsi_{period}_buy'] = result[f'rsi_{period}'] < rsi_buy_value
        result[f'rsi_{period}_sell'] = result[f'rsi_{period}'] > rsi_sell_value
        
        result[f'rsi_{period}_bullish_divergence'] = (
            (result[f'rsi_{period}_rising'] == True) & 
            (result[f'close_dropping'] == True)
        )
        result[f'rsi_{period}_bearish_divergence'] = (
            (result[f'rsi_{period}_dropping'] == True) & 
            (result[f'close_rising'] == True)
        )

        for avg_period in averages_timeperiods:
            result[f'rsi_{period}_ma_{avg_period}'] = result[f'rsi_{period}'].rolling(window=avg_period).mean()
            result[f'rsi_{period}_rising_in_avg_period_{avg_period}'] = result[f'rsi_{period}'] > result[f'rsi_{period}_ma_{avg_period}']
            result[f'rsi_{period}_dropping_in_avg_period_{avg_period}'] = result[f'rsi_{period}'] < result[f'rsi_{period}_ma_{avg_period}']
            result[f'rsi_{period}_change_vs_ma_{avg_period}'] = result[f'rsi_{period}'] - result[f'rsi_{period}_ma_{avg_period}']
            result[f'rsi_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'rsi_{period}'] - result[f'rsi_{period}_ma_{avg_period}']) / result[f'rsi_{period}_ma_{avg_period}'] * 100
            result[f'rsi_{period}_ma_{avg_period}_buy'] = result[f'rsi_{period}_ma_{avg_period}'] < rsi_buy_value
            result[f'rsi_{period}_ma_{avg_period}_sell'] = result[f'rsi_{period}_ma_{avg_period}'] > rsi_sell_value
            
            result[f'rsi_{period}_ma_{avg_period}_bullish_divergence'] = (
                (result[f'rsi_{period}_rising_in_avg_period_{avg_period}'] == True) & 
                (result[f'close_dropping_in_avg_period_{avg_period}'] == True)
            )
            result[f'rsi_{period}_ma_{avg_period}_bearish_divergence'] = (
                (result[f'rsi_{period}_dropping_in_avg_period_{avg_period}'] == True) & 
                (result[f'close_rising_in_avg_period_{avg_period}'] == True)
            )

        result[f'cci_{period}'] = talib.CCI(
            result['high'],
            result['low'],
            result['close'],
            timeperiod=period
            )
        result[f'cci_{period}_rising'] = result[f'cci_{period}'].diff() > 0
        result[f'cci_{period}_dropping'] = result[f'cci_{period}'].diff() < 0
        result[f'cci_{period}_change'] = result[f'cci_{period}'].diff()
        result[f'cci_{period}_pct_change'] = result[f'cci_{period}'].pct_change() * 100
        result[f'cci_{period}_buy'] = result[f'cci_{period}'] < cci_buy_value
        result[f'cci_{period}_sell'] = result[f'cci_{period}'] > cci_sell_value
        
        result[f'cci_{period}_bullish_divergence'] = (
            (result[f'cci_{period}_rising'] == True) & 
            (result[f'close_dropping'] == True)
        )
        result[f'cci_{period}_bearish_divergence'] = (
            (result[f'cci_{period}_dropping'] == True) & 
            (result[f'close_rising'] == True)
        )

        for avg_period in averages_timeperiods:
            result[f'cci_{period}_ma_{avg_period}'] = result[f'cci_{period}'].rolling(window=avg_period).mean()
            result[f'cci_{period}_rising_in_avg_period_{avg_period}'] = result[f'cci_{period}'] > result[f'cci_{period}_ma_{avg_period}']
            result[f'cci_{period}_dropping_in_avg_period_{avg_period}'] = result[f'cci_{period}'] < result[f'cci_{period}_ma_{avg_period}']
            result[f'cci_{period}_change_vs_ma_{avg_period}'] = result[f'cci_{period}'] - result[f'cci_{period}_ma_{avg_period}']
            result[f'cci_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'cci_{period}'] - result[f'cci_{period}_ma_{avg_period}']) / result[f'cci_{period}_ma_{avg_period}'] * 100
            result[f'cci_{period}_ma_{avg_period}_buy'] = result[f'cci_{period}_ma_{avg_period}'] < cci_buy_value
            result[f'cci_{period}_ma_{avg_period}_sell'] = result[f'cci_{period}_ma_{avg_period}'] > cci_sell_value
            
            result[f'cci_{period}_ma_{avg_period}_bullish_divergence'] = (
                (result[f'cci_{period}_rising_in_avg_period_{avg_period}'] == True) & 
                (result[f'close_dropping_in_avg_period_{avg_period}'] == True)
            )
            result[f'cci_{period}_ma_{avg_period}_bearish_divergence'] = (
                (result[f'cci_{period}_dropping_in_avg_period_{avg_period}'] == True) & 
                (result[f'close_rising_in_avg_period_{avg_period}'] == True)
            )
            
        result[f'mfi_{period}'] = talib.MFI(
            result['high'],
            result['low'],
            result['close'],
            result['volume'],
            timeperiod=period
        )
        result[f'mfi_{period}_rising'] = result[f'mfi_{period}'].diff() > 0
        result[f'mfi_{period}_dropping'] = result[f'mfi_{period}'].diff() < 0
        result[f'mfi_{period}_change'] = result[f'mfi_{period}'].diff()
        result[f'mfi_{period}_pct_change'] = result[f'mfi_{period}'].pct_change() * 100
        result[f'mfi_{period}_buy'] = result[f'mfi_{period}'] < mfi_buy_value
        result[f'mfi_{period}_sell'] = result[f'mfi_{period}'] > mfi_sell_value
        
        result[f'mfi_{period}_bullish_divergence'] = (
            (result[f'mfi_{period}_rising'] == True) & 
            (result[f'close_dropping'] == True)
        )
        result[f'mfi_{period}_bearish_divergence'] = (
            (result[f'mfi_{period}_dropping'] == True) & 
            (result[f'close_rising'] == True)
        )

        for avg_period in averages_timeperiods:
            result[f'mfi_{period}_ma_{avg_period}'] = result[f'mfi_{period}'].rolling(window=avg_period).mean()
            result[f'mfi_{period}_rising_in_avg_period_{avg_period}'] = result[f'mfi_{period}'] > result[f'mfi_{period}_ma_{avg_period}']
            result[f'mfi_{period}_dropping_in_avg_period_{avg_period}'] = result[f'mfi_{period}'] < result[f'mfi_{period}_ma_{avg_period}']
            result[f'mfi_{period}_change_vs_ma_{avg_period}'] = result[f'mfi_{period}'] - result[f'mfi_{period}_ma_{avg_period}']
            result[f'mfi_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'mfi_{period}'] - result[f'mfi_{period}_ma_{avg_period}']) / result[f'mfi_{period}_ma_{avg_period}'] * 100
            result[f'mfi_{period}_ma_{avg_period}_buy'] = result[f'mfi_{period}_ma_{avg_period}'] < mfi_buy_value
            result[f'mfi_{period}_ma_{avg_period}_sell'] = result[f'mfi_{period}_ma_{avg_period}'] > mfi_sell_value
            
            result[f'mfi_{period}_ma_{avg_period}_bullish_divergence'] = (
                (result[f'mfi_{period}_rising_in_avg_period_{avg_period}'] == True) & 
                (result[f'close_dropping_in_avg_period_{avg_period}'] == True)
            )
            result[f'mfi_{period}_ma_{avg_period}_bearish_divergence'] = (
                (result[f'mfi_{period}_dropping_in_avg_period_{avg_period}'] == True) & 
                (result[f'close_rising_in_avg_period_{avg_period}'] == True)
            )

        result[f'atr_{period}'] = talib.ATR(
            result['high'], 
            result['low'], 
            result['close'], 
            timeperiod=period
            )
        result[f'atr_{period}_rising'] = result[f'atr_{period}'].diff() > 0
        result[f'atr_{period}_dropping'] = result[f'atr_{period}'].diff() < 0
        result[f'atr_{period}_change'] = result[f'atr_{period}'].diff()
        result[f'atr_{period}_pct_change'] = result[f'atr_{period}'].pct_change() * 100
        for avg_period in averages_timeperiods:
            result[f'atr_{period}_ma_{avg_period}'] = result[f'atr_{period}'].rolling(window=avg_period).mean()
            result[f'atr_{period}_rising_in_avg_period_{avg_period}'] = result[f'atr_{period}'] > result[f'atr_{period}_ma_{avg_period}']
            result[f'atr_{period}_dropping_in_avg_period_{avg_period}'] = result[f'atr_{period}'] < result[f'atr_{period}_ma_{avg_period}']
            result[f'atr_{period}_change_vs_ma_{avg_period}'] = result[f'atr_{period}'] - result[f'atr_{period}_ma_{avg_period}']
            result[f'atr_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'atr_{period}'] - result[f'atr_{period}_ma_{avg_period}']) / result[f'atr_{period}_ma_{avg_period}'] * 100

        result[f'adx_{period}'] = talib.ADX(
            result['high'],
            result['low'],
            result['close'],
            timeperiod=period
            )
        result[f'adx_{period}_strong_trend'] = result[f'adx_{period}'] > adx_strong_trend
        result[f'adx_{period}_weak_trend'] = (result[f'adx_{period}'] > adx_weak_trend) & (result[f'adx_{period}'] < adx_strong_trend)
        result[f'adx_{period}_no_trend'] = result[f'adx_{period}'] < adx_no_trend
        result[f'adx_{period}_rising'] = result[f'adx_{period}'].diff() > 0
        result[f'adx_{period}_dropping'] = result[f'adx_{period}'].diff() < 0
        result[f'adx_{period}_change'] = result[f'adx_{period}'].diff()
        result[f'adx_{period}_pct_change'] = result[f'adx_{period}'].pct_change() * 100
        for avg_period in averages_timeperiods:
            result[f'adx_{period}_ma_{avg_period}'] = result[f'adx_{period}'].rolling(window=avg_period).mean()
            result[f'adx_{period}_rising_in_avg_period_{avg_period}'] = result[f'adx_{period}'] > result[f'adx_{period}_ma_{avg_period}']
            result[f'adx_{period}_dropping_in_avg_period_{avg_period}'] = result[f'adx_{period}'] < result[f'adx_{period}_ma_{avg_period}']
            result[f'adx_{period}_change_vs_ma_{avg_period}'] = result[f'adx_{period}'] - result[f'adx_{period}_ma_{avg_period}']
            result[f'adx_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'adx_{period}'] - result[f'adx_{period}_ma_{avg_period}']) / result[f'adx_{period}_ma_{avg_period}'] * 100
            result[f'adx_{period}_ma_{avg_period}_strong_trend'] = result[f'adx_{period}_ma_{avg_period}'] > adx_strong_trend
            result[f'adx_{period}_ma_{avg_period}_weak_trend'] = (result[f'adx_{period}_ma_{avg_period}'] > adx_weak_trend) & (result[f'adx_{period}_ma_{avg_period}'] < adx_strong_trend)
            result[f'adx_{period}_ma_{avg_period}_no_trend'] = result[f'adx_{period}_ma_{avg_period}'] < adx_no_trend
            
        result[f'plus_di_{period}'] = talib.PLUS_DI(
            result['high'],
            result['low'],
            result['close'],
            timeperiod=period
        )
        result[f'plus_di_{period}_rising'] = result[f'plus_di_{period}'].diff() > 0
        result[f'plus_di_{period}_dropping'] = result[f'plus_di_{period}'].diff() < 0
        result[f'plus_di_{period}_change'] = result[f'plus_di_{period}'].diff()
        result[f'plus_di_{period}_pct_change'] = result[f'plus_di_{period}'].pct_change() * 100
        for avg_period in averages_timeperiods:
            result[f'plus_di_{period}_ma_{avg_period}'] = result[f'plus_di_{period}'].rolling(window=avg_period).mean()
            result[f'plus_di_{period}_rising_in_avg_period_{avg_period}'] = result[f'plus_di_{period}'] > result[f'plus_di_{period}_ma_{avg_period}']
            result[f'plus_di_{period}_dropping_in_avg_period_{avg_period}'] = result[f'plus_di_{period}'] < result[f'plus_di_{period}_ma_{avg_period}']
            result[f'plus_di_{period}_change_vs_ma_{avg_period}'] = result[f'plus_di_{period}'] - result[f'plus_di_{period}_ma_{avg_period}']
            result[f'plus_di_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'plus_di_{period}'] - result[f'plus_di_{period}_ma_{avg_period}']) / result[f'plus_di_{period}_ma_{avg_period}'] * 100

        result[f'minus_di_{period}'] = talib.MINUS_DI(
            result['high'],
            result['low'],
            result['close'],
            timeperiod=period
        )
        result[f'minus_di_{period}_rising'] = result[f'minus_di_{period}'].diff() > 0
        result[f'minus_di_{period}_dropping'] = result[f'minus_di_{period}'].diff() < 0
        result[f'minus_di_{period}_change'] = result[f'minus_di_{period}'].diff()
        result[f'minus_di_{period}_pct_change'] = result[f'minus_di_{period}'].pct_change() * 100
        for avg_period in averages_timeperiods:
            result[f'minus_di_{period}_ma_{avg_period}'] = result[f'minus_di_{period}'].rolling(window=avg_period).mean()
            result[f'minus_di_{period}_rising_in_avg_period_{avg_period}'] = result[f'minus_di_{period}'] > result[f'minus_di_{period}_ma_{avg_period}']
            result[f'minus_di_{period}_dropping_in_avg_period_{avg_period}'] = result[f'minus_di_{period}'] < result[f'minus_di_{period}_ma_{avg_period}']
            result[f'minus_di_{period}_change_vs_ma_{avg_period}'] = result[f'minus_di_{period}'] - result[f'minus_di_{period}_ma_{avg_period}']
            result[f'minus_di_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'minus_di_{period}'] - result[f'minus_di_{period}_ma_{avg_period}']) / result[f'minus_di_{period}_ma_{avg_period}'] * 100

        result[f'trend_{period}'] = result.apply(
            lambda row: 'Bullish' if row[f'adx_{period}'] > 25 and row[f'plus_di_{period}'] > row[f'minus_di_{period}'] else 
                        'Bearish' if row[f'adx_{period}'] > 25 and row[f'plus_di_{period}'] < row[f'minus_di_{period}'] else 
                        'No trend',
            axis=1
        )

    result[f'ema_{ema_fast_timeperiod}'] = talib.EMA(
        result['close'], 
        timeperiod=ema_fast_timeperiod
        )
    result[f'ema_{ema_fast_timeperiod}_{period}_rising'] = result[f'ema_{ema_fast_timeperiod}_{period}'].diff() > 0
    result[f'ema_{ema_fast_timeperiod}_{period}_dropping'] = result[f'ema_{ema_fast_timeperiod}_{period}'].diff() < 0
    result[f'ema_{ema_fast_timeperiod}_{period}_change'] = result[f'ema_{ema_fast_timeperiod}_{period}'].diff()
    result[f'ema_{ema_fast_timeperiod}_{period}_pct_change'] = result[f'ema_{ema_fast_timeperiod}_{period}'].pct_change() * 100
    
    for avg_period in averages_timeperiods:
        result[f'ema_{ema_fast_timeperiod}_{period}_ma_{avg_period}'] = result[f'ema_{ema_fast_timeperiod}_{period}'].rolling(window=avg_period).mean()
        result[f'ema_{ema_fast_timeperiod}_{period}_rising_in_avg_period_{avg_period}'] = result[f'ema_{ema_fast_timeperiod}_{period}'] > result[f'ema_{ema_fast_timeperiod}_{period}_ma_{avg_period}']
        result[f'ema_{ema_fast_timeperiod}_{period}_dropping_in_avg_period_{avg_period}'] = result[f'ema_{ema_fast_timeperiod}_{period}'] < result[f'ema_{ema_fast_timeperiod}_{period}_ma_{avg_period}']
        result[f'ema_{ema_fast_timeperiod}_{period}_change_vs_ma_{avg_period}'] = result[f'ema_{ema_fast_timeperiod}_{period}'] - result[f'ema_{ema_fast_timeperiod}_{period}_ma_{avg_period}']
        result[f'ema_{ema_fast_timeperiod}_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'ema_{ema_fast_timeperiod}_{period}'] - result[f'ema_{ema_fast_timeperiod}_{period}_ma_{avg_period}']) / result[f'ema_{ema_fast_timeperiod}_{period}_ma_{avg_period}'] * 100

    result[f'ema_{ema_slow_timeperiod}'] = talib.EMA(
        result['close'], 
        timeperiod=ema_slow_timeperiod
        )
    result[f'ema_{ema_slow_timeperiod}_{period}_rising'] = result[f'ema_{ema_slow_timeperiod}_{period}'].diff() > 0
    result[f'ema_{ema_slow_timeperiod}_{period}_dropping'] = result[f'ema_{ema_slow_timeperiod}_{period}'].diff() < 0
    result[f'ema_{ema_slow_timeperiod}_{period}_change'] = result[f'ema_{ema_slow_timeperiod}_{period}'].diff()
    result[f'ema_{ema_slow_timeperiod}_{period}_pct_change'] = result[f'ema_{ema_slow_timeperiod}_{period}'].pct_change() * 100
    for avg_period in averages_timeperiods:
        result[f'ema_{ema_slow_timeperiod}_{period}_ma_{avg_period}'] = result[f'ema_{ema_slow_timeperiod}_{period}'].rolling(window=avg_period).mean()
        result[f'ema_{ema_slow_timeperiod}_{period}_rising_in_avg_period_{avg_period}'] = result[f'ema_{ema_slow_timeperiod}_{period}'] > result[f'ema_{ema_slow_timeperiod}_{period}_ma_{avg_period}']
        result[f'ema_{ema_slow_timeperiod}_{period}_dropping_in_avg_period_{avg_period}'] = result[f'ema_{ema_slow_timeperiod}_{period}'] < result[f'ema_{ema_slow_timeperiod}_{period}_ma_{avg_period}']
        result[f'ema_{ema_slow_timeperiod}_{period}_change_vs_ma_{avg_period}'] = result[f'ema_{ema_slow_timeperiod}_{period}'] - result[f'ema_{ema_slow_timeperiod}_{period}_ma_{avg_period}']
        result[f'ema_{ema_slow_timeperiod}_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'ema_{ema_slow_timeperiod}_{period}'] - result[f'ema_{ema_slow_timeperiod}_{period}_ma_{avg_period}']) / result[f'ema_{ema_slow_timeperiod}_{period}_ma_{avg_period}'] * 100

    result[f'ema_{ema_fast_timeperiod}_prev'] = result['ema_fast'].shift(1)
    result[f'ema_{ema_slow_timeperiod}_prev'] = result['ema_slow'].shift(1)
    result[f'ema_{ema_fast_timeperiod}_cross_up'] = (result[f'ema_{ema_fast_timeperiod}_prev'] < result[f'ema_{ema_slow_timeperiod}_prev']) & (result[f'ema_{ema_fast_timeperiod}'] > result[f'ema_{ema_slow_timeperiod}'])
    result[f'ema_{ema_fast_timeperiod}_cross_down'] = (result[f'ema_{ema_fast_timeperiod}_prev'] > result[f'ema_{ema_slow_timeperiod}_prev']) & (result[f'ema_{ema_fast_timeperiod}'] < result[f'ema_{ema_slow_timeperiod}'])
        
    for period in macd_timeperiods:
        macd, macd_signal, _ = talib.MACD(result['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        result[f'macd_{period[0]}'] = macd
        result[f'macd_signal_{period[1]}'] = macd_signal
        result[f'macd_histogram_{period[0]}'] = result[f'macd_{period[0]}'] - result[f'macd_signal_{period[0]}']
        
        result[f'macd_{period[0]}_{period}_rising'] = result[f'macd_{period[0]}_{period}'].diff() > 0
        result[f'macd_{period[0]}_{period}_dropping'] = result[f'macd_{period[0]}_{period}'].diff() < 0
        result[f'macd_{period[0]}_{period}_change'] = result[f'macd_{period[0]}_{period}'].diff()
        result[f'macd_{period[0]}_{period}_pct_change'] = result[f'macd_{period[0]}_{period}'].pct_change() * 100
        
        result[f'macd_signal_{period[1]}_{period}_rising'] = result[f'macd_signal_{period[1]}_{period}'].diff() > 0
        result[f'macd_signal_{period[1]}_{period}_dropping'] = result[f'macd_signal_{period[1]}_{period}'].diff() < 0
        result[f'macd_signal_{period[1]}_{period}_change'] = result[f'macd_signal_{period[1]}_{period}'].diff()
        result[f'macd_signal_{period[1]}_{period}_pct_change'] = result[f'macd_signal_{period[1]}_{period}'].pct_change() * 100
        
        result[f'macd_histogram_{period[0]}_{period}_rising'] = result[f'macd_histogram_{period[0]}_{period}'].diff() > 0
        result[f'macd_histogram_{period[0]}_{period}_dropping'] = result[f'macd_histogram_{period[0]}_{period}'].diff() < 0
        result[f'macd_histogram_{period[0]}_{period}_change'] = result[f'macd_histogram_{period[0]}_{period}'].diff()
        result[f'macd_histogram_{period[0]}_{period}_pct_change'] = result[f'macd_histogram_{period[0]}_{period}'].pct_change() * 100
        
        for avg_period in averages_timeperiods:
            result[f'macd_{period[0]}_{period}_ma_{avg_period}'] = result[f'macd_{period[0]}_{period}'].rolling(window=avg_period).mean()
            result[f'macd_{period[0]}_{period}_rising_in_avg_period_{avg_period}'] = result[f'macd_{period[0]}_{period}'] > result[f'macd_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_{period[0]}_{period}_dropping_in_avg_period_{avg_period}'] = result[f'macd_{period[0]}_{period}'] < result[f'macd_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_{period[0]}_{period}_change_vs_ma_{avg_period}'] = result[f'macd_{period[0]}_{period}'] - result[f'macd_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_{period[0]}_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'macd_{period[0]}_{period}'] - result[f'macd_{period[0]}_{period}_ma_{avg_period}']) / result[f'macd_{period[0]}_{period}_ma_{avg_period}'] * 100

            result[f'macd_signal_{period[0]}_{period}_ma_{avg_period}'] = result[f'macd_signal_{period[0]}_{period}'].rolling(window=avg_period).mean()
            result[f'macd_signal_{period[0]}_{period}_rising_in_avg_period_{avg_period}'] = result[f'macd_signal_{period[0]}_{period}'] > result[f'macd_signal_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_signal_{period[0]}_{period}_dropping_in_avg_period_{avg_period}'] = result[f'macd_signal_{period[0]}_{period}'] < result[f'macd_signal_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_signal_{period[0]}_{period}_change_vs_ma_{avg_period}'] = result[f'macd_signal_{period[0]}_{period}'] - result[f'macd_signal_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_signal_{period[0]}_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'macd_signal_{period[0]}_{period}'] - result[f'macd_signal_{period[0]}_{period}_ma_{avg_period}']) / result[f'macd_signal_{period[0]}_{period}_ma_{avg_period}'] * 100

            result[f'macd_histogram_{period[0]}_{period}_ma_{avg_period}'] = result[f'macd_histogram_{period[0]}_{period}'].rolling(window=avg_period).mean()
            result[f'macd_histogram_{period[0]}_{period}_rising_in_avg_period_{avg_period}'] = result[f'macd_histogram_{period[0]}_{period}'] > result[f'macd_histogram_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_histogram_{period[0]}_{period}_dropping_in_avg_period_{avg_period}'] = result[f'macd_histogram_{period[0]}_{period}'] < result[f'macd_histogram_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_histogram_{period[0]}_{period}_change_vs_ma_{avg_period}'] = result[f'macd_histogram_{period[0]}_{period}'] - result[f'macd_histogram_{period[0]}_{period}_ma_{avg_period}']
            result[f'macd_histogram_{period[0]}_{period}_pct_change_vs_ma_{avg_period}'] = (result[f'macd_histogram_{period[0]}_{period}'] - result[f'macd_histogram_{period[0]}_{period}_ma_{avg_period}']) / result[f'macd_histogram_{period[0]}_{period}_ma_{avg_period}'] * 100

        result[f'macd_{period[0]}_prev'] = result['ema_fast'].shift(1)
        result[f'macd_signal_{period[1]}_prev'] = result['ema_slow'].shift(1)
        result[f'macd_{period[0]}_cross_up'] = (result[f'macd_{period[0]}_prev'] < result[f'macd_signal_{period[1]}_prev']) & (result[f'macd_{period[0]}'] > result[f'macd_signal_{period[1]}'])
        result[f'macd_{period[0]}_cross_down'] = (result[f'macd_{period[0]}_prev'] > result[f'macd_signal_{period[1]}_prev']) & (result[f'macd_{period[0]}'] < result[f'macd_signal_{period[1]}'])
        
    result['upper_band'], result['middle_band'], result['lower_band'] = talib.BBANDS(
            result['close'],
            timeperiod=boilinger_timeperiod[0],
            nbdevup=boilinger_timeperiod[1],
            nbdevdn=boilinger_timeperiod[1],
            matype=0
        )
    result[f'upper_band_rising'] = result[f'upper_band'].diff() > 0
    result[f'upper_band_dropping'] = result[f'upper_band'].diff() < 0
    result[f'upper_band_change'] = result['upper_band'].diff()
    result[f'upper_band_pct_change'] = result['upper_band'].pct_change() * 100
    
    result[f'middle_band_rising'] = result[f'middle_band'].diff() > 0
    result[f'middle_band_dropping'] = result[f'middle_band'].diff() < 0
    result[f'middle_band_change'] = result['middle_band'].diff()
    result[f'middle_band_pct_change'] = result['middle_band'].pct_change() * 100
    
    result[f'lower_band_rising'] = result[f'lower_band'].diff() > 0
    result[f'lower_band_dropping'] = result[f'lower_band'].diff() < 0
    result[f'lower_band_change'] = result['lower_band'].diff()
    result[f'lower_band_pct_change'] = result['lower_band'].pct_change() * 100
    
    result['lower_band_buy_signal'] = (result['close'] < result['lower_band']).astype(int)  # Cena poniżej dolnej wstęgi - sygnał kupna
    result['upper_band_sell_signal'] = (result['close'] > result['upper_band']).astype(int)  # Cena powyżej górnej wstęgi - sygnał sprzedaży
    
    result['stoch_k'], result['stoch_d'] = talib.STOCH(
        result['high'],
        result['low'],
        result['close'],
        fastk_period=stochastic_timeperiods[0],
        slowk_period=stochastic_timeperiods[1],
        slowk_matype=0,
        slowd_period=stochastic_timeperiods[1],
        slowd_matype=0
    )
    
    result[f'stoch_k_rising'] = result[f'stoch_k'].diff() > 0
    result[f'stoch_k_dropping'] = result[f'stoch_k'].diff() < 0
    result[f'stoch_k_change'] = result['stoch_k'].diff()
    result[f'stoch_k_pct_change'] = result['stoch_k'].pct_change() * 100
    
    result[f'stoch_d_rising'] = result[f'stoch_d'].diff() > 0
    result[f'stoch_d_dropping'] = result[f'stoch_d'].diff() < 0
    result[f'stoch_d_change'] = result['stoch_d'].diff()
    result[f'stoch_d_pct_change'] = result['stoch_d'].pct_change() * 100
    
    result['stoch_buy_signal'] = (result['stoch_k'] > result['stoch_d']) & (result['stoch_k'].shift(1) <= result['stoch_d'].shift(1))
    result['stoch_buy_signal_2'] = (result['stoch_k'] > stoch_buy_value) & (result['stoch_k'].shift(1) <= stoch_buy_value)
    result['stoch_buy_signal_combined'] = result['stoch_buy_signal'] | result['stoch_buy_signal_2']
    
    result['stoch_rsi_k'], result['stoch_rsi_d'] = talib.STOCHRSI(
        result['close'],
        timeperiod=stochastic_rsi_timeperiods[0],
        fastk_period=stochastic_rsi_timeperiods[1],
        fastd_period=stochastic_rsi_timeperiods[1],
        fastd_matype=0
    )
        
    result[f'stoch_rsi_k_rising'] = result[f'stoch_rsi_k'].diff() > 0
    result[f'stoch_rsi_k_dropping'] = result[f'stoch_rsi_k'].diff() < 0
    result[f'stoch_rsi_k_change'] = result['stoch_rsi_k'].diff()
    result[f'stoch_rsi_k_pct_change'] = result['stoch_rsi_k'].pct_change() * 100
    
    result[f'stoch_rsi_d_rising'] = result[f'stoch_rsi_d'].diff() > 0
    result[f'stoch_rsi_d_dropping'] = result[f'stoch_rsi_d'].diff() < 0
    result[f'stoch_rsi_d_change'] = result['stoch_rsi_d'].diff()
    result[f'stoch_rsi_d_pct_change'] = result['stoch_rsi_d'].pct_change() * 100
    
    # Dodanie sygnałów kupna i sprzedaży
    result['stoch_rsi_buy_signal'] = (result['stoch_rsi_k'] > result['stoch_rsi_d']) & (result['stoch_rsi_k'].shift(1) < result['stoch_rsi_d'].shift(1)).astype(int)
    result['stoch_rsi_sell_signal'] = (result['stoch_rsi_k'] < result['stoch_rsi_d']) & (result['stoch_rsi_k'].shift(1) > result['stoch_rsi_d'].shift(1)).astype(int)
        
    result['typical_price'] = (result['high'] + result['low'] + result['close']) / 3
    result['vwap'] = (result['typical_price'] * result['volume']).cumsum() / result['volume'].cumsum()
    result[f'vwap_rising'] = result[f'vwap'].diff() > 0
    result[f'vwap_dropping'] = result[f'vwap'].diff() < 0
    result[f'vwap_change'] = result['vwap'].diff()
    result[f'vwap_pct_change'] = result['vwap'].pct_change() * 100
    # Dodawanie kolumn sygnałów
    result['vwap_buy_signal'] = (result['close'] > result['vwap']).astype(int)  # Sygnał kupna, gdy cena > VWAP
    result['vwap_sell_signal'] = (result['close'] < result['vwap']).astype(int)  # Sygnał sprzedaży, gdy cena < VWAP
    # Możesz dodać kolumny z sygnałami na podstawie przecięć VWAP
    result['vwap_cross_up'] = ((result['close'] > result['vwap']) & (result['close'].shift(1) <= result['vwap'].shift(1))).astype(int)  # Cross up: cena przekroczyła VWAP
    result['vwap_cross_down'] = ((result['close'] < result['vwap']) & (result['close'].shift(1) >= result['vwap'].shift(1))).astype(int)  # Cross down: cena opuściła VWAP
    
    result['psar'] = talib.SAR(
        result['high'],
        result['low'],
        acceleration=psar_acceleration,
        maximum=psar_maximum
    )
    result[f'psar_rising'] = result[f'psar'].diff() > 0
    result[f'psar_dropping'] = result[f'psar'].diff() < 0
    result[f'psar_change'] = result['psar'].diff()
    result[f'psar_pct_change'] = result['psar'].pct_change() * 100
    
    # Dodajemy kolumny z sygnałami kupna i sprzedaży
    result['buy_signal'] = (result['psar'] < result['close']).astype(int)  # PSAR poniżej ceny = sygnał kupna
    result['sell_signal'] = (result['psar'] > result['close']).astype(int)  # PSAR powyżej ceny = sygnał sprzedaży
    # Możesz również dodać sygnały na podstawie zmian PSAR (czyli zmiana z poniżej na powyżej lub odwrotnie)
    result['psar_cross_up'] = (result['psar'] < result['close']) & (result['psar'].shift(1) > result['close'].shift(1))  # Cross from down to up (buy signal)
    result['psar_cross_down'] = (result['psar'] > result['close']) & (result['psar'].shift(1) < result['close'].shift(1))  # Cross from up to down (sell signal)
    # Sygnał kupna na podstawie przecięcia PSAR z ceną (cross up)
    result['buy_signal_cross'] = result['psar_cross_up'].astype(int)
    # Sygnał sprzedaży na podstawie przecięcia PSAR z ceną (cross down)
    result['sell_signal_cross'] = result['psar_cross_down'].astype(int)
        
    result['ma_200'] = result['close'].rolling(window=200).mean()
    result[f'ma_200_rising'] = result[f'ma_200'].diff() > 0
    result[f'ma_200_dropping'] = result[f'ma_200'].diff() < 0
    result[f'ma_200_change'] = result['ma_200'].diff()
    result[f'ma_200_pct_change'] = result['ma_200'].pct_change() * 100
    result['ma_200_buy_signal'] = (result['close'] > result['ma_200'])
    result['ma_200_sell_signal'] = (result['close'] < result['ma_200'])
  
    result['ma_50'] = result['close'].rolling(window=50).mean()
    result[f'ma_50_rising'] = result[f'ma_50'].diff() > 0
    result[f'ma_50_dropping'] = result[f'ma_50'].diff() < 0
    result[f'ma_50_change'] = result['ma_50'].diff()
    result[f'ma_50_pct_change'] = result['ma_50'].pct_change() * 100
    result['ma_50_buy_signal'] = (result['close'] > result['ma_50'])
    result['ma_50_sell_signal'] = (result['close'] < result['ma_50'])

    result['ma_50_200_buy_signal'] = (result['ma_50'] > result['ma_200']) & (result['ma_50'].shift(1) <= result['ma_200'].shift(1))
    result['ma_50_200_sell_signal'] = (result['ma_50'] < result['ma_200']) & (result['ma_50'].shift(1) >= result['ma_200'].shift(1))
  
    return result