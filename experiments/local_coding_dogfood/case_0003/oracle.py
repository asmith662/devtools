"""Frozen independent negative and freshness controls; never disclosed to model."""
import asyncio
import json
from dataclasses import replace

import pytest

from devtools.context import RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from devtools.models.interaction import ModelResponse, ModelToolCall, InteractionSource, PromptMessage
from devtools.resources.filesystem import TextFile, write
from devtools.tools.errors import ToolInputError
from devtools.tools.source import SourceScope
from tests.agents.coding.test_inventory import inventory, make_host, progress


def test_refreshed_metadata(tmp_path):
    host=make_host(tmp_path)
    before=inventory(asyncio.run(host.prepare(progress())))
    path=tmp_path/'package/source.py';write(TextFile(resolve_path(path),'# new semantic bytes\nvalue = 9\n'))
    host.scope=SourceScope.observe(root=host.scope.root,repository=__import__('devtools.context',fromlist=['Repository']).Repository(host.scope.snapshot.repository_id),addresses=tuple(r.address for r in host.scope.snapshot.resources))
    after=inventory(asyncio.run(host.prepare(progress())))
    assert after['snapshot_id']==str(host.scope.snapshot.id)!=before['snapshot_id']
    row=next(r for r in after['resources'] if r['address']=='package/source.py')
    assert row['content_identity']==str(ContentIdentity.from_text('# new semantic bytes\nvalue = 9\n'))
    assert len(host.disclosures)==0


def test_native_feedback_retained(tmp_path):
    host=make_host(tmp_path)
    state=progress();asyncio.run(host.prepare(state))
    call=ModelToolCall('read_source',json.dumps({'path':'package/source.py','start':0,'end':7}), 'independent-native-id')
    response=ModelResponse('',source=InteractionSource('independent-host'),tool_calls=(call,))
    assert host.classify(response)=='acquire'
    asyncio.run(host.acquire(response))
    request=asyncio.run(host.prepare(state))
    assert inventory(request)['source_acquired'] is False
    feedback=[m for m in request.prompt.messages if m.role=='tool']
    assert len(feedback)==1 and feedback[0].tool_call_id=='independent-native-id'
    assert len(host.disclosures)==1


def test_metadata_not_edit_witness(tmp_path):
    host=make_host(tmp_path);asyncio.run(host.prepare(progress()))
    call=ModelToolCall('replace_source',json.dumps({'path':'package/source.py','old_text':"value = 'é'",'new_text':'value = 1'}),'no-witness')
    response=ModelResponse('',source=InteractionSource('independent-host'),tool_calls=(call,))
    assert asyncio.run(host.propose(response)) is None
    assert (tmp_path/'package/source.py').read_text(encoding='utf-8').endswith("value = 'é'\n")


def test_escaped_address_and_utf8_metadata(tmp_path):
    host=make_host(tmp_path)
    address=RepositoryResourceAddress('package/naïve [part].py')
    text='private-unicode-λ\n';write(TextFile(resolve_path(tmp_path/address.value),text))
    host.scope=SourceScope.observe(root=host.scope.root,repository=__import__('devtools.context',fromlist=['Repository']).Repository(host.scope.snapshot.repository_id),addresses=tuple(r.address for r in host.scope.snapshot.resources)+(address,))
    request=asyncio.run(host.prepare(progress()));data=inventory(request)
    row=next(r for r in data['resources'] if r['address']==address.value)
    assert row['byte_size']==len(text.encode('utf-8')) and row['editable'] is False
    assert row['content_identity']==str(ContentIdentity.from_text(text))
    assert 'private-unicode-λ' not in '\n'.join(m.content for m in request.prompt.messages)
