import os
import re
import traceback
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import Callable, Iterator
from urllib.parse import urlencode

import jinja2
from feditest.reporting import warning
from feditest.testruntranscript import (
    TestMetaTranscript,
    TestRunResultTranscript,
    TestRunSessionTranscript,
    TestRunTranscript,
)
from feditest.utils import FEDITEST_VERSION


def _regex_sub(s, pattern, replacement):
    return re.sub(pattern, replacement, s)


def _get_templates(template_path: str) -> jinja2.Environment:
    templates_base_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "templates"
    )
    os.chdir(templates_base_dir)
    template_path = template_path.split(",")
    templates = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    templates.filters["regex_sub"] = _regex_sub
    return templates


def write_hugo_bundle(
    transcript: TestRunTranscript,
    output_dir: str | os.PathLike,
    template_path: str | os.PathLike | list[str | os.PathLike] = "multifile",
):
    write_multifile_report(
        transcript, output_dir, template_path, "md", lambda name: f"../sessions/{name}/"
    )

    templates = _get_templates(template_path)

    os.makedirs(os.path.join(output_dir, "css"), exist_ok=True)
    with open(os.path.join(output_dir, "css", "style.css"), "w") as fp:
        css_template = templates.get_template("style.css")
        fp.write(css_template.render())


def write_multifile_report(
    transcript: TestRunTranscript,
    output_dir: str | os.PathLike,
    template_path: str | os.PathLike | list[str | os.PathLike] = "multifile",
    file_ext: str = "html",
    session_linker: Callable[[str], str] = lambda name: f"sessions/{name}.html",
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sessions_dir = os.path.join(output_dir, "sessions")
    if not os.path.exists(sessions_dir):
        os.makedirs(sessions_dir)

    templates = _get_templates(template_path)
    context = dict(
        run=transcript,
        summary=transcript.build_summary(),
        getattr=getattr,
        sorted=sorted,
        enumerate=enumerate,
        get_results_for=_get_results_for,
        remove_white=lambda s: re.sub("[ \t\n\a]", "_", str(s)),
        session_linker=session_linker,
        format_timestamp=lambda ts, format="%Y-%m-%dT%H-%M-%S.%fZ": (
            ts.strftime(format) if ts else ""
        ),
    )

    matrix_filename = os.path.join(output_dir, f"matrix.{file_ext}")
    with open(matrix_filename, "w") as fp:
        matrix_template = templates.get_template("matrix.jinja2")
        fp.write(matrix_template.render(**context))

    session_template = templates.get_template("session.jinja2")
    for run_session in transcript.sessions:
        session_context = dict(context)
        session_context.update(run_session=run_session)
        session_filename = (
            f"{run_session.constellation.nodes['server'].appdata['app']}.{file_ext}"
        )
        with open(os.path.join(sessions_dir, session_filename), "w") as fp:
            fp.write(session_template.render(**session_context))

    # tests_template = templates.get_template("tests.jinja2")
    # tests_filename = os.path.join(output_dir, "tests.html")
    # with open(os.path.join(output_dir, tests_filename), "w") as fp:
    #     fp.write(tests_template.render(**context))


def _get_results_for(
    run_transcript: TestRunTranscript,
    session_transcript: TestRunSessionTranscript,
    test_meta: TestMetaTranscript,
) -> Iterator[TestRunResultTranscript | None]:
    """
    Determine the set of test results running test_meta within session_transcript, and return it as an Iterator.
    This is a set, not a single value, because we might run the same test multiple times (perhaps with differing role
    assignments) in the same session. The run_transcript is passed in because session_transcript does not have a pointer "up".
    """
    plan_session = run_transcript.plan.sessions[session_transcript.plan_session_index]
    for test_transcript in session_transcript.run_tests:
        plan_testspec = plan_session.tests[test_transcript.plan_test_index]
        if plan_testspec.name == test_meta.name:
            yield test_transcript.worst_result
    return None


def run(parser: ArgumentParser, args: Namespace, remaining: list[str]) -> int:
    """
    Run this command.
    """

    try:
        transcript = TestRunTranscript.load(args.transcript_name)
        if not transcript.has_compatible_version():
            warning(
                f"Transcript was created by FediTest { transcript.feditest_version }, "
                f"you are running FediTest { FEDITEST_VERSION }: incompatibilities may occur."
            )

        if args.format == "html":
            write_multifile_report(transcript, args.output_dir, args.template_path)
        elif args.format == "hugo":
            write_hugo_bundle(transcript, args.output_dir, args.template_path)
        else:
            raise ValueError(args.format)
    except Exception:
        traceback.print_exc()


def add_sub_parser(parent_parser: _SubParsersAction, cmd_name: str) -> None:
    """
    Add command-line options for this sub-command
    parent_parser: the parent argparse parser
    cmd_name: name of this command
    """
    parser = parent_parser.add_parser(cmd_name, help="Run one or more tests")
    parser.add_argument(
        "--transcript",
        required=True,
        dest="transcript_name",
        help="JSON file containing the transcript",
    )
    parser.add_argument("--out", dest="output_dir")
    parser.add_argument("--templates", dest="template_path", default="multifile")
    parser.add_argument("-f", "--format", choices=["html", "hugo"], default="html")
