import logging
import re
import time
from http import HTTPStatus
from threading import Thread
from typing import Any

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn import Config, Server

from feditest import nodedriver
from feditest.protocols import Node, NodeDriver
from feditest.protocols.fediverse import FediverseNode
from feditest.protocols.webfinger import WebFingerServer
from feditest.ubos import UbosNodeDriver

_RESOURCE_REGEX = re.compile("(?:.*?):[@~]?([^@]+)@?(.*)")


async def webfinger(request: Request):
    resource: str = request.query_params.get("resource")
    if resource is None or resource.startswith("="):  # Just a hack for now
        raise HTTPException(
            HTTPStatus.BAD_REQUEST.value, detail="Invalid resource"
        )
    
    if  "undefined" in resource:
        raise HTTPException(
            HTTPStatus.NOT_FOUND.value, detail="Resource not found"
        )
    
    m = _RESOURCE_REGEX.match(resource)
    if m:
        actor_uri = "http://server.test/actor"

        return JSONResponse(
            {
                "subject": resource,
                "links": [
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": actor_uri,
                    }
                ],
            }
        )
    else:
        raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Invalid resource format")

class WebFingerServerNode(WebFingerServer):
    "WebFinger server"
    def __init__(self, node_driver: "WebFingerServerNodeDriver", rolename: str, hostname: str) -> None:
        super().__init__(rolename, hostname, node_driver)
        self._actor_id = "actor"
        self._hostname = hostname
        app = Starlette()
        app.add_route("/.well-known/webfinger", webfinger)
        self._server = Server(Config(app=app, host="localhost", port=9999))
        self._server_thread: Thread = None
        self.log = logging.getLogger(type(self).__qualname__)

    def _start(self):
        self.log.info("Starting server")
        self._server.run()

    def start(self):
        self._server_thread = Thread(target=self._start)
        self._server_thread.start()
        time.sleep(1)
        self.log.info("Server started")

    def stop(self):
        self._server.should_exit = True
        self.log.info("Server shutdown")

    def obtain_account_identifier(self, nickname: str = None) -> str:
        """
        We simply return the admin account that we know exists.
        """
        return f"acct:{self._actor_id}@{self._hostname}"


    def obtain_non_existing_account_identifier(self, nickname: str = None ) ->str:
        return f"acct:undefined@{self._hostname}"


    def obtain_actor_document_uri(self, actor_rolename: str = None) -> str:
        return f"https://{self._hostname}/author/{self._actor_id}/"


@nodedriver
class WebFingerServerNodeDriver(NodeDriver):

    def _provision_node(self, rolename: str, hostname: str, parameters: dict[str, Any] | None = None) -> Node:
    #     return super()._provision_node(rolename, hostname, parameters)   
    # def _instantiate_node(self, site_id: str, rolename: str, hostname: str, admin_id: str) -> None:
        node = WebFingerServerNode(self, rolename, hostname)
        node.start()
        return node
    
    def _unprovision_node(self, instance: Node) -> None:
        instance.stop()
