"""Buzzoff command line tool."""

import click


@click.group()
def cli() -> None:
    """CLI group"""


@cli.command()
@click.option("-l", "--length", type=int, default=4, help="minimum word length")
@click.option("-m", "--mandatory", help="mandatory letter(s)")
@click.argument("letters")
def off(letters, length: int, mandatory) -> None:
    """Buzz off"""
    # import inside function to speed up CLI parsing
    from buzz.off import buzz  # pylint: disable=import-outside-toplevel)

    print("\n".join(buzz(letters, minlength=length, mandatory=mandatory)))


@cli.command()
@click.argument("letters")
def letterboxed(letters: str) -> None:
    """Solve LetterBoxed"""
    from buzz.letterboxed import solve  # pylint: disable=import-outside-toplevel)

    print("\n".join(" ".join(row) for row in solve(letters)))


if __name__ == "__main__":
    cli()
