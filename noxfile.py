from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()

nox.options.sessions = ["lint", "pylint", "tests"]


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run(
        "pre-commit", "run", "--all-files", "--show-diff-on-failure", *session.posargs
    )


@nox.session
def pylint(session: nox.Session) -> None:
    """
    Run PyLint.
    """
    # This needs to be installed into the package environment, and is slower
    # than a pre-commit check
    session.install(".", "pylint")
    session.run("pylint", "ss_pybind11", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "-- --help" to show helps.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Serve after building")
    parser.add_argument(
        "--check", action="store_true", help="Checks the docs with warnings as errors."
    )
    parser.add_argument("--linkcheck", action="store_true", help="Checks the links.")
    args, posargs = parser.parse_known_args(session.posargs)

    extra_installs = ["sphinx-autobuild"] if args.serve else []
    session.install("-e.[docs]", *extra_installs)

    shared_args = [
        "-T",  # full tracebacks
        "-c",
        "docs",
        "docs",
        "docs/_build/html",
        *posargs,
    ]

    if args.check:
        shared_args.append("-n")  # nitpicky mode

    if args.serve:
        session.run("sphinx-autobuild", *shared_args)
    elif args.linkcheck:
        session.run("sphinx-build", "-b", "linkcheck", *shared_args)
    else:
        session.run("sphinx-build", "--keep-going", *shared_args)


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel.
    """

    build_path = DIR.joinpath("build")
    if build_path.exists():
        shutil.rmtree(build_path)

    session.install("build")
    session.run("python", "-m", "build")


@nox.session(reuse_venv=True)
def pyi(session: nox.Session) -> None:
    """
    Generate the Pyi type stubs.
    """
    session.install("pybind11-stubgen")
    session.install(".[test]")
    session.run("pybind11-stubgen", "ss_pybind11._core", "-o", "src")


@nox.session(reuse_venv=True)
def template(session: nox.Session) -> None:
    """
    Build template from current repo. Pass "-- --help" to show helps.
    """
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--vcs-ref", default="HEAD", help="Git reference to generate."
    )
    parser.add_argument(
        "--data-file",
        default="includes/copier-answers-sample.yml",
        help="Load data from a YAML file.",
    )
    parser.add_argument("--dest", default=".", help="Destination to generate.")
    args, posargs = parser.parse_known_args(session.posargs)

    excludes = [".", ".git", "template", "includes", ".nox", "copier.yml"]
    for dir_item in os.listdir("."):
        if dir_item in excludes:
            continue
        if Path(dir_item).is_dir():
            shutil.rmtree(dir_item)
        else:
            Path(dir_item).unlink()

    session.run(
        "pipx",
        "run",
        "copier",
        "copy",
        "-r",
        args.vcs_ref,
        "--data-file",
        args.data_file,
        ".",
        args.dest,
        *posargs,
    )

    Path(".copier-answers.yml").unlink()
