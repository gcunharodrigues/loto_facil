import csv

filename = 'data/loto_facil_compiled_draws_2345.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header = next(reader)
    print(header)