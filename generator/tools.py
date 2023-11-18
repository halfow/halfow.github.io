"""
Small tools to do help during development
"""
from argparse import ArgumentParser
from ast import literal_eval
from pathlib import Path

from PIL import Image, ImageOps


def two_usigned(d: str) -> tuple[int, int]:
    a = literal_eval(d)
    return int(a), int(a)


def img2fav() -> None:
    parser = ArgumentParser(description="Image 2 Favicon")
    parser.add_argument(
        "path",
        type=Path,
        help="path to image",
    )
    parser.add_argument(
        *("-s", "--size"),
        nargs="+",
        type=two_usigned,
        help="sizes to create (Default: %(default)s)",
        default=((16, 16), (32, 32), (96, 96)),
    )
    parser.add_argument(
        *("-o", "--output"),
        type=Path,
        help="output file path (Default: %(default)s)",
    )
    args = parser.parse_args()

    with Image.open(args.path) as image:
        image.save(
            args.output or args.path.with_name("favicon.ico"),
            format="ICO",
            sizes=args.size,
        )


def add_alpha(rbg, alpha, threshold):
    """
    useful thresholds are 0 and 255
    """
    for (r, b, g, *_), a in zip(rbg, alpha, strict=True):
        yield r, g, b, abs(threshold - a)


def make_transparent():
    """
    RGB to RGBA

    Add alpha channel from the grayscale image
    """
    parser = ArgumentParser(description="Image 2 Transparent")
    parser.add_argument(
        "path",
        help="path to image",
        type=Path,
    )
    parser.add_argument(
        *("-o", "--output"),
        help="output file path (Default: %(default)s)",
        type=Path,
        default=Path(__file__).parent.parent / "site" / "img" / "output.png",
    )
    parser.add_argument(
        *("-t", "--threshold"),
        help="set threshold transparency point (Default: %(default)s)",
        type=int,
        default=255,
    )
    args = parser.parse_args()

    with Image.open(args.path) as image:
        data = image.getdata()
        rbga = Image.new(mode="RGBA", size=image.size)
        if isinstance(data[0], int):
            rbga.paste(image)
            data = rbga.getdata()

        rbga.putdata(
            list(
                add_alpha(
                    rbg=data,
                    alpha=image.convert("L").getdata(),
                    threshold=args.threshold,
                )
            )  # type: ignore
        )
        rbga.save(args.output or args.path.with_stem("transparent"), "PNG")


def invert_colors() -> None:
    parser = ArgumentParser(description="Image 2 Favicon")
    parser.add_argument(
        "path",
        type=Path,
        help="path to image",
    )
    parser.add_argument(
        *("-o", "--output"),
        type=Path,
        help="output file path",
    )
    args = parser.parse_args()

    with Image.open(args.path) as image:
        inverted = ImageOps.invert(image)
        inverted.save(args.output or args.path.with_stem("inverted"))


def text2IO() -> None:
    parser = ArgumentParser()
    parser.add_argument("string", nargs="+")
    args = parser.parse_args()
    string = " ".join(args.string)
    trans = str.maketrans("10", "IO")
    result = "".join(map("{:08b}".format, map(ord, string))).translate(trans)  # type: ignore
    print(result)
