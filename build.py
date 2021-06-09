#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from pathlib import Path
from shutil import which


def setup_environment(ns):
    os.environ["CONFIG"] = ns.config
    os.environ["UPLOAD_PACKAGES"] = "False"


def run_build(ns, extra_args):
    dot_abs_folder = (Path(__file__).parent.absolute() / ".abs").as_posix()
    cmd = [
        "conda",
        "build",
        "./recipe",
        "-m",
        f"{dot_abs_folder}/{ns.config}.yaml",
        "--suppress-variables",
        "--clobber-file",
        f"{dot_abs_folder}/clobber_noarch.yaml",
    ] + extra_args
    if ns.output_folder:
        cmd += ["--output-folder", ns.output_folder]
    print(f"Calling: {cmd}")
    subprocess.check_call(cmd)


def verify_config(ns):
    dot_abs_folder = Path(__file__).parent.absolute() / ".abs"
    valid_configs = {os.path.basename(f)[:-5] for f in dot_abs_folder.glob("*.yaml")}
    print(f"valid configs are {valid_configs}")
    if ns.config in valid_configs:
        print("Using " + ns.config + " configuration")
        return


def main(args=None):
    p = argparse.ArgumentParser("build")
    p.add_argument("config", default="conda_build_config", nargs="?")
    p.add_argument("--output-folder", action="store")

    ns, extra_args = p.parse_known_args(args=args)

    verify_config(ns)

    # check that conda is available
    if which("conda") is None:
        sys.exit("conda is not available")

    # ensure conda-build is available
    if which("conda-build") is None:
        subprocess.check_call(["conda", "install", "conda-build", "-y"])

    # build
    run_build(ns, extra_args)


if __name__ == "__main__":
    main()
