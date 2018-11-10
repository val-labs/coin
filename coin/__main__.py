"""
coin: a coin engine

 a total coin engine

        Usage:
            coin create-chain [-f | --force] <name>
            coin remove-chain <name>
            coin create-cat <name> <wallet> [<remote-url>]
            coin remove-cat <name> <wallet> [<remote-url>]
            coin rename-cat <name> <wallet> <new-name> [<remote-url>]
            coin meow <name> <wallet> <message> [<remote-url>]
            coin purr <name> <wallet> <message> [<remote-url>]
            coin hiss <name> <wallet> <message> [<remote-url>]
            coin (-h | --help | --version)
        
        Options:
            -h, --help  Show this screen and exit.
"""
from . import __version__, main, docopt
if __name__=='__main__':
    main(docopt.docopt(__doc__, version=__version__))
