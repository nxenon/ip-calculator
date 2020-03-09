def BinaryOctet(num):
    '''define a function to correct a binary number to 8 lenght binary number'''
    splited_num = bin(num).split("b")
    binary_num = splited_num[1]
    if len(binary_num) == 1 :
        adding_zeros = "0000000"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 2 :
        adding_zeros = "000000"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 3 :
        adding_zeros = "00000"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 4 :
        adding_zeros = "0000"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 5 :
        adding_zeros = "000"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 6 :
        adding_zeros = "00"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 7 :
        adding_zeros = "0"
        new_num = adding_zeros + binary_num
        return new_num
    elif len(binary_num) == 8 :
        adding_zeros = ""
        new_num = adding_zeros + binary_num
        return new_num

def DecimalConversion(num):
    new_num = "0b" + num
    decimal_num = int(new_num,2)
    return str(decimal_num)