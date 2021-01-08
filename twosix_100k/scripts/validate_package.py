from pprint import pprint as pp
import frictionless as fl


def main():
    report = fl.validate_package('datapackage.json')
    # breakpoint()
    if report.errors:
        pp(report)
        # breakpoint()
    else:
        print("Is valid")


if __name__ == '__main__':
    main()
