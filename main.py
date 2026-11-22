"""Deliver the strawberry picture for the make.fun bounty.

The picture itself ships beside this file as entry.png. All this program
does is carry that file, byte for byte, into the output directory the
grader points at, so the image the judge sees is exactly the one in the
repository. Only the Python standard library is used.
"""

import os
import shutil
import sys

PICTURE_NAME = "entry.png"
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Print a problem to stderr and stop with a non-zero exit."""
    print("error: " + message, file=sys.stderr)
    return 1


def picture_path():
    """Locate entry.png next to this script, wherever it is run from."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, PICTURE_NAME)


def output_path():
    """Work out where the finished picture belongs."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, PICTURE_NAME)


def check_copy(source, destination):
    """Confirm the delivered file is a faithful copy of the source.

    Returns an error string when something is wrong, or None when the
    copy is good: the file must exist, match the source byte for byte in
    size, start with the PNG signature, and stay under the 1 MiB cap.
    """
    if not os.path.isfile(destination):
        return "output picture missing after copy: " + destination

    source_size = os.path.getsize(source)
    copied_size = os.path.getsize(destination)
    if copied_size != source_size:
        return (
            "output size %d does not match source size %d"
            % (copied_size, source_size)
        )
    if copied_size > MAX_BYTES:
        return "output picture is %d bytes, over the %d byte limit" % (
            copied_size,
            MAX_BYTES,
        )

    with open(destination, "rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        return "output picture does not start with the PNG signature"

    return None


def main():
    source = picture_path()
    if not os.path.isfile(source):
        return fail("source picture not found: " + source)

    destination = output_path()
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copyfile(source, destination)

    problem = check_copy(source, destination)
    if problem is not None:
        return fail(problem)

    print("wrote %s (%d bytes)" % (destination, os.path.getsize(destination)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
