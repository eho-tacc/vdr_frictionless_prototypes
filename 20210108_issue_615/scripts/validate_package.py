import frictionless as fl


def main():
    report = fl.validate_package('datapackage.json', nopool=False)
    if report.errors:
        print(report)
    else:
        print("Is valid")


if __name__ == '__main__':
    main()
