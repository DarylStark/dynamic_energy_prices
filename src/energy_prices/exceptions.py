""" Exceptions for the script """


class EnergyPricesException(Exception):
    """ Generic base class for exceptions """
    pass


class ConfigLoadError(EnergyPricesException):
    """ Error when config couldn't be loaded """
    pass
