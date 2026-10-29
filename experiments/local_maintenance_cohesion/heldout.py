"""Withheld independent acceptance; never part of worker source scope."""
import asyncio
import json
from dataclasses import replace

import pytest

from focused import inventory, make_host, progress
from devtools.agents.coding.projection import ProjectionPolicy
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from devtools.models.interaction import InteractionSource, ModelResponse, ModelToolCall
from devtools.resources.filesystem import TextFile, write
from devtools.tools.source import SourceScope


def test_current_snapshot_not_cached(tmp_path):
    host=make_host(tmp_path)
    first=inventory(asyncio.run(host.prepare(progress())))
    text='value = 9\n'
    write(TextFile(resolve_path(tmp_path/'package/source.py'),text))
    host.scope=SourceScope.observe(root=host.scope.root,repository=Repository(host.scope.snapshot.repository_id),addresses=tuple(r.address for r in host.scope.snapshot.resources))
    data=inventory(asyncio.run(host.prepare(progress())))
    assert data['snapshot_id']==str(host.scope.snapshot.id)!=first['snapshot_id']
    row=next(r for r in data['resources'] if r['address']=='package/source.py')
    assert row['content_identity']==str(ContentIdentity.from_text(text))
    assert row['byte_size']==10


def test_metadata_cannot_authorize_edit(tmp_path):
    host=make_host(tmp_path);asyncio.run(host.prepare(progress()))
    response=ModelResponse('',source=InteractionSource('independent'),tool_calls=(ModelToolCall('replace_source',json.dumps(dict(path='package/source.py',old_text="value = 'é'",new_text='value = 0')),'not-read'),))
    assert asyncio.run(host.propose(response)) is None
    assert not host.disclosures and not host.source_results
    assert (tmp_path/'package/source.py').read_text(encoding='utf-8').endswith("value = 'é'\n")


def test_native_correlation_and_metadata_coexist(tmp_path):
    host=make_host(tmp_path);state=progress();asyncio.run(host.prepare(state))
    call=ModelToolCall('read_source',json.dumps(dict(path='package/source.py',start=0,end=7)),'heldout-source')
    response=ModelResponse('',source=InteractionSource('independent'),tool_calls=(call,))
    assert host.classify(response)=='acquire'
    asyncio.run(host.acquire(response));request=asyncio.run(host.prepare(state))
    assert inventory(request)['source_acquired'] is False
    feedback=[m for m in request.prompt.messages if m.role=='tool']
    assert len(feedback)==1 and feedback[0].tool_call_id=='heldout-source'
    assert json.loads(feedback[0].content)['text']=='# priva'
    assert len(host.disclosures)==1


def test_empty_resource_unicode_and_readonly(tmp_path):
    host=make_host(tmp_path)
    address=RepositoryResourceAddress('package/naïve [part].py')
    write(TextFile(resolve_path(tmp_path/address.value),''))
    host.scope=SourceScope.observe(root=host.scope.root,repository=Repository(host.scope.snapshot.repository_id),addresses=tuple(r.address for r in host.scope.snapshot.resources)+(address,))
    data=inventory(asyncio.run(host.prepare(progress())))
    row=next(r for r in data['resources'] if r['address']==address.value)
    assert row==dict(address=address.value,content_identity=str(ContentIdentity.from_text('')),byte_size=0,editable=False)


def test_projection_preserves_metadata_and_objective(tmp_path):
    host=make_host(tmp_path);host.projection=ProjectionPolicy(3000,2500)
    request=asyncio.run(host.prepare(progress()))
    assert request.prompt.messages[0].content==host.objective.text
    assert len(inventory(request)['resources'])==2
    assert not host.active_disclosures


def test_utf8_size_differs_from_character_count(tmp_path):
    host=make_host(tmp_path)
    row=next(r for r in inventory(asyncio.run(host.prepare(progress())))['resources'] if r['address']=='package/source.py')
    raw=(tmp_path/'package/source.py').read_bytes()
    assert row['byte_size']==len(raw)==len(raw.decode('utf-8'))+1
