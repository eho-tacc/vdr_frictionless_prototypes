# dialect/commentChar is not respected during extraction

# Overview

In a Tabular Data Resource, [`dialect/commentChar`](https://specs.frictionlessdata.io/csv-dialect/#specification) is not respected when extracting from CSV. Attempting to extract from a Data Resource with a comment character raises the following error. The error is the same if `dialect` field is removed from `dataresource.json`.

```bash
$ frictionless validate dataresource.json
---
invalid: data.csv
---

===  =====  ==========  ===============================================================
row  field  code        message
===  =====  ==========  ===============================================================
  2      2  extra-cell  Row at position "2" has an extra value in field at position "2"
  3      2  extra-cell  Row at position "3" has an extra value in field at position "2"
  4      2  extra-cell  Row at position "4" has an extra value in field at position "2"
  5      2  extra-cell  Row at position "5" has an extra value in field at position "2"
===  =====  ==========  ===============================================================
```

# Details to Reproduce

```bash
$ tree .
.
├── data.csv
└── dataresource.json
```

`data.csv`:
```csv
# some metadata
user,balance
fred,0
george,100
bill,10
```

`dataresource.json`:
```json
{
    "name": "data",
    "path": "data.csv",
    "profile": "tabular-data-resource",
    "dialect": {
        "commentChar": "#"
    }
}
```

## Environment

```bash
$ frictionless --version
3.48.0
$ python --version
Python 3.8.3
$ echo $SHELL
/bin/zsh
```

---

Please preserve this line to notify @roll (lead of this repository)
