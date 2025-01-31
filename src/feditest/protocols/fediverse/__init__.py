"""
Abstractions for nodes that speak today's Fediverse protocol stack.
"""

from feditest.protocols import NotImplementedByNodeError
from feditest.protocols.activitypub import ActivityPubNode
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer


class FediverseNode(WebFingerClient, WebFingerServer, ActivityPubNode):
    """
    A Node that can participate in today's Fediverse.
    The methods defined on FediverseNode reflect -- well, try to start reflecting, we are only
    learning what those are -- what users expect of the Fediverse.
    The methods here do not reflect the entire expressiveness of ActivityPub and ActivityStreams,
    only the subset relevant for interop in today's Fediverse. (As we broaden support for
    more applications, that list and the exposed variations may grow.)
    """

    def make_create_note(self, actor_uri: str, content: str, deliver_to: list[str] | None = None) -> str:
        """"
        Perform whatever actions are necessary so the actor with actor_uri will have created
        a Note object on this Node with the specified content.
        deliver_to: make sure the Node is delivered to these Actors (i.e. in arrives in their inbox)
        return: URI to the Note object
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_create_note)


    def make_announce_object(self, actor_uri, announced_object_uri: str) -> str:
        """
        Perform whatever actions are necessary so the actor with actor_uri will have created
        an Announce object on this Node announcing the object with announced_object_uri.
        return: URI to the Announce object
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_announce_object)


    def make_reply_note(self, actor_uri, replied_object_uri: str, reply_content: str) -> str:
        """
        Perform whatever actions are necessary so the actor with actor_uri will have created
        a Note object that replies to the object at replied_object_uri with the specified content.
        return: URI to the Reply object
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_reply_note)


    def make_follow(self, actor_uri: str, to_follow_actor_uri: str) -> None:
        """
        Perform whatever actions are necessary so the actor with actor_uri will have created
        a Follow activity for the Actor with to_follow_actor_uri.
        No return value: we already have the to_follow_actor_uri
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_follow)


    def set_auto_accept_follow(self, actor_uri: str, auto_accept_follow: bool = True) -> None:
        """
        Configure the behavior of this Node for the Actor with actor_uri so that when
        Follow requests come in, they are automatically accepted.
        This method exists so that implementations can throw a NotImplementedByNodeError
        if they do not have the requested behavior (or it cannot be scripted) and
        the corresponding tests does not run.
        """
        raise NotImplementedByNodeError(self, FediverseNode.set_auto_accept_follow)


    def make_follow_accept(self, actor_uri: str, follower_actor_uri: str) -> None:
        """
        Perform whatever actions are necessary so the actor with actor_uri will have created
        an Accept activity for a Follow request by the Actor with follower_actor_uri.
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_follow_accept)


    def make_follow_reject(self, actor_uri: str, follower_actor_uri: str) -> None:
        """
        Perform whatever actions are necessary so the actor with actor_uri will have created
        a Reject activity for a Follow request by the Actor with follower_actor_uri.
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_follow_reject)


    def make_follow_undo(self, actor_uri: str, follower_actor_uri: str) -> None:
        """
        Perform whatever actions are necessary so the actor with actor_uri will have created
        an Undo activity for a Follow Accept withy the Actor with follower_actor_uri.
        """
        raise NotImplementedByNodeError(self, FediverseNode.make_follow_undo)


    def wait_until_actor_has_received_note(self, actor_uri: str, object_uri: str, max_wait: float = 5.) -> None:
        """
        Wait until the object at object_uri has arrived with the Actor at actor_uri.
        This method does not state that the object needs to have arrived in the Actor's, inbox,
        as Nodes might implement different routing strategies (including antispam).
        If the condition has not arrived by the time max_wait seconds have passed, throw
        a TimeoutException.
        """
        raise NotImplementedByNodeError(self, FediverseNode.wait_until_actor_has_received_note)


    def wait_until_actor_is_following_actor(self, actor_uri: str, to_be_followed_uri: str, max_wait: float = 5.) -> None:
        """
        Wait until the Actor at actor_uri is following the Actor at to_be_followed_uri on this Node.
        If the condition has not arrived by the time max_wait seconds have passed, throw
        a TimeoutException.
        """
        raise NotImplementedByNodeError(self, FediverseNode.wait_until_actor_is_following_actor)


    def wait_until_actor_is_followed_by_actor(self, actor_uri: str, to_be_following_uri: str, max_wait: float = 5.) -> None:
        """
        Wait until the Actor at actor_uri is being followed by the Actor with to_be_following_uri on this Node.
        If the condition has not arrived by the time max_wait seconds have passed, throw
        a TimeoutException.
        """
        raise NotImplementedByNodeError(self, FediverseNode.wait_until_actor_is_followed_by_actor)
