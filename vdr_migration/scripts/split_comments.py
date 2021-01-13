import os
import logging
import argparse


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_fp', help='file path of CSV to split', type=str)
    parser.add_argument('--out-fp', help='output file path', type=str,
                        required=False, default=None)
    return parser.parse_args()


def main(fp, out_fp, comment_char="#"):
    if out_fp is None:
        out_fp = fp
    comments = list()
    data = list()

    # read
    with open(fp) as f:
        for line in f.readlines():
            if line.startswith(comment_char):
                comments.append(line)
            else:
                data.append(line)

    # leave it be if there are no comments
    # if not comments:
    #     logging.debug(f"No comments in '{fp}'")
    #     return

    # get comment fp
    pre, ext = os.path.splitext(out_fp)
    comment_fp = f"{pre}.comments.txt"
    logging.debug(f"comment_fp: {comment_fp}")

    # write comments
    with open(comment_fp, 'w') as f:
        for item in comments:
            f.write(f"{item}")

    # write data
    with open(out_fp, 'w') as f:
        for item in data:
            f.write(f"{item}")


if __name__ == '__main__':
    opts = get_opts()
    main(fp=opts.csv_fp, out_fp=opts.out_fp)
