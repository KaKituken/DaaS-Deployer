import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', required=True, help="path to input dataset")
parser.add_argument('-o', '--output', required=True, help="path to output dataset")
parser.add_argument('-t', '--type', required=True, help="type of dataset")

args = parser.parse_args()

print(args)