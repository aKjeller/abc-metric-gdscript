import os
import math
import re
import requests

# TODO: 
# Make it work for folders
def calculate_abc_metric(path, data=None):
    if data is None:
        data = read_file(path)
    
    a = find_a(data)
    b = find_b(data)
    c = find_c(data)

    # Debug
    print('A: {}'.format(a))
    print('B: {}'.format(b))
    print('C: {}'.format(c))
    print()

    # Return sqrt( a^2 + b^2 + c^2 )
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2) + math.pow(c, 2))

# TODO: 
# Exclude constant declarations and default parameter assignments (is "onready var close_btn: Button = $Close" constant declaration?)
# Check for missmatches
def find_a(code):
    # Pattern to find: = += -= *= /= %= &= |= <<= >>= ++ --
    pattern = re.compile(r' = | \+= | -= | \*= | /= | %= | &= | \|= | <<= | >>= |\+\+|--')
    res = re.findall(pattern, code)
    return len(res)

# TODO: 
# Add the occurrence of a function call or a class method call.
# Add the occurrence of a ‘new’ operator. (GDscript has .new() and .instance() instead of new? (So they are function calls?))
def find_b(code):
    return 0

# TODO: 
# Add the occurrence of the GDscript equivalent of thefollowing keywords (‘else’, ‘case’, ‘default’, ‘?’, ‘try’, ‘catch’). 
# Add the occurrence of a unary conditional operator.
# Check for missmatches
def find_c(code):
    # Pattern to find: < > == != >= <=
    pattern = re.compile(r' < | > | == | != | >= | <= ') # Add 'else:' here?
    res = re.findall(pattern, code)
    return len(res)

# Read file at file_path and return contents as a string
def read_file(file_path):
    if os.path.isfile(file_path):
        file = open(file_path, "r")  
        data = file.read()
        file.close()
        return data
    else:
        print("No file found at path")
        return None

# TODO: 
# Add arguments i.e. path
if __name__ == '__main__':
    response = requests.get('https://raw.githubusercontent.com/aKjeller/group-10-smce-gd/code_editor/project/src/ui/code_editor/MainWindow.gd')
    abc = calculate_abc_metric('', response.text)
    print('ABC: {}'.format(round(abc, 1)))