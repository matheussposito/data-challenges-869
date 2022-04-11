# pylint: disable=missing-docstring

# TODO: add some currency rates
RATES = {
    'USDEUR': 0.85,
    'GBPEUR': 1.13,
    'CHFEUR': 0.86,
    'EURGBP': 0.885
    }

def convert(amount, currency):
    """returns the converted amount in the given currency
    amount is a tuple like (100, "EUR")
    currency is a string
    """
    rate = RATES.get(amount[1]+currency)
    print(rate)
    if rate:
        return round(rate*amount[0])
    return rate
