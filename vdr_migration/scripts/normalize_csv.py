import pandas as pd
import logging
import argparse


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', help='file path(s) of CSV files to normalize', required=True, nargs="+")
    return vars(parser.parse_args())


def main(files):
    norm_cols = pd.CategoricalIndex(list())
    # get union of unique field names
    for fp in files:
        df = pd.read_csv(fp, nrows=5)
        norm_cols = norm_cols.union(df.columns, sort=False)
    for fp in files:
        # get file name
        # get new file name
        pass

if __name__ == '__main__':
    opts = get_opts()
    main(**opts)

