
def get_commission(sum: int, percent: str) -> float:
    return sum - (sum/100 * float(percent))
