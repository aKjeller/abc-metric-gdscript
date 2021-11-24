import os
import math
import re
import requests
import glob

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
# Check for missmatches
def find_b(code):
    b = 0

    # Pattern to find all lines containing a function call
    pattern = re.compile(r'.*\(.*(?!\n)')
    res = re.findall(pattern, code)
    if len(res) > 0:
        for r in res:
            pattern = re.compile(r'\w\(') # All function calls
            res = re.findall(pattern, r)
            if '#' not in r: # Remove comments
                b += len(res)

                pattern = re.compile(r'func|while|match') # Remove: func, while, match
                res = re.findall(pattern, r)
                b -= len(res)
    return b

# TODO: 
# Add the occurrence of the GDscript equivalent of thefollowing keywords (‘?’, ‘try’, ‘catch’). 
# Add the occurrence of a unary conditional operator.
# Check for missmatches
def find_c(code):
    c = 0

    # Pattern to find: < > == != >= <= else:
    pattern = re.compile(r' < | > | == | != | >= | <= |else:') # Add 'else:' here?
    res = re.findall(pattern, code)
    c += len(res)

    # Pattern to find switch case blocks
    pattern = re.compile(r'((.*)match(.|\n\2\t)*)')
    res = re.findall(pattern, code)
    if len(res) > 0:
        for r in res:
            pattern = re.compile(r'\n{}\t(?!\t)'.format(r[1]))
            res = re.findall(pattern, r[0])
            c += len(res)

    return c

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
    # response = requests.get('https://raw.githubusercontent.com/aKjeller/group-10-smce-gd/code_editor/project/src/ui/code_editor/MainWindow.gd')
    #response = requests.get('https://raw.githubusercontent.com/aKjeller/group-10-smce-gd/code_editor/project/src/ui/code_editor/FileTree.gd') # Contains a match statement
    #abc = calculate_abc_metric('', response.text)
    #print('ABC: {}'.format(round(abc, 1)))
    path = 'C:\SEP\smce-gd'
    filelist = glob.glob(path + '/**/*.gd', recursive=True)
    for x in range(len(filelist)):
        abc = calculate_abc_metric('', filelist[x])
        print(filelist[x], abc)