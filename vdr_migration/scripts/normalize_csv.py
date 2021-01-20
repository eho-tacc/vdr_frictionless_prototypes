import  os
import pandas as pd
import logging
import argparse

logging.basicConfig(level=logging.INFO)


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', help='file path(s) of CSV files to normalize', required=True, nargs="+")
    return vars(parser.parse_args())


def get_appended_fp(fp, suffix):
    path, ext = os.path.splitext(fp)
    return f"{path}{suffix}{ext}"


def main(files, fill_value=str()):
    norm_cols = pd.CategoricalIndex(list())
    # get union of unique field names
    for fp in files:
        df = pd.read_csv(fp, nrows=5)
        norm_cols = norm_cols.union(df.columns, sort=False)
    for fp in files:
        # get appended file name
        new_fp = get_appended_fp(fp, "_normalized")
        # load as dataframe
        # should be small enough to fit in memory, see xarray.Dataset or
        # Dask arrays if we prefer lazy loading
        df = pd.read_csv(fp)
        # fill missing columns with empty value
        logging.info(f"Normalizing columns in CSV '{fp}', writing to '{new_fp}'")
        for col in norm_cols:
            if col not in df.columns:
                logging.debug(f"File at '{fp}' is missing column '{col}'. " +
                              f"Adding fill value '{fill_value}' for this column.")
                df[col] = fill_value
        # write to new fp
        df.to_csv(new_fp, index=False)


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)

