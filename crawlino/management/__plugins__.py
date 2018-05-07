import logging
import argparse

from crawlino_core import resolve_log_level

logging.basicConfig(format='[LOG] %(message)s')
log = logging.getLogger("crawlino")


def build_arg_parse():
    examples = '''
    Examples:

        * Scan target using default 50 most common plugins:
            plecost TARGET
        '''

    parser = argparse.ArgumentParser(
        description='Crawlino plugins manager',
        epilog=examples,
        formatter_class=argparse.RawTextHelpFormatter)

    # Main options
    parser.add_argument("-v", "--verbosity", dest="verbosity", action="count",
                        help="verbosity level: -v, -vv, -vvv.", default=3)

    subparsers = parser.add_subparsers(help='Options', dest="option")

    # -------------------------------------------------------------------------
    # Plugins management
    # -------------------------------------------------------------------------
    plugins_search_parser = subparsers.add_parser('search',
                                                  help='search plugin')
    plugins_search_parser.add_argument("PLUGIN_NAME", nargs="+", default=None)

    plugins_install_parser = subparsers.add_parser('install',
                                                   help='install plugin')
    plugins_install_parser.add_argument("PLUGIN_NAME", nargs="+", default=None)

    plugins_add_parser = subparsers.add_parser('add',
                                               help='add plugins repository')
    plugins_add_parser.add_argument("URL", default=None)

    plugins_update_parser = subparsers.add_parser(
        'update', help='update plugins / repositories')
    plugins_update_parser.add_argument("PLUGIN_NAME", nargs="?", default=None)

    return parser


def main():
    args = build_arg_parse()
    parsed_args = args.parse_args()

    # Setup log
    log.setLevel(resolve_log_level(parsed_args.verbosity))

    try:
        pass
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
