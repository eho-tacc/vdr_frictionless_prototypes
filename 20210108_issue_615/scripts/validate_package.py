import frictionless as fl


def main():
    report = fl.validate_package('datapackage.json', nopool=True)
    if report.valid:
        print("Is valid")
    else:
        print(report)


if __name__ == '__main__':
    main()
