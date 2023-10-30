import logging
import os
import re
import shutil
from argparse import ArgumentParser

logging.basicConfig()
logger = logging.getLogger(__name__)


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    move_files(args.src, args.dest, args.interactive, args.insensitive)


def move_files(
    src: str,
    dest: str,
    interactive: bool = False,
    case_insensitive: bool = False,
):
    """
    regex move `src` to `dest`

    Args:
        src (str): the source regex
        dest (str): the destination regex
        interactive (bool): ask for user confirmation if True (default is False)
        case_insensitive (bool): match files ignoring case (default is False)

    Returns:
        None
    """
    src_dir = os.path.dirname(src) or "."
    dest_dir = os.path.dirname(dest) or "."

    src_basename = os.path.basename(src)
    src_file_re = (
        re.compile(src_basename)
        if not case_insensitive
        else re.compile(src_basename, re.IGNORECASE)
    )
    dest_file_re = os.path.basename(dest)

    logger.debug(f"{src_dir=}, {dest_dir=}\n{src_file_re=}, {dest_file_re=}")
    if not os.path.exists(dest_dir):
        logger.debug(f"created directory: {dest_dir}")
        os.mkdir(dest_dir)

    for file in os.listdir(src_dir):
        if not src_file_re.match(file):
            logger.debug(f"{file} doesn't match the src_re")
            continue

        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, src_file_re.sub(dest_file_re, file))

        should_move = True
        if interactive:
            print(f"{src_file} --> {dest_file}")
            if input("y/n: ")[0].lower() != "y":
                should_move = False

        if should_move:
            logger.debug(f"{src_file} --> {dest_file}")
            shutil.move(src_file, dest_file)


def get_parser() -> ArgumentParser:
    """
    get the parser for command line arguments

    Returns:
        ArgumentParser: argument parser with required arguments added
    """
    parser = ArgumentParser(prog="rmv", description="regular expression mv")
    parser.add_argument("src", metavar="SRC", help="source regex", type=str)
    parser.add_argument("dest", metavar="DEST", help="destination regex", type=str)
    parser.add_argument(
        "--interactive", "-a", action="store_true", help="run interactively"
    )
    parser.add_argument("--insensitive", "-i", action="store_true", help="ignore case")
    parser.add_argument("--verbose", "-v", action="store_true", help="print each move")

    return parser


if __name__ == "__main__":
    main()
