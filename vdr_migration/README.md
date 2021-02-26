# Versioned Datasets -> Frictionless Migration

## Installation

Validation was performed using [frictionless-py](https://github.com/frictionlessdata/frictionless-py) `5bd794179dcbaab080e1e0d0e692b6c875e44d43`. As of writing (1/13/21), this is the only stable commit that avoids [#609](https://github.com/frictionlessdata/frictionless-py/issues/609) and [#616](https://github.com/frictionlessdata/frictionless-py/issues/616).

## Strip Comments

As of `5bd794179dcbaab080e1e0d0e692b6c875e44d43`, Frictionless CLI does not respect `dialect/commentChar` ([#610](https://github.com/frictionlessdata/frictionless-py/issues/610)). We have to strip the metadata in the comments manually, before loading CSVs into Frictionless:
```bash
python3 scripts/split_comments.py --out-fp data/TwoSix_100K_stab_scores_1.csv ${VERSIONED_DATASETS_REPOSITORY}/data/protein-design/experimental_stability_scores/TwoSix_100K.v4.experimental_stability_scores.csv
```
This generates a data (`*.csv`) file and a comments (`*.comments.txt`) file in the `data` directory.

## Normalize to 1NF

Normalization to 1NF was performed in the iPython notebook [20210223_1nf.ipynb](./notebooks/20210223_1nf.ipynb). In short, the notebook finds an optimal partition of data files into tables, based on columns that are unique to groups of data files. It then uses the utilities in [normalize_csv.py](./scripts/normalize_csv.py) to add empty columns to files where necessary.

## (Optional) Split Large Data Files

GitHub restricts upload of files >100 MB unless using git-lfs. In order to accommodate this restriction, the utility [split_large_csv.py](./scripts/split_large_csv.py) was used to split each large CSV file into two smaller ones.

## Validation Using Frictionless CLI

From the root of this directory:
```bash
frictionless validate --nopool datapackage.json
```

`--nopool` avoids [#615](https://github.com/frictionlessdata/frictionless-py/issues/615).
