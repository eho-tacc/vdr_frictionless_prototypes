# VDR -> Frictionless Report Out

## Usage

Please see the [README](../README.md) for details on usage.

## How to Write Schemas and Table Relationships in Frictionless

> With regard to the workflow, what I don't quite understand well is how to build and work with schemas, beyond the ones that can be automatically inferred. There is supposedly a way to add a table schema that describes the relations between tabular resources, which would be critical for representing a data set like the versioned datasets sub-directories
> Using fricitionless, figure out how to represent a one of the subset datasets from versioned datasets as best as possible. Once you figure out how to do that we can sync it up with the builder workflow in the Datasets CLI prototype.
> On the frictionless side, I think it's a matter of describing the indivudual tables, then adding something like "tables.yml" or "tables.json" in one of the table schema dialects (edited)
> So, one might do a datasets builder init then go build up the table schemas (by hand or using frictionless-py) then datasets builder update to load those changes into the dataset's resources (edited)

### Schemas

For a given [Data Resources](https://specs.frictionlessdata.io/data-resource/), the `schema` field can be either a JSON object, or relative POSIX path to a `*.json` file that contains a JSON object. A minimal schema has a `fields` field:
```json
{
    "fields": [
        {
            "name": "dataset",
            "type": "string"
        },
        {
            "name": "name",
            "type": "string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "comments",
            "type": "string"
        }
    ]
}
```
The Resource that this schema describes must have exactly the two fields defined above. To my knowledge, there is no way to specify `additionalProperties` or similar in a Frictionless schema. There is a `schema/fields/constraints/required` field, but even set to `false`, it will allow null values in a field, but not missing fields. e.g. the following tabular CSV Resource would pass:
```csv
dataset,name,comments
some_dataset,,some_comments
```
...but this one fails:
```csv
dataset,comments
some_dataset,some_comments
```
We'll see that this poses problems for migrating SD2E Versioned Datasets, in particular, to Frictionless.

### DB Relationships

Relationships between fields in different tables are drawn using two fields in a [Table Schema](https://specs.frictionlessdata.io/table-schema/): [`primaryKey`](https://specs.frictionlessdata.io/table-schema/#primary-key) and [`foreignKey`](https://specs.frictionlessdata.io/table-schema/#foreign-keys).

[`primaryKey`](https://specs.frictionlessdata.io/table-schema/#primary-key) is an optional field in the schema that defines one or more fields in a table. These field(s) **uniquely** identify each row in a [Data Resource](https://specs.frictionlessdata.io/data-resource/). The presence of rows with non-unique `primaryKey`s will raise an error during validation.

[`foreignKey`](https://specs.frictionlessdata.io/table-schema/#foreign-keys) is an optional field in the schema that defines relationships to another [Table Schema](https://specs.frictionlessdata.io/table-schema/) that describes a [Data Resources](https://specs.frictionlessdata.io/data-resource/) (or tables). For every row of the table described by this schema (the schema that has a `foreignKey` defined), Frictionless "looks up" the `primaryKey` of that row in the other table (defined at each `foreignKey/reference/resource`).

Notably, `foreignKey` **links** two schemas, but neither schema **inherits** from the other. e.g. the following resource:
```json
{
    "name": "some_data",
    "path": "some_data.csv",
    "profile": "tabular-data-resource",
    "schema": {
        "fields": [{
            "name": "dataset",
            "constraints": {"minLength": 4}
        }],
        "foreignKeys": [{
            "fields": "dataset",
            "reference": {
                "resource": "other_data",
                "fields": "dataset"
            }
        }]
    }
}
```
enforces `schema/fields/constraints` only to the `dataset` field in Resource `some_data` , but not to `dataset` in `other_data` Resource. Likewise, any `schema/fields/constraints` defined for field `dataset` in Resource `other_data` will not be enforced on the `some_data` Resource.

## Bugs & Pain Points Using Tapis Datasets CLI

* `datasets builder init`
    * Generates empty placeholder values for `contributors`, `keywords`, and `licences` fields in `datapackage.json`.
        * `frictionless validate --nopool datapackage.json` complains that these fields are too short
        * Validation passes if these placeholders are removed
    * Most of the time, I just want to infer files in the top level of `./data`
        * It would be nice if there were a `--max-depth` or `--recurse` option here
        * Maybe add exclude options? e.g. `--exclude datapackage.json --exclude dataresource.json --exclude schemas/` by default
        * `datasets builder init data` generates `data/datapackage.json`
            * This wouldn't be an issue, except that the `resources/path` are pointing to the wrong place
    * Populates `resources/scheme`, which breaks `resources/path` if `path` is an array.
        * I assume this is a placeholder for `resources/schema`

## Challenges

### Frictionless

As far as I am aware, the fields in a Frictionless [Table Schema](https://specs.frictionlessdata.io/table-schema/) must **exactly** match the fields in the tabular data it describes. Adding or removing a single field in the tabular data, even if `schema/fields/constraints/required` is `false` for that field, fails schema validation.

### SD2E Versioned Datasets (VDS)

The Versioned Datasets Repository has minimal enforcement of which fields are in the tabular data. It strictly enforces row identifiers (`primaryKey` in Fricitonless lingo), but only requires `dataset` and `name` fields in each table.

### VDS -> Frictionless Migration

The consequence of the above two design choices is that very similar tabular data sources (CSV files in the case of VDS), differing only by 1 or 2 columns (fields), fails validation against any single schema (exception is an empty schema). Without modifying tabular data, this prevents us from defining a single Data Resource with multiple `path`s, which would be ideal for migrating VDS.

An example of this is the addition of another VDS dataset `data/winter19_stab_scores_1.csv` as a `path` in the `stab_scores` Data Resource. The `stab_scores` schema (`schemas/stab_scores.csv`) contains 3 extra columns compared to the tabular data in `data/winter19_stab_scores_1.csv`, because the schema was inferred from `data/TwoSix_100K_stab_scores_1.csv`.

## Next Steps

In the VDS -> Frictionless migration workflow, we need to add a normalization step, so that we can conveniently annotate/enforce all stability score (`stab_score`) data, for instance, under a single schema. I will explore a couple strategies for normalizing, but will start by splitting the monolithic `stab_score` Resource (114 fields!) into multiple atomic Resources. The hope is that such a normalization strategy would be generic enough to harden as a sub-command in `tapis datasets`.
