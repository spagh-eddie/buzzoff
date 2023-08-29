"""Buzzoff command line tool."""

import click


@click.group()
def cli() -> None:
    """CLI group"""


@cli.command()
@click.option("-l", "--length", type=int, default=4, help="minimum word length")
@click.option("-m", "--mandatory", help="mandatory letter(s)")
@click.argument("letters")
def buzzoff(letters, length: int, mandatory) -> None:
    """Buzz off"""
    # import inside function to speed up CLI parsing
    from buzzoff import buzz  # pylint: disable=import-outside-toplevel)

    print("\n".join(buzz(letters, minlength=length, mandatory=mandatory)))


if __name__ == "__main__":
    cli()
