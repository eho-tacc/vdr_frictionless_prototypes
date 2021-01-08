# Validation tasks in mp.pool fail when serializing

# Overview

Validation tasks with `nopool=False` raise the following error (wrapped in a response with code `task-error`):
```
TypeError("cannot pickle '_hashlib.HASH' object")
```
This only occurs if `resource.schema` is a reference to a JSON file (#609, and #611). I suspect that this is an error during serialization when a validation task is in a `multiprocessing.pool`.

Validation passes if:
1. Pass `nopool=True` to `validate_package`
2. Other changes that I assume result in serial execution, such as:
    * Change the contents of `schema.json` to `{"fields": []}` or `{}`
    * Yank the JSON object from `schema.json` to the `schema` field, as an inline JSON object
    * Include only one of the `resources` in `datapackage.json`

# Details to Reproduce

I'm sure this is an error thrown in the lower-level API; apologies that I was not able to provide lower-level diagnosis.

```bash
$ python3 scripts/validate_package.py
{'version': '3.48.0', 'time': 0.765, 'valid': False, 'stats': {'errors': 1, 'tables': 0}, 'errors': [{'code': 'task-error', 'name': 'Task Error', 'tags': ['#general'], 'note': 'Error sending result: \'[{\'version\': \'3.48.0\', \'time\': 0.069, \'valid\': True, \'stats\': {\'errors\': 0, \'tables\': 1}, \'errors\': [], \'tables\': [{\'path\': \'data/data.csv\', \'scheme\': \'file\', \'format\': \'csv\', \'hashing\': \'md5\', \'encoding\': \'utf-8\', \'compression\': \'no\', \'compressionPath\': \'\', \'control\': {\'newline\': \'\'}, \'dialect\': {}, \'query\': {}, \'schema\': {\'fields\': [{\'name\': \'user\', \'type\': \'string\'}, {\'name\': \'balance\', \'type\': \'integer\'}]}, \'header\': [\'user\', \'balance\'], \'time\': 0.003, \'valid\': True, \'scope\': [\'dialect-error\', \'schema-error\', \'field-error\', \'extra-label\', \'missing-label\', \'blank-label\', \'duplicate-label\', \'blank-header\', \'incorrect-label\', \'extra-cell\', \'missing-cell\', \'blank-row\', \'type-error\', \'constraint-error\', \'unique-error\', \'primary-key-error\', \'foreign-key-error\', \'checksum-error\'], \'stats\': {\'hash\': \'8402358f59c6d1d178cd2f77cbf84e7a\', \'bytes\': 39, \'fields\': 2, \'rows\': 3, \'errors\': 0}, \'partial\': False, \'errors\': []}]}]\'. Reason: \'TypeError("cannot pickle \'_hashlib.HASH\' object")\'', 'message': 'The validation task has an error: Error sending result: \'[{\'version\': \'3.48.0\', \'time\': 0.069, \'valid\': True, \'stats\': {\'errors\': 0, \'tables\': 1}, \'errors\': [], \'tables\': [{\'path\': \'data/data.csv\', \'scheme\': \'file\', \'format\': \'csv\', \'hashing\': \'md5\', \'encoding\': \'utf-8\', \'compression\': \'no\', \'compressionPath\': \'\', \'control\': {\'newline\': \'\'}, \'dialect\': {}, \'query\': {}, \'schema\': {\'fields\': [{\'name\': \'user\', \'type\': \'string\'}, {\'name\': \'balance\', \'type\': \'integer\'}]}, \'header\': [\'user\', \'balance\'], \'time\': 0.003, \'valid\': True, \'scope\': [\'dialect-error\', \'schema-error\', \'field-error\', \'extra-label\', \'missing-label\', \'blank-label\', \'duplicate-label\', \'blank-header\', \'incorrect-label\', \'extra-cell\', \'missing-cell\', \'blank-row\', \'type-error\', \'constraint-error\', \'unique-error\', \'primary-key-error\', \'foreign-key-error\', \'checksum-error\'], \'stats\': {\'hash\': \'8402358f59c6d1d178cd2f77cbf84e7a\', \'bytes\': 39, \'fields\': 2, \'rows\': 3, \'errors\': 0}, \'partial\': False, \'errors\': []}]}]\'. Reason: \'TypeError("cannot pickle \'_hashlib.HASH\' object")\'', 'description': 'General task-level error.'}], 'tables': []}
```

...and the working directory:

```bash
$ tree .
.
├── data
│   ├── data.csv
│   └── more_data.csv
├── datapackage.json
├── schema.json
└── scripts
    └── validate_package.py
```

`data/data.csv` and `data/more_data.csv`:
```csv
user,balance
fred,0
george,100
bill,10
```

`datapackage.json`:
```json
{
    "name": "test_package",
    "profile": "data-package",
    "resources": [
        {
            "name": "data",
            "path": "data/data.csv",
            "schema": "schema.json",
            "profile": "tabular-data-resource"
        },
        {
            "name": "more_data",
            "path": "data/more_data.csv",
            "schema": "schema.json",
            "profile": "tabular-data-resource"
        }
    ]
}
```

`schema.json`:
```json
{
    "fields": [
        {
            "name": "user",
            "type": "string"
        },
        {
            "name": "balance",
            "type": "integer"
        }
    ]
}
```

`scripts/validate_package.py`:
```python
import frictionless as fl


def main():
    report = fl.validate_package('datapackage.json', nopool=False)
    if report.errors:
        print(report)
    else:
        print("Is valid")


if __name__ == '__main__':
    main()
```

## Environment

```bash
$ pip freeze | grep frictionless
-e git+https://github.com/frictionlessdata/frictionless-py.git@5bd794179dcbaab080e1e0d0e692b6c875e44d43#egg=frictionless
$ python --version
Python 3.8.3
$ echo $SHELL
/bin/zsh
```

---

Please preserve this line to notify @roll (lead of this repository)
