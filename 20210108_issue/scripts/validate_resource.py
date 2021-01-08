from pprint import pprint as pp
import frictionless as fl


def main():
    report = fl.validate('dataresource.json')
    if report.valid:
        print("Is valid")
    else:
        pp(report)


if __name__ == '__main__':
    main()
