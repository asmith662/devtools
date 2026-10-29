"""Private oracle preflight: reference observations, never a host implementation."""
import asyncio
import copy
import json
from types import SimpleNamespace

import pytest

from focused import assert_metadata, inventory, make_host
from devtools.context.repository.resource import ContentIdentity
from devtools.models.interaction import PromptMessage
from devtools.evaluation.preflight import OracleComparison, check_oracle_expectations


def assert_contract(data,host):
    assert data['repository_id']==str(host.scope.snapshot.repository_id)
    assert data['snapshot_id']==str(host.scope.snapshot.id)
    assert data['source_acquired'] is False
    resources={r['address']:r for r in data['resources']}
    assert len(resources)==len(data['resources'])==2
    assert set(resources)=={'README.md','package/source.py'}
    for path,editable in [('README.md',False),('package/source.py',True)]:
        raw=(host.scope.root.value/path).read_bytes()
        assert resources[path]==dict(address=path,content_identity=str(ContentIdentity.from_text(raw.decode('utf-8'))),byte_size=len(raw),editable=editable)


def reference(host):
    # Independent literal addresses and raw filesystem bytes, no candidate helper.
    return dict(repository_id=str(host.scope.snapshot.repository_id),snapshot_id=str(host.scope.snapshot.id),source_acquired=False,resources=[dict(address=p,content_identity=str(ContentIdentity.from_text((host.scope.root.value/p).read_bytes().decode('utf-8'))),byte_size=(host.scope.root.value/p).stat().st_size,editable=e) for p,e in [('README.md',False),('package/source.py',True)]])


def test_reference_observations_and_cross_checks(tmp_path):
    host=make_host(tmp_path);data=reference(host);assert_contract(data,host);assert_metadata(data,host)
    request=SimpleNamespace(prompt=SimpleNamespace(messages=(PromptMessage('user',host.objective.text),PromptMessage('user',json.dumps(data)))))
    assert inventory(request)==data
    cases=(
      OracleComparison('scope','inventory','normal',2,len({'README.md','package/source.py'}),'independently authored permitted-address set'),
      OracleComparison('unicode','inventory','boundary',1,len('é'.encode('utf-8'))-len('é'),'UTF-8 two-byte encoding versus one codepoint'),
      OracleComparison('empty-file','inventory','empty',0,len(b''),'empty byte sequence'),
      OracleComparison('clip','review','boundary',2,sum(any(a<=x<b for a,b in [(1,3),(5,8)]) for x in range(2,6)),'enumerated half-open unit cells, not literal summation'),
    )
    assert check_oracle_expectations(obligations=('inventory','review'),comparisons=cases)==()


@pytest.mark.parametrize('mutation',['bytes','missing','foreign','duplicate','editable','source-credit','identity'])
def test_oracle_rejects_wrong_observations(tmp_path,mutation):
    host=make_host(tmp_path);data=reference(host)
    if mutation=='bytes':data['resources'][1]['byte_size']-=1
    if mutation=='missing':data['resources'].pop()
    if mutation=='foreign':data['resources'][0]['address']='outside.py'
    if mutation=='duplicate':data['resources'].append(copy.deepcopy(data['resources'][0]))
    if mutation=='editable':data['resources'][0]['editable']=True
    if mutation=='source-credit':data['source_acquired']=True
    if mutation=='identity':data['snapshot_id']='foreign'
    with pytest.raises(AssertionError):assert_contract(data,host)


def test_original_wrong_expectation_is_rejected():
    cases=(OracleComparison('clip','clip','normal',3,sum(any(a<=x<b for a,b in [(1,3),(5,8)]) for x in range(2,6)),'unit cells'),OracleComparison('edge','clip','boundary',0,len(set()),'empty intersection'),OracleComparison('empty','clip','empty',0,len(set()),'empty reservations'))
    assert check_oracle_expectations(obligations=('clip',),comparisons=cases)==('clip: expected value disagrees with cross-check.',)


def test_full_oracle_positive_control(tmp_path,monkeypatch):
    """Hidden finite reference, never installed as the worker's implementation."""
    import focused
    import heldout
    from devtools.agents.coding.repository import RepositoryCodingHost

    class ReferenceObservationHost(RepositoryCodingHost):
        async def prepare(self,state):
            self.scope.check_current()
            # Derive bytes/identities independently from raw authorized files.
            rows=[]
            for resource in self.scope.snapshot.resources:
                raw=(self.scope.root.value/resource.address.value).read_bytes()
                rows.append(dict(address=resource.address.value,content_identity=str(ContentIdentity.from_text(raw.decode('utf-8'))),byte_size=len(raw),editable=resource.address in self.objective.editable))
            note=PromptMessage('user',json.dumps(dict(repository_id=str(self.scope.snapshot.repository_id),snapshot_id=str(self.scope.snapshot.id),source_acquired=False,resources=rows)))
            if len(self.messages)>1 and self.messages[1].role=='user':self.messages[1]=note
            else:self.messages.insert(1,note)
            return await super().prepare(state)

    monkeypatch.setattr(focused,'RepositoryCodingHost',ReferenceObservationHost)
    checks=(focused.test_first_request_scoped_inventory,focused.test_inventory_not_duplicated_on_prepare,focused.test_inventory_charged_to_prompt_budget,focused.test_inventory_does_not_bypass_currentness,heldout.test_current_snapshot_not_cached,heldout.test_metadata_cannot_authorize_edit,heldout.test_native_correlation_and_metadata_coexist,heldout.test_empty_resource_unicode_and_readonly,heldout.test_projection_preserves_metadata_and_objective,heldout.test_utf8_size_differs_from_character_count)
    for index,check in enumerate(checks):
        root=tmp_path/str(index);root.mkdir();check(root)
