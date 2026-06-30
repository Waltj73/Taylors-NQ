# engine/exceptions.py

"""
Taylor NQ Custom Exceptions

Application-specific exception hierarchy.
"""


class TaylorError(Exception):
    """Base application exception."""


#
# Data
#

class DataError(TaylorError):
    """Generic data error."""


class DataDownloadError(DataError):
    """Unable to download market data."""


class InvalidDataError(DataError):
    """Downloaded data is invalid."""


class MissingColumnsError(DataError):
    """Required columns are missing."""


#
# Workbook
#

class WorkbookError(TaylorError):
    """Workbook error."""


class WorkbookLoadError(WorkbookError):
    """Workbook could not be loaded."""


class WorkbookVerificationError(WorkbookError):
    """Workbook verification failed."""


#
# Calculations
#

class CalculationError(TaylorError):
    """Calculation failure."""


#
# Signals
#

class SignalError(TaylorError):
    """Signal generation failure."""


#
# Yahoo
#

class YahooError(TaylorError):
    """Yahoo Finance error."""


class QuoteError(YahooError):
    """Unable to retrieve live quote."""


class HistoryError(YahooError):
    """Unable to retrieve historical data."""


#
# Session
#

class SessionError(TaylorError):
    """Trading session error."""


#
# Configuration
#

class ConfigurationError(TaylorError):
    """Configuration problem."""


#
# UI
#

class UIError(TaylorError):
    """UI rendering error."""
