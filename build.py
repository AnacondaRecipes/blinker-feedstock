#!/usr/bin/env python3

import glob
import os
import subprocess
import sys
from argparse import ArgumentParser
from shutil import which


def setup_environment(ns):
    os.environ["CONFIG"] = ns.config
    os.environ["UPLOAD_PACKAGES"] = "False"


def run_build(ns):
    cmd = [
        "conda",
        "build",
        "./recipe",
        "-m",
        f"./.abs/{ns.config}.yaml",
        "--suppress-variables",
        "--clobber-file",
        "./.abs/clobber_noarch.yaml",
    ]
    if ns.output_folder:
        cmd += [
            "--output-folder",
            ns.output_folder
        ]
    print(f"Calling: {cmd}")
    subprocess.check_call(cmd)


def verify_config(ns):
    valid_configs = {os.path.basename(f)[:-5] for f in glob.glob(".abs/*.yaml")}
    print(f"valid configs are {valid_configs}")
    if ns.config in valid_configs:
        print("Using " + ns.config + " configuration")
        return


def main(args=None):
    p = ArgumentParser("build")
    p.add_argument("config", default="conda_build_config", nargs="?")
    p.add_argument("--output-folder", action="store")

    ns = p.parse_args(args=args)

    verify_config(ns)

    # check that conda is available
    if which("conda") is None:
        sys.exit("conda is not available")

    # ensure conda-build is available
    if which("conda-build") is None:
        subprocess.check_call(["conda", "install", "conda-build", "-y"])

    # build
    run_build(ns)


if __name__ == "__main__":
    main()
