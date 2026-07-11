"""
Custom exceptions for feed management.
"""


class FeedConfigurationError(Exception):
    """
    Raised when feed configuration validation fails.
    """

    pass


class FeedRegistryError(Exception):
    """
    Raised when feed registry operation fails.
    """

    pass