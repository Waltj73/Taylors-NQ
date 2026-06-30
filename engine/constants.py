# engine/constants.py

"""
Taylor NQ Constants

Central location for application-wide constants.
"""

from __future__ import annotations

#
# Market
#

NQ_SYMBOL = "NQ=F"

#
# Timeframes
#

ONE_MINUTE = "1m"
TWO_MINUTE = "2m"
FIVE_MINUTE = "5m"
FIFTEEN_MINUTE = "15m"
THIRTY_MINUTE = "30m"
ONE_HOUR = "1h"
ONE_DAY = "1d"
ONE_WEEK = "1wk"
ONE_MONTH = "1mo"

DEFAULT_INTERVAL = ONE_DAY
DEFAULT_HISTORY = "2y"

#
# Display
#

PRICE_DECIMALS = 2

#
# Taylor Columns
#

OPEN = "Open"
HIGH = "High"
LOW = "Low"
CLOSE = "Close"
VOLUME = "Volume"

RALLY = "Rally"
RALLY_AVG = "RallyAvg3"

ANTICIPATED_HIGH_LOW = "AnticipatedHighFromLow"

BUYING_HIGH = "BuyingHigh"
BUYING_HIGH_AVG = "BuyingHighAvg3"

ANTICIPATED_HIGH_HIGH = "AnticipatedHighFromHigh"

PIVOT_HIGH = "PivotBreakoutHigh"

AVG_SELL = "AvgSell"

DECLINE = "Decline"
DECLINE_AVG = "DeclineAvg3"

YESTERDAY_HIGH_AVG = "YesterdayHighMinusAvg"

BUYING_LOW = "BuyingLow"
BUYING_LOW_AVG = "BuyingLowAvg3"

YESTERDAY_LOW_AVG = "YesterdayLowMinusAvg"

PIVOT_LOW = "PivotBreakoutLow"

AVG_BUY = "AvgBuy"

ALL_COLUMNS = [
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    VOLUME,
    RALLY,
    RALLY_AVG,
    ANTICIPATED_HIGH_LOW,
    BUYING_HIGH,
    BUYING_HIGH_AVG,
    ANTICIPATED_HIGH_HIGH,
    PIVOT_HIGH,
    AVG_SELL,
    DECLINE,
    DECLINE_AVG,
    YESTERDAY_HIGH_AVG,
    BUYING_LOW,
    BUYING_LOW_AVG,
    YESTERDAY_LOW_AVG,
    PIVOT_LOW,
    AVG_BUY,
]

#
# Day Types
#

BUY_DAY = "BUY DAY"
SELL_DAY = "SELL DAY"
BUY_SELL_DAY = "BUY/SELL DAY"
SELL_BUY_DAY = "SELL/BUY DAY"

#
# UI Colors
#

GREEN = "#00C853"
RED = "#D50000"
YELLOW = "#F9A825"
BLUE = "#1565C0"
GRAY = "#757575"

#
# Workbook
#

DEFAULT_WORKSHEET = 0

#
# Verification
#

DEFAULT_TOLERANCE = 0.01
