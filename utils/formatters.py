# Function to format the big numbers into Billion, Million and Thousand Format
def format_number(num):
    if abs(num) >= 1e9:
        return f'${num/1e9:.2f}B'
    elif abs(num) >= 1e6:
        return f'${num/1e6:.2f}M'
    elif abs(num) >= 1e3:
        return f'${num/1e3:.2f}K'
    else:
        return f'${num:.2f}'