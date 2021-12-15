def convert_sum(sum: str, step_size: str) -> str:
    sum = sum.replace(',', '.')
    if not '1' in step_size.split('.')[1]:
        return sum.split('.')[0]
    step_len = len(step_size.split('.')[1].split('1')[0]) + 1
    currect_sum = f"%.{step_len}f" % round(float(sum), step_len)
    return currect_sum