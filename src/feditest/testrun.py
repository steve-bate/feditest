"""
Classes that represent a running TestPlan and its its parts.
"""

from datetime import datetime, timezone
from typing import Any, List, Type

from feditest import Test, all_node_drivers, all_tests
from feditest.protocols import Node, NodeDriver
from feditest.reporting import error, fatal, info
from feditest.testplan import (
    TestPlan,
    TestPlanConstellation,
    TestPlanSession,
    TestPlanTestSpec,
)


class TestRunConstellation:
    def __init__(self, plan_constellation: TestPlanConstellation ):
        self._plan_constellation = plan_constellation
        self._run_constellation : dict[str, Node] = {}

    def setup(self):
        """
        Set up the constellation of nodes needed for some tests.
        """

        info('Setting up constellation:', self._plan_constellation.name)

        for plan_role in self._plan_constellation.roles:
            plan_role_name = plan_role.name
            node_driver_class : Type[Any] = all_node_drivers[plan_role.nodedriver]

            info('Setting up role', plan_role_name, f'(node driver: {plan_role.nodedriver})')

            node_driver : NodeDriver = node_driver_class(plan_role_name)
            node : Node = node_driver.provision_node(plan_role_name, plan_role.hostname, plan_role.parameters)
            if node:
                self._run_constellation[plan_role_name] = node
            else:
                raise Exception(f'NodeDriver {node_driver} return null Node from provision_node()')

        # time.sleep(10) # This is a fudge factor because apparently some applications take some time
                       # after deployment before they are ready to communicate.
                       # FIXME? This should potentially be in the NodeDrivers

    def teardown(self):
        info('Tearing down constellation:', self._plan_constellation.name)

        for plan_role in reversed(self._plan_constellation.roles):
            plan_role_name = plan_role.name

            if plan_role_name in self._run_constellation: # setup may never have succeeded
                info('Tearing down role', plan_role_name)
                node = self._run_constellation[plan_role_name]
                driver = node.node_driver()
                driver.unprovision_node(node)
                del self._run_constellation[plan_role_name]


class TestRunSession:
    def __init__(self, name: str, plan_session: TestPlanSession):
        self._name = name
        self._plan_session = plan_session
        self._constellation = None
        self._problems : List[Exception] = []

    @property
    def name(self):
        return self._name
    
    @property
    def problems(self):
        return self._problems
    
    def run(self):
        if len(self._plan_session.tests ):
            info('Running session:', self._name)

            try:
                self._constellation = TestRunConstellation(self._plan_session.constellation)
                self._constellation.setup()

                for test_spec in self._plan_session.tests:
                    if test_spec.disabled:
                        info('Skipping TestSpec', test_spec.disabled, "reason:", test_spec.disabled)
                    else:
                        try:
                            self._run_test_spec(test_spec)
                        except Exception as e:
                             error('FAILED test:', e)
                             self._problems.append((test_spec, e))
            finally:
                self._constellation.teardown()

            if self._constellation._run_constellation:
                fatal( 'Still have nodes in the constellation', self._constellation._run_constellation )

            info('End running session:', self._name)

        else:
            info('Skipping session:', self._name, ': no tests defined')


    def _run_test_spec(self, test_spec: TestPlanTestSpec):

        info('Running test', test_spec.name)
        test : Test = all_tests.get(test_spec.name)

        for test_step in test.steps:
            info('Running step', test_step.name )

            plan_roles = self._constellation._plan_constellation.roles
            run_constellation = self._constellation._run_constellation

            # FIXME: we should map the plan_roles to the names of the @test function parameters
            match len(plan_roles):
                case 1:
                    test_step.function(run_constellation[plan_roles[0].name])
                case 2:
                    test_step.function(run_constellation[plan_roles[0].name], run_constellation[plan_roles[1].name])
                case 3:
                    test_step.function(run_constellation[plan_roles[0].name], run_constellation[plan_roles[1].name], run_constellation[plan_roles[2].name])
                case 4:
                    test_step.function(run_constellation[plan_roles[0].name], run_constellation[plan_roles[1].name], run_constellation[plan_roles[2].name], run_constellation[plan_roles[3].name])
                case _:
                    error( 'Constellation size not supported yet:', len(plan_roles))


class TestRun:
    """
    Encapsulates the state of a test run while feditest is executing a TestPlan
    """
    def __init__(self, plan: TestPlan):
        self._plan = plan
        self._runid : str = 'feditest-run-' + datetime.now(timezone.utc).strftime( "%Y-%m-%dT%H:%M:%S.%f")

    # def _report_test_results(self, plan: TestPlan, run_sessions: list[TestRunSession]):
    #     print("TAP version 14")
    #     print(f"# plan: {self._plan.name}")
    #     # date, etc.
    #     for i in range(0, len(run_sessions)):
    #         run_session = run_sessions[i]
    #         plan_session = self._plan.sessions[i]
    #         print(f"# session: {run_session.name}")
    #         print(f"    1..{len(plan_session.tests)}")
    #         for n, test in enumerate(plan_session.tests):
    #             problem = None
    #             for problem_record in run_session.problems:
    #                 if problem_record[0].name == test.name:
    #                     problem = problem_record[1]
    #             if problem:
    #                 print(f"    not ok {n + 1} - {test.name}")
    #                 for line in str(problem).split("\n"):
    #                     print(f"    # {line}")
    #             else:
    #                 directives = f" # SKIP {test.disabled}" if test.disabled else ""
    #                 print(f"    ok {n + 1} - {test.name}{directives}")
    #         if run_session._problems:
    #             print(f"not ok {i + 1} - {len(run_session.problems)} session error(s)")
    #         else:
    #             print(f"ok {i + 1}")

    #     print(f"1..{len(self._plan.sessions)}")


    def _report_test_results(self, plan: TestPlan, run_sessions: list[TestRunSession]):
        print("TAP version 14")
        print(f"# test plan: {self._plan.name}")
        # date, etc.
        test_count = sum(len(s.tests) for s in self._plan.sessions)
        print(f"1..{test_count}")
        test_id = 1
        for i in range(0, len(run_sessions)):
            run_session = run_sessions[i]
            plan_session = self._plan.sessions[i]
            print(f"# session: {run_session.name}")
            for test in plan_session.tests:
                problem = None
                for problem_record in run_session.problems:
                    if problem_record[0].name == test.name:
                        problem = problem_record[1]
                if problem:
                    print(f"not ok {test_id} - {test.name}")
                    print("  ---")
                    print("  exception: |")
                    for line in str(problem).strip().split("\n"):
                        print(f"    {line}")
                    print("  ...")
                else:
                    directives = f" # SKIP {test.disabled}" if test.disabled else ""
                    print(f"ok {test_id} - {test.name}{directives}")
                test_id += 1

    def run(self):
        info( f'RUNNING test plan: {self._plan.name} (id: {self._runid})' )

        run_sessions = []
        for i in range(0, len(self._plan.sessions)):
            plan_session = self._plan.sessions[i]
            session_name = plan_session.name if plan_session.name else f'{self._plan.name}/{str(i)}'
            run_session = TestRunSession(session_name, plan_session)
            run_sessions.append(run_session)
            run_session.run()

        self._report_test_results(self._plan, run_sessions)

