#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered front page to the output directory.

Stdlib only. No network, no clock, no randomness: both runs write the
same bytes, because the image is a fixed file shipped in this repository.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
