"""
Provide information on a variety of objects
"""

import os
import pickle
import re
from argparse import ArgumentParser, Namespace, _SubParsersAction

import jinja2
from feditest.reporting import fatal
from feditest.testplan import TestPlanTestSpec
from feditest.testrun import HtmlTestResultWriter, TestProblem, TestSummary


def _get_problem(
    run_session, test: TestPlanTestSpec
) -> TestProblem | None:  # noqa: F821
    return next((p for p in run_session.problems if p.test.name == test.name), None)


def run(parser: ArgumentParser, args: Namespace, remaining: list[str]) -> int:
    """
    Generate a test report.
    """
    template = HtmlTestResultWriter.get_template(args.template)
    
    with open(args.results, "rb") as fp:
        results = pickle.load(fp)
        all_tests = sorted(
            {
                test.name: test for s in results["plan"].sessions for test in s.tests
            }.values(),
            key=lambda t: t.name,
        )
        sessions = list(zip(results["run_sessions"], results["plan"].sessions))
        summary = TestSummary.for_run(results["plan"], results["run_sessions"])
        print(
            template.render(
                plan=results["plan"],
                sessions=sessions,
                summary=summary,
                metadata=results["metadata"],
                all_tests=all_tests,
                get_problem=_get_problem,
                remove_white=lambda s: re.sub("[ \t\n\a]", "_", s),
                format_problem=lambda p: (
                    lambda s: s if len(s) < 128 else s[:129] + "..."
                )(str(p.exc).strip()),
            )
        )


    return 0


def add_sub_parser(parent_parser: _SubParsersAction, cmd_name: str) -> None:
    parser = parent_parser.add_parser(cmd_name, help="Generate report")
    parser.add_argument("results", nargs="?", default="results.pkl", help="Pickled test results")
    parser.add_argument(
        "--template", default="report", help="Template for generating report"
    )
