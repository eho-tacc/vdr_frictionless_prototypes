# Versioned Datasets -> Frictionless Migration

## Installation

Validation was performed using [frictionless-py](https://github.com/frictionlessdata/frictionless-py) `5bd794179dcbaab080e1e0d0e692b6c875e44d43`. As of writing (1/13/21), this is the only stable commit that avoids [#609](https://github.com/frictionlessdata/frictionless-py/issues/609) and [#616](https://github.com/frictionlessdata/frictionless-py/issues/616).

## Strip Comments

As of `5bd794179dcbaab080e1e0d0e692b6c875e44d43`, Frictionless CLI does not respect `dialect/commentChar`. We have to strip the metadata in the comments manually, before loading CSVs into Frictionless:
```bash
python3 scripts/split_comments.py --out-fp data/TwoSix_100K_stab_scores_1.csv ${VERSIONED_DATASETS_REPOSITORY}/data/protein-design/experimental_stability_scores/TwoSix_100K.v4.experimental_stability_scores.csv
```
This generates a data (`*.csv`) file and a comments (`*.comments.txt`) file in the `data` directory.

## Validation

From the root of this directory:
```bash
frictionless validate --nopool datapackage.json
```

`--nopool` avoids [#615](https://github.com/frictionlessdata/frictionless-py/issues/615).
