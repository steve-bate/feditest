# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feditest/nodedrivers/grpc/node.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$feditest/nodedrivers/grpc/node.proto\x12!feditest.nodedrivers.grpc.service\"$\n\x0f\x41\x63torUriRequest\x12\x11\n\trole_name\x18\x01 \x01(\t\"\"\n\rActorUriReply\x12\x11\n\tactor_uri\x18\x01 \x01(\t\"-\n\x18\x41\x63torFollowersUriRequest\x12\x11\n\tactor_uri\x18\x01 \x01(\t\"%\n\x16\x41\x63torFollowersUriReply\x12\x0b\n\x03uri\x18\x01 \x01(\t\"-\n\x18\x41\x63torFollowingUriRequest\x12\x11\n\tactor_uri\x18\x01 \x01(\t\"%\n\x16\x41\x63torFollowingUriReply\x12\x0b\n\x03uri\x18\x01 \x01(\t\"k\n\x13\x43reateObjectRequest\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x11\n\tactor_uri\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x12\n\ninbox_kind\x18\x04 \x01(\t\x12\x0e\n\x06to_uri\x18\x05 \x01(\t\"=\n\x11\x43reateObjectReply\x12\x14\n\x0c\x61\x63tivity_uri\x18\x01 \x01(\t\x12\x12\n\nobject_uri\x18\x02 \x01(\t\"B\n\x19WaitForInboxObjectRequest\x12\x11\n\tactor_uri\x18\x01 \x01(\t\x12\x12\n\nobject_uri\x18\x02 \x01(\t\",\n\x17WaitForInboxObjectReply\x12\x11\n\tsucceeded\x18\x01 \x01(\x08\">\n\x15\x41nnounceObjectRequest\x12\x11\n\tactor_uri\x18\x01 \x01(\t\x12\x12\n\nobject_uri\x18\x02 \x01(\t\"R\n\x13\x41nnounceObjectReply\x12\x11\n\tsucceeded\x18\x01 \x01(\x08\x12\x14\n\x0c\x61\x63tivity_uri\x18\x02 \x01(\t\x12\x12\n\nobject_uri\x18\x03 \x01(\t\"N\n\x14ReplyToObjectRequest\x12\x11\n\tactor_uri\x18\x01 \x01(\t\x12\x12\n\nobject_uri\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"Q\n\x12ReplyToObjectReply\x12\x11\n\tsucceeded\x18\x01 \x01(\x08\x12\x14\n\x0c\x61\x63tivity_uri\x18\x02 \x01(\t\x12\x12\n\nobject_uri\x18\x03 \x01(\t\"M\n\x12\x46ollowActorRequest\x12\x1b\n\x13\x66ollowing_actor_uri\x18\x01 \x01(\t\x12\x1a\n\x12\x66ollowed_actor_uri\x18\x02 \x01(\t\"$\n\x10\x46ollowActorReply\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x02 \x01(\x08\"G\n\x19\x43ollectionContainsRequest\x12\x12\n\nobject_uri\x18\x01 \x01(\t\x12\x16\n\x0e\x63ollection_uri\x18\x02 \x01(\t\")\n\x17\x43ollectionContainsReply\x12\x0e\n\x06result\x18\x01 \x01(\x08\x32\xdf\t\n\x13\x46\x65\x64itestNodeService\x12u\n\x0bGetActorUri\x12\x32.feditest.nodedrivers.grpc.service.ActorUriRequest\x1a\x30.feditest.nodedrivers.grpc.service.ActorUriReply\"\x00\x12\x8f\x01\n\x13GetActorFollowerUri\x12;.feditest.nodedrivers.grpc.service.ActorFollowersUriRequest\x1a\x39.feditest.nodedrivers.grpc.service.ActorFollowersUriReply\"\x00\x12\x90\x01\n\x14GetActorFollowingUri\x12;.feditest.nodedrivers.grpc.service.ActorFollowingUriRequest\x1a\x39.feditest.nodedrivers.grpc.service.ActorFollowingUriReply\"\x00\x12~\n\x0c\x43reateObject\x12\x36.feditest.nodedrivers.grpc.service.CreateObjectRequest\x1a\x34.feditest.nodedrivers.grpc.service.CreateObjectReply\"\x00\x12\x90\x01\n\x12WaitFprInboxObject\x12<.feditest.nodedrivers.grpc.service.WaitForInboxObjectRequest\x1a:.feditest.nodedrivers.grpc.service.WaitForInboxObjectReply\"\x00\x12\x84\x01\n\x0e\x41nnounceObject\x12\x38.feditest.nodedrivers.grpc.service.AnnounceObjectRequest\x1a\x36.feditest.nodedrivers.grpc.service.AnnounceObjectReply\"\x00\x12\x81\x01\n\rReplyToObject\x12\x37.feditest.nodedrivers.grpc.service.ReplyToObjectRequest\x1a\x35.feditest.nodedrivers.grpc.service.ReplyToObjectReply\"\x00\x12{\n\x0b\x46ollowActor\x12\x35.feditest.nodedrivers.grpc.service.FollowActorRequest\x1a\x33.feditest.nodedrivers.grpc.service.FollowActorReply\"\x00\x12\x90\x01\n\x12\x43ollectionContains\x12<.feditest.nodedrivers.grpc.service.CollectionContainsRequest\x1a:.feditest.nodedrivers.grpc.service.CollectionContainsReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'feditest.nodedrivers.grpc.node_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ACTORURIREQUEST']._serialized_start=75
  _globals['_ACTORURIREQUEST']._serialized_end=111
  _globals['_ACTORURIREPLY']._serialized_start=113
  _globals['_ACTORURIREPLY']._serialized_end=147
  _globals['_ACTORFOLLOWERSURIREQUEST']._serialized_start=149
  _globals['_ACTORFOLLOWERSURIREQUEST']._serialized_end=194
  _globals['_ACTORFOLLOWERSURIREPLY']._serialized_start=196
  _globals['_ACTORFOLLOWERSURIREPLY']._serialized_end=233
  _globals['_ACTORFOLLOWINGURIREQUEST']._serialized_start=235
  _globals['_ACTORFOLLOWINGURIREQUEST']._serialized_end=280
  _globals['_ACTORFOLLOWINGURIREPLY']._serialized_start=282
  _globals['_ACTORFOLLOWINGURIREPLY']._serialized_end=319
  _globals['_CREATEOBJECTREQUEST']._serialized_start=321
  _globals['_CREATEOBJECTREQUEST']._serialized_end=428
  _globals['_CREATEOBJECTREPLY']._serialized_start=430
  _globals['_CREATEOBJECTREPLY']._serialized_end=491
  _globals['_WAITFORINBOXOBJECTREQUEST']._serialized_start=493
  _globals['_WAITFORINBOXOBJECTREQUEST']._serialized_end=559
  _globals['_WAITFORINBOXOBJECTREPLY']._serialized_start=561
  _globals['_WAITFORINBOXOBJECTREPLY']._serialized_end=605
  _globals['_ANNOUNCEOBJECTREQUEST']._serialized_start=607
  _globals['_ANNOUNCEOBJECTREQUEST']._serialized_end=669
  _globals['_ANNOUNCEOBJECTREPLY']._serialized_start=671
  _globals['_ANNOUNCEOBJECTREPLY']._serialized_end=753
  _globals['_REPLYTOOBJECTREQUEST']._serialized_start=755
  _globals['_REPLYTOOBJECTREQUEST']._serialized_end=833
  _globals['_REPLYTOOBJECTREPLY']._serialized_start=835
  _globals['_REPLYTOOBJECTREPLY']._serialized_end=916
  _globals['_FOLLOWACTORREQUEST']._serialized_start=918
  _globals['_FOLLOWACTORREQUEST']._serialized_end=995
  _globals['_FOLLOWACTORREPLY']._serialized_start=997
  _globals['_FOLLOWACTORREPLY']._serialized_end=1033
  _globals['_COLLECTIONCONTAINSREQUEST']._serialized_start=1035
  _globals['_COLLECTIONCONTAINSREQUEST']._serialized_end=1106
  _globals['_COLLECTIONCONTAINSREPLY']._serialized_start=1108
  _globals['_COLLECTIONCONTAINSREPLY']._serialized_end=1149
  _globals['_FEDITESTNODESERVICE']._serialized_start=1152
  _globals['_FEDITESTNODESERVICE']._serialized_end=2399
# @@protoc_insertion_point(module_scope)
