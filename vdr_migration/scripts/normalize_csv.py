import  os
import pandas as pd
import logging
import argparse

logging.basicConfig(level=logging.WARNING)


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', help='file path(s) of CSV files to normalize',
                        required=True, nargs="+")
    parser.add_argument('--out-dir', help='directory in which to write normalized files. Omitting will write normalized files to same directory as source files.',
                        required=False, default=None)
    parser.add_argument('--overwrite', help='whether to overwrite output paths, even if they already exist',
                        required=False, action='store_true', default=False)
    parser.add_argument('--sort-cols', help='whether to sort columns alphabetically',
                        required=False, action='store_true', default=True)
    return vars(parser.parse_args())


def get_appended_fp(fp, suffix, out_dir=None):
    path, ext = os.path.splitext(fp)
    # cd to out_dir if specified
    if out_dir is not None:
        assert os.path.isdir(out_dir)
        in_dir, fname = os.path.split(path)
        path = os.path.join(out_dir, fname)
    return f"{path}{suffix}{ext}"

def get_norm_cols(files):
    """get union of unique field names"""
    col_src = dict()
    norm_cols = list()
    for fp in files:
        df = pd.read_csv(fp, nrows=5)
        for col in df.columns:
            if col in norm_cols:
                col_src[col].append(fp)
            else:
                norm_cols.append(col)
                col_src[col] = [fp]
    # breakpoint()
    return norm_cols


def main(files, out_dir, overwrite=False, fill_value=str(), intersect_thresh=0.5,
         sort_cols=True):
    norm_cols = get_norm_cols(files)
    for fp in files:
        # get appended file name
        new_fp = get_appended_fp(fp, "_normalized", out_dir=out_dir)
        # warn if new_fp exists
        if os.path.exists(new_fp):
            if overwrite is not True:
                raise FileExistsError(
                    f"Write path '{new_fp}' already exists. Pass --overwrite " +
                    f"if you are sure you want to overwrite this path.")
            else:
                logging.info(
                    f"Write path '{new_fp}' already exists. " +
                    f"Overwriting... (--overwrite was passed)")
        # load as dataframe
        # should be small enough to fit in memory, see xarray.Dataset or
        # Dask arrays if we prefer lazy loading
        df = pd.read_csv(fp)
        # fill missing columns with empty value
        logging.info(f"Normalizing columns in CSV '{fp}', writing to '{new_fp}'")
        empty_cols = 0
        for col in norm_cols:
            if col not in df.columns:
                logging.debug(f"File at '{fp}' is missing column '{col}'. " +
                              f"Adding fill value '{fill_value}' for this column.")
                df[col] = fill_value
                empty_cols += 1

        # sort columns such that order is same as norm_cols
        if sort_cols:
            logging.debug(f"'sort_cols' flag is True. Sorting columns alphabetically...")
            df = df[norm_cols]

        # warn if too many empty columns were inserted
        tot_cols = float(len(df.columns))
        prop_empty = empty_cols / tot_cols
        if prop_empty > intersect_thresh:
            log_func = logging.warning
        else:
            log_func = logging.info
        log_func(f"Inserted {empty_cols} empty columns into the DataFrame " +
                 f"read from '{fp}'. This accounts for {(prop_empty * 100):.2f}% " +
                 f"of columns in this table.")

        # write to new fp
        df.to_csv(new_fp, index=False)


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)

