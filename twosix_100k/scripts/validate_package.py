from pprint import pprint as pp
import frictionless as fl


def main():
    report = fl.validate_package('datapackage.json', nopool=True)
    if report.valid:
        print("Is valid")
    else:
        pp(report)
        # breakpoint()


if __name__ == '__main__':
    main()
