import subprocess
from typing import Any

from feditest import nodedriver
from feditest.protocols import Node, NodeDriver


class SubprocessNode(Node):
    "Runs a program in a subprocess"
    def __init__(self, node_driver: "SubprocessNodeDriver", rolename: str, parameters: dict[str, Any]) -> None:
        super().__init__(rolename, node_driver)
        args = parameters["args"]
        self.process = subprocess.Popen(args, stdout=subprocess.PIPE)
        ...

    def stop(self):
        self.process.kill()

@nodedriver
class SubprocessNodeDriver(NodeDriver):

    def _provision_node(self, rolename: str, _: str, parameters: dict[str,Any] | None = None) -> Node:
        return SubprocessNode(self, rolename, parameters)
    
    def _unprovision_node(self, instance: Node) -> None:
        instance.stop()
