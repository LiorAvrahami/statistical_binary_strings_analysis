import itertools

def get_all_n_digit_strings(n):
    digits_possibilities = [["0", "1"]] * n
    all_n_digit_bit_arrays = itertools.product(*digits_possibilities)
    return ["".join(bit_array) for bit_array in all_n_digit_bit_arrays]

def get_all_couples(arr):
    return list(itertools.product(arr,arr))

def get_all_couples_minimal(arr):
    couples_full = get_all_couples(arr)
    large_couples_only = [c for c in couples_full if c > (c[1],c[0])] # extract only the "large" pairs
    return large_couples_only