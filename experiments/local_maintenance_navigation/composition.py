"""Experimental recording and fixed procedure exposure; no private source search."""
from __future__ import annotations
import json
from dataclasses import replace
import support as s
from devtools.agents.coding.models import CodingEffect
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.agents.model_tools import execute_model_tool_call,normalize_tool_descriptor
from devtools.models.interaction import PromptMessage
from devtools.tools import ToolDescriptor,ToolRunner

PROCEDURE=ToolDescriptor('inspect_and_validate_change','Inspect authorized changes and execute host-fixed checks. No command or scope arguments.','{"type":"object","maxProperties":0}')

class Invocation:
    descriptor=PROCEDURE
    def materialize(self,arguments):
        if json.loads(arguments)!={}:raise ValueError('Fixed procedure accepts no arguments')
        return None

async def execute_procedure(tool):
    try:return await ToolRunner().execute(tool,None)
    finally:
        if tool.last_report is not None:s.OBSERVATIONS.extend(tool.last_report.observations)

class Host(RepositoryCodingHost):
    def build_request(self,messages):
        request=super().build_request(messages)
        return replace(request,tools=(*request.tools,normalize_tool_descriptor(PROCEDURE)),provider_settings=s.LlamaCppRequestSettings(**s.QWEN38_INSTRUCT_SAMPLING))

    def classify(self,response):
        if any(c.name==PROCEDURE.name for c in response.tool_calls) and all(c.name in {'read_source','read_source_unit','find_source','validate_candidate',PROCEDURE.name} for c in response.tool_calls):
            self.scope.check_current()
            self.messages.append(PromptMessage('assistant',response.content,response.tool_calls))
            return 'acquire'
        return super().classify(response)

    async def acquire(self,response):
        if len(response.tool_calls)>self.progress.limits.tool_actions-self.progress.actions:raise ValueError('Frozen acquisition budget exceeded')
        ready=False
        for call in response.tool_calls:
            if call.name!=PROCEDURE.name:
                before=len(self.messages)
                try:ready=await super().acquire(replace(response,tool_calls=(call,))) or ready
                finally:
                    for message in self.messages[before:]:
                        if message.role=='tool':self.acquisitions.append(dict(kind='source' if call.name in {'read_source','read_source_unit'} else 'navigation' if call.name=='find_source' else 'model-check',call_id=call.provider_call_id,name=call.name,arguments=call.arguments_json,result=json.loads(message.content)))
                continue
            effect=self.progress.claim_action(call.provider_call_id)
            tool=procedure_tool(self.scope.root.value,self.scope,self.revision,'model-procedure-'+str(self.progress.actions))
            try:report=await execute_model_tool_call(call,invocation=Invocation(),tool=tool,admit=self.authorize,runner=ToolRunner())
            finally:
                if tool.last_report is not None:s.OBSERVATIONS.extend(tool.last_report.observations)
            self.procedures.append(dict(trigger='model',call_id=call.provider_call_id,report=s.plain(report)))
            effect.acknowledged=True
            value=dict(status=report.status,checks=[dict(status=c.status,exit_code=c.result.command_result.exit_code if c.result else None,stdout=c.result.command_result.stdout.decode(errors='replace') if c.result else None,stderr=c.result.command_result.stderr.decode(errors='replace') if c.result else None) for c in report.checks])
            self.messages.append(PromptMessage('tool',json.dumps(value),tool_call_id=call.provider_call_id))
        return ready

    async def propose(self,response):
        result=await super().propose(response)
        available=self.active_disclosures if self.projection is not None else tuple(self.disclosures)
        self.proposal_events.append(dict(snapshot=str(self.scope.snapshot.id),calls=s.plain(response.tool_calls),admitted=result is not None,source_disclosures=[dict(path=str(d.unit.resource.address),content_identity=str(d.unit.resource.content_identity),span=d.span,snapshot=str(d.snapshot_id)) for d in available],changes=s.plain(result)))
        return result

    async def check(self,proposal):
        del proposal
        effect=CodingEffect('check',(),check_name='focused-acceptance');self.progress.effects.append(effect)
        report=await execute_procedure(procedure_tool(self.scope.root.value,self.scope,self.revision,'host-check-'+str(len(self.check_results))))
        self.procedures.append(dict(trigger='deterministic-host-validation',report=s.plain(report)))
        self.check_results.append(tuple(c.result for c in report.checks if c.result is not None))
        if report.error is not None:raise report.error
        if report.status not in {'passed','failed'}:raise RuntimeError('Fixed check procedure refused or incomplete')
        effect.acknowledged=True
        return report.status=='passed'
