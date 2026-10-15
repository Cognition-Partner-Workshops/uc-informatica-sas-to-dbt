select
    CUSTOMER_ID,
    cast(SCORE_DATE as date) as SCORE_DATE,
    FICO_SCORE,
    VANTAGE_SCORE,
    BUREAU_INQS_6MO,
    BUREAU_TRADES_OPEN,
    BUREAU_DEROGS,
    cast(BUREAU_UTIL_PCT as float) as BUREAU_UTIL_PCT,
    BUREAU_OLDEST_TRADE_MO
from {{ source('source_sf', 'ORA_DW_BUREAU_SCORES') }}
