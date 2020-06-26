import sys
for line in open(sys.argv[1]):
    split_line = line.split()
    if len(split_line) == 0:
        print
    else:
        sys.stdout.write(split_line[1] + ' ')