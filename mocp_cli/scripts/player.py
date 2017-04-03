import click
import moc
from mocp_cli import Player


@click.command()
@click.argument('glob_patterns', nargs=-1)
def main(glob_patterns):
    """Start a REPL to control music on console player (mocp)"""
    if glob_patterns:
        moc.find_and_play(*glob_patterns)
    Player()


if __name__ == '__main__':
    main()
