import os

directory = '/Users/brandonallen/Documents/GitHub/DSA-Compendium/Data Structures/Intermediate/Segment Tree/'
filename = 'output.txt'
data = list(range(100000))

file_path = os.path.join(directory, filename)

with open(file_path, 'w') as file:
    file.write(str(data))
