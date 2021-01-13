import pandas as pd
import logging
import argparse


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ladder-fp', help='file path of ladder CSV', required=True, type=str)
    parser.add_argument('--stab-scores-fp', help='file path of stability scores CSV (for more recent chip)', required=True, type=str)
    parser.add_argument('--chip-dataset', help='str value that should populate "chip-dataset" column in `ladder-fp`', required=False, type=str)
    return vars(parser.parse_args())


def main(ladder_fp, stab_scores_fp, chip_dataset=None):
    # load the new_ladder_file
    lad = pd.read_csv(ladder_fp)
    # load the stability scores file
    stab = pd.read_csv(stab_scores_fp)
    # try to get the dataset name from stab scores, if not provided
    if chip_dataset is None:
        try:
            chip_dataset = stab.dataset.unique().tolist()[0]
        except (IndexError, AttributeError):
            logging.error(f"Error getting a unanimous value for `dataset` from '{stab_scores_fp}'")
            raise

    # assign column values and write the ladder file
    assert chip_dataset is not None
    lad['chip_dataset'] = chip_dataset
    lad.to_csv(ladder_fp, index=False)


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)

