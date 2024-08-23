####################### FOR TRIAL PURPOSES #################################
import numpy as np
from fractions import Fraction
from decimal import Decimal, getcontext
import math

def hex_to_num(num):
    """Converts the number that is greater than 9 to a hexadecimal value"""
    return ord(num)-55

def num_to_hex(num):
    """Converts the hexadecimal value that is greater than 9 to a decimal value"""
    return chr(num+55)

def is_letter(char):
    """Checks if the value is a letter"""
    return char.isalpha()

def is_float(string, base):
    """Checks if the string resembles a floating point value"""
    # Handle non-hexadecimal cases (base 2-10 & 11-36)
    if base != 16:  
        if "." not in string:
            return False 
        try:
            whole_part, decimal_part = string.split(".")
            
            whole_list = convert_to_base(whole_part, base)
            if whole_list is False:  
                return False
    
            decimal_list = convert_to_base(decimal_part, base)
            if decimal_list is False:
                return False
            return True
        except ValueError:
            return False
  # Special handling for hexadecimal values (base 16)
    try:
        # Attempt to convert the entire string as a hexadecimal number
        int(string, base=16)
        # Entire string is a valid hex number, not a float
        return False  
    except ValueError:
        # If conversion fails, proceed with checking for a valid decimal part
        if "." not in string:
            return False 
        try:
            whole_part, decimal_part = string.split(".")

            whole_list = convert_to_base(whole_part, 16)
            if whole_list is False:  
                return False

            decimal_list = convert_to_base(decimal_part, 16)
            if decimal_list is False: 
                return False

            return True
        except ValueError:
            return False

def convert_hex(list):
    """Iterates throughout the list to convert any value greater than 9 to a hexadecimal value"""
    for i, item in enumerate(list):
        if is_letter(item):
            list[i] = str(hex_to_num(item))
    return list

def convert_num(list):
    """Iterates throughout the list to convert any hexadecimal value to a numerical value"""
    for i, item in enumerate(list):
        if item>9:
            list[i] = str(num_to_hex(item))
    return list

def base_check(base):
    """Checks base if it is numeric and within the limit between 2 to 36"""
    if base.isnumeric() == False:
        return False
    elif (int(base) < 2 or int(base) > 36):
        return False
    else:
        return True

def base_from_input(base_from):
    """Asks user for the base of the number to be converted
       
       It raises an error if the base is less than 2 or greater than 36

       The error is received as an exception which is handled by returning False which triggers an action in GUI
    """
    try:
        if base_check(base_from) == True:
            return base_from
        else:
            raise ValueError("Limit base from 2 to 36")
    except ValueError:
        return False

def base_to_input(base_to):
    """Asks user for the base in which the number is to be converted
       
       It raises an error if the base is less than 2 or greater than 36

       The error is received as an exception which is handled by returning False which triggers an action in GUI
    """
    try:
        if base_check(base_to) == True:
            return base_to
        else:
            raise ValueError("Limit base from 2 to 36")
    except ValueError:
        return False

def user_base_check(list, base):
    """Checks if the input that has been converted to a list is greater than the base it is converted from"""
    i=0
    ans = False
    while i<len(list):
        if (int(list[i])<base):
            ans = True
            i+=1
        else:
            ans = False
            break
    return ans

def handle_negatives(user_input):
    """Removes leading negative sign from user input (if present)."""
    if user_input.find("-") != -1:
        return user_input.replace("-", "")
    else:
        return user_input
    
def split_float(user_input, base):
    """Splits a string containing a decimal point into integer and float parts."""
    if is_float(user_input, base):
        user_list = user_input.split(".")
        return list(user_list[0]), list(user_list[1])

def convert_to_base(user_input, base):
    """Converts user input to a list of integers in the specified base."""
    converted_list = convert_hex(list(user_input))
    # print(converted_list)
    try:
        if user_base_check(converted_list, base):
            return converted_list
        else:
            raise ValueError("Invalid characters for base", base)
    except ValueError:
        return False

def handle_float_conversion(int_part, float_part, base1):
    """Converts integer and float parts of a number separately."""
    int_part = "".join(int_part)
    float_part = "".join(float_part)
    converted_int = convert_to_base(str(int_part), base1)
    converted_float = convert_to_base(str(float_part), base1)
    return converted_int, converted_float

def user_input(user_input, base1):
    """Gets user input, validates it, and converts it to the desired base.

    Args:
        base1: The base of the user input.
        base2: The base to convert the user input to.

    Returns:
        A tuple containing the converted integer and float parts (if applicable) in base2.

    Raises:
        ValueError: If the user input is invalid.
    """
    while True:
        user_input = handle_negatives(user_input)
        if is_float(user_input, base1) == True:
            int_part, float_part = split_float(user_input, base1)
            int_part, float_part = handle_float_conversion(int_part, float_part, base1)
            return int_part, float_part
        else:
            int_list = convert_to_base(user_input, base1)
            return int_list

def int_dec_to_n(int_val, base):
    """Converts the integer part of the user-inputted decimal value to the desired base with appropriate spacing"""
    int_list = []
    group_count = 0 
    while int_val > 0:
        remainder = int_val % base
        if remainder > 9:
            remainder = num_to_hex(remainder)
        int_list.append(str(remainder))
        group_count += 1
        int_val //= base
        if (base == 10 or base == 8) and int_val > 0 and group_count % 3 == 0:
            if base == 10:
                int_list.append(",")
            else:
                int_list.append(" ")
            group_count = 0
        elif int_val > 0 and group_count % 4 == 0:
            int_list.append(" ")
            group_count = 0
    res_int = "".join(int_list[::-1])
    return res_int

def float_dec_to_n(float_val, base):
    """Converts the floating-point part of the user-inputted decimal value to the desired base with appropriate spacing"""
    float_list = []
    float_val_iteration = 0
    max_iterations = 30
    float_val = Fraction(float_val).limit_denominator()  # Convert float_val to Fraction for better accuracy

    while float_val % 1 != 0 and float_val_iteration < max_iterations:
        remainder = int(float_val * base)
        if remainder > 9:
            remainder = num_to_hex(remainder)
        float_list.append(str(remainder))
        float_val = (float_val * base) % 1
        float_val_iteration += 1

        if base not in (10, 8) and float_val_iteration > 0 and float_val_iteration % 4 == 0:
            float_list.append(" ")
        elif base == 8 and float_val_iteration % 3 == 0:
            float_list.append(" ")

    if float_val_iteration == max_iterations:
        float_list.append("...")

    res_float = "".join(float_list)
    return res_float

    
def int_n_to_dec(int_val, base):
    """Converts the integer part of the user-inputted value to a decimal value"""
    i = 0
    int_val.reverse()
    int_val_list = np.array(int_val, dtype=int)
    dec_int = 0

    while(i<=len(int_val)-1):
        dec_int += int_val_list[i]*(base**i)
        i+=1
    return dec_int

def float_n_to_dec(float_val, base):
    """Converts the floating-point part of the user-inputted value to a decimal value"""
    i = 0
    float_exp = 1
    float_val_list = np.array(float_val, dtype=int)
    dec_float = 0
    while(i<=len(float_val)-1):
        dec_float += float_val_list[i]*(base**-float_exp)
        i+=1
        float_exp+=1
    return dec_float

def twos_complement(user_input, int_val, base):
    """Reverses the integer value of the converted binary value
       
       0 value are inverted to 1 while 1 value is inverted to 0
       
       It adds one after the process
    """
    if is_float(user_input, base) == True:
        return "N/A"
    else:
        int_val = str(int_val).replace('1','2')
        int_val = str(int_val).replace('0','1')
        int_val = str(int_val).replace('2','0')

        int_list = list(int_val)
        i = 0
        while i < len(int_list):
            if int_list[i] == " ":
                del int_list[i]
            else:
                i += 1
        int_list.reverse()
        new_int_list = np.array(int_list, dtype=int)
        j = 0
        added = 1
        while j<=len(new_int_list)-1:
            new_int_list[j] = new_int_list[j] + added
            if new_int_list[j] == 2:
                new_int_list[j] = 0
            else:
                added = 0

            if j%5 == 0:
                new_int_list = np.insert(new_int_list, j, 5)
                j += 1
            j+=1

        final_string = "".join(map(str, new_int_list.tolist())) [::-1]  # Used map for efficient string conversion
        final_string = final_string.replace("5", " ")
        return final_string

def convert_process(base1, base2, input_string):
    """This is the whole process of conversion
    
       Returns the integer and float value to be used in string_return
    """
    if is_float(input_string, base1) == True:
        input_int, input_float = user_input(input_string, base1)
    else:
        input_int = user_input(input_string, base1)
    
    dec_int = int_n_to_dec(input_int, base1)
    n_int = int_dec_to_n(dec_int, base2)
    
    if is_float(input_string, base1) == True:
        dec_float = float_n_to_dec(input_float, base1)
        n_float = float_dec_to_n(dec_float, base2)
    else:
        n_float = 0

    return n_int, n_float

def string_return(input_string, n_int, n_float, base):
    """Gets the values from the conversion process
       
       Returns the values to be printed based on which condition applies
    """
        # .search is used in the front end
    if is_float(input_string, base) == True:
        if(not input_string.find("-")==-1):
            return "-" + n_int + "." + n_float
        else:
            return n_int + "." + n_float
    else:
        if(not input_string.find("-")==-1):
            return "-" + n_int
        else:
            return n_int