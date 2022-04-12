# pylint: disable=missing-module-docstring,missing-function-docstring,eval-used
import sys


def main():
    """Implement the calculator"""
    return eval(''.join(sys.argv[1:]))


if __name__ == "__main__":
    print(main())
