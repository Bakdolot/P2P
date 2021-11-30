def get_correct_sum(sum: str, step_size: str) -> str:
    step_len = len(step_size.split('.')[1].split('1')[0]) + 1
    temp = sum.split('.')
    if len(temp) == 1:
        sum = temp[0] + '0' * step_len
        return sum
    sum_len = len(sum.split('.')[1])
    if sum_len > step_len:
        correct_sum = '.'.join([sum.split('.')[0], sum.split('.')[1][:step_len]])   #   потом оптимизирую
        return correct_sum
    diferent = step_len - sum_len
    correct_sum = '.'.join([sum.split('.')[0], sum.split('.')[1]+('0'*diferent)])
    return correct_sum


print(get_correct_sum('23.234', '0.0000010000'))
