import os
import math
import re
import glob
import sys

def main():
    folderpath = sys.argv[1]
    if(os.path.exists(folderpath)):
        calculate_abc_metric(folderpath)
    else:
        print('Incorrect folder path, Folder not found')

def calculate_abc_metric(folderpath):
    filelist = glob.glob(folderpath + '/**/*.gd', recursive=True)

    total_a = 0
    total_b = 0
    total_c = 0

    res_list = []

    for file in filelist:
        data = read_file(file)

        a = find_a(data)
        b = find_b(data)
        c = find_c(data)

        total_a += a
        total_b += b
        total_c += c

        res_list.append((math.sqrt(math.pow(a, 2) + math.pow(b, 2) + math.pow(c, 2)), file))

    res_list.sort(reverse=True)

    print('############################################')
    print('Total ABC score for the whole project: ')
    print(round(math.sqrt(math.pow(total_a, 2) + math.pow(total_b, 2) + math.pow(total_c, 2)), 1))
    print('############################################')
    print('ABC score for individual files:')
    for res in res_list:
        print(str(round(res[0], 1)) + "\t" + res[1])

def find_a(code):
    # Pattern to find: = += -= *= /= %= &= |= <<= >>= ++ --
    pattern = re.compile(r' = | \+= | -= | \*= | /= | %= | &= | \|= | <<= | >>= |\+\+|--')
    res = re.findall(pattern, code)
    return len(res)

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

main()