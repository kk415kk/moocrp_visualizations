import sys

filename=sys.argv[1]
fp = open(filename,'r')

print fp.readline().rstrip("\n")
for line in fp:
  row = line.split(',')
  if not(float(row[0]) == 0.0):
    print line.rstrip("\n")
