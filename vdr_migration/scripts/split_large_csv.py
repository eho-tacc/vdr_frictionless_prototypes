import os
import pandas as pd
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', help='file path(s) of CSV files to split',
                        required=True, nargs="+")
    parser.add_argument('--out-dir', help='directory in which to write output files. Omitting will write files to same directory as source files.',
                        required=False, default=None)
    parser.add_argument('--overwrite', help='whether to overwrite output paths, even if they already exist',
                        required=False, action='store_true', default=False)
    parser.add_argument('--max-size', help='maximum allowed file size, in MB',
                        required=False, default=100)
    return vars(parser.parse_args())

def get_appended_fp(fp, suffix, out_dir=None):
    path, ext = os.path.splitext(fp)
    # cd to out_dir if specified
    if out_dir is not None:
        assert os.path.isdir(out_dir)
        in_dir, fname = os.path.split(path)
        path = os.path.join(out_dir, fname)
    return f"{path}{suffix}{ext}"


def main(files, out_dir, overwrite=False, max_size=100):
    for fp in files:
        fsize = os.path.getsize(fp) * 10**-6
        if fsize > max_size:
            logging.info(f"file '{fp}' is greater than {max_size} MB " +
                         f"({fsize:.2f} MB). Splitting CSV file...")
            large_df = pd.read_csv(fp)
            midpoint = int(len(large_df) / 2)
            dfs = [large_df.iloc[:midpoint], large_df.iloc[midpoint:]]
            for idx, df in enumerate(dfs):
                new_fp = get_appended_fp(fp, f"_{idx}", out_dir=out_dir)
                if os.path.exists(new_fp):
                    if overwrite is not True:
                        raise FileExistsError(
                            f"Write path '{new_fp}' already exists. Pass --overwrite " +
                            f"if you are sure you want to overwrite this path.")
                    else:
                        logging.info(
                            f"Write path '{new_fp}' already exists. " +
                            f"Overwriting... (--overwrite was passed)")
                df.to_csv(new_fp, index=False)
        else:
            logging.debug(f"file '{fp}' is less than {max_size} MB " +
                          f"({fsize:.2f} MB). Skipping...")
    return None


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)

