from pathlib import Path

from nvim.wrapper import DockerWrapper


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("file", nargs="*", help="files to open")
    parser.add_argument(
        *("-w", "--work"),
        help="directory to mount to the container",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        *("-t", "--timeout"),
        type=float,
    )
    parser.add_argument(
        *("-b", "--build"),
        help="force build step, useful if Docker file is changed",
        action="store_true",
    )
    args = parser.parse_args()

    application = DockerWrapper("nvim", args.work)
    if not application.exists() or args.build:
        application.build()

    application.run(*args.file, timeout=args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
