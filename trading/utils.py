from decimal import Decimal


def get_commission(sum: int, percent: str) -> Decimal:
    return sum - (sum/100 * Decimal(percent))