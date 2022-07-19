"""Buzzoff command line tool."""

import argparse


def run(letters: str) -> list[str]:
    from buzzoff import buzz

    return buzz(letters)


def main() -> None:
    parser = argparse.ArgumentParser(prog="buzzoff")
    parser.add_argument("letters", help="the set of letters")
    args = parser.parse_args()

    print("\n".join(run(args.letters)))


if __name__ == "__main__":
    main()
