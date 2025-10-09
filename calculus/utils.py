import numpy as np

# convert a floating-point number 'x' in scientific format and return the related string in latex format
def to_latex_scientific(x):
    formatted = "{:.1e}".format(x)  # Convert to scientific notation with 3 significant figures
    base, exponent = formatted.split("e")  # Split into base and exponent

    base = float(base)  # Convert base to float to check if it's an integer
    exponent = int(exponent)  # Convert exponent to integer to remove leading zeros

    # Convert base to int if it is a whole number
    base_is_integer = base.is_integer()
    if base_is_integer:
        base = int(base)

    if x != 0:
        if exponent == 0:
            result = r"${}$".format(base)
        else:
            if base_is_integer and (np.abs(base) == 1):
                if base == 1:
                    result = r"$10^{{{}}}$".format(exponent)
                elif base == -1:
                    result = r"$-10^{{{}}}$".format(exponent)
            else:
                result = r"${} \times 10^{{{}}}$".format(base, exponent)

    else:
        result = r"$0$"
    return result

'''
compute the floor of a number with respect to multiples of 10
Input values: 
- 'x': the number

Output values: 
- the floor
'''
def floor_base_10(x):
    if x > 0:
        return (10.0 ** (np.floor(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.ceil(np.log10(-x))))
    elif x == 0:
        return 0

'''
compute the ceil of a number with respect to multiples of 10
Input values: 
- 'x': the number

Output values: 
- the ceil
'''
def ceil_base_10(x):
    if x > 0:
        return (10.0 ** (np.ceil(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.floor(np.log10(-x))))
    elif x == 0:
        return 0
