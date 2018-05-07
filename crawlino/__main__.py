import logging
import argparse

from crawlino_core import resolve_log_level
from crawlino.models.input_model import RunningConfig
from crawlino import SimpleCrawlinoManager

logging.basicConfig(format='[LOG] %(message)s')
log = logging.getLogger("crawlino")


def build_arg_parse():
    examples = '''
    Examples:

        * Scan target using default 50 most common plugins:
            plecost TARGET
        '''

    parser = argparse.ArgumentParser(
        description='Crawlino: the new level of the crawling systems',
        epilog=examples,
        formatter_class=argparse.RawTextHelpFormatter)

    # Main options
    parser.add_argument("CRAWLERS_PATH", nargs="+", default=".")
    parser.add_argument("-v", "--verbosity", dest="verbosity", action="count",
                        help="verbosity level: -v, -vv, -vvv.", default=3)

    parser.add_argument("-c", "--concurrency",
                        dest="concurrency",
                        type=int,
                        help="set concurrency value", default=1)
    parser.add_argument("-e", "--environ-var",
                        dest="environment_vars",
                        action="append",
                        help="set environment vars")
    parser.add_argument("-E", "--environs-file",
                        dest="environment_file",
                        help="environment vars from file")
    parser.add_argument("-w", "--concurrency-type",
                        dest="concurrency_type",
                        type=str,
                        choices=RunningConfig.CONCURRENCY_MODES,
                        help="set concurrency mode", default="sequential")

    return parser


def main():
    args = build_arg_parse()
    parsed_args = args.parse_args()

    # Setup log
    log.setLevel(resolve_log_level(parsed_args.verbosity))

    log.debug("Starting crawlino in CLI")
    o = SimpleCrawlinoManager.from_argparser(parsed_args)
    o.load()

    try:
        o.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
