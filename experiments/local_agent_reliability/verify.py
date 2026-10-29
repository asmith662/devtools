"""Effect-free integrity/native/retained-output verification, never live inference."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from devtools.agents.coding.compaction.format import summary_payload, validate_summary
from devtools.models.interaction import ModelToolCall, Prompt, PromptMessage

HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    freeze = load(HERE / "freeze.json")
    for path, expected in freeze["files"].items():
        assert hashlib.sha256((HERE / path).read_bytes()).hexdigest() == expected, path
    result = load(HERE / "evidence/result.json")
    original = load(HERE / "history.json")["request"]["prompt"]["messages"]
    assert result["messages"][:len(original)] == original
    assert result["history_prefix_unchanged"]
    assert not result["result"]["candidate_validated"]
    assert result["result"]["disposition"] == "proposal_limit"
    assert result["result"]["custody"]["restored"]
    assert not result["result"]["custody"]["reconciliation_required"]
    acting = [load(p) for p in sorted((HERE / "evidence").glob("acting-*.json"))]
    assert len(acting) == 5
    read_calls = []
    for entry in acting:
        assert entry["entered"]
        messages = tuple(PromptMessage(**{
            **m, "tool_calls": tuple(ModelToolCall(**c) for c in m["tool_calls"]),
        }) for m in entry["request"]["prompt"]["messages"])
        Prompt("", "messages", messages)
        assert "UNTRUSTED DERIVED" not in str(messages)
        for call in entry["response"]["tool_calls"]:
            if call["name"] == "read_source":
                args = json.loads(call["arguments_json"])
                assert args["start"] == 0 and "end" not in args
                read_calls.append(call["provider_call_id"])
    assert len(read_calls) == 6
    feedback = {m["tool_call_id"]: json.loads(m["content"]) for m in result["messages"] if m["role"] == "tool"}
    for identity in read_calls:
        value = feedback[identity]
        assert value["span"] == value["valid_range"] == [0, value["source_length"]]
        assert value["continuation_start"] == value["source_length"]
        assert len(value["text"]) == value["source_length"]
        assert not value["partial"]
        assert value["maximum_bytes"] == 8192
    assert any(v.get("reason") == "Edit anchors overlap." for v in feedback.values())
    assert len(result["checks"]) == 1
    assert result["checks"][0][0]["command_result"]["exit_code"] == 1
    assert load(HERE / "evidence/grade.json")["exit_code"] == 1
    auxiliary = load(HERE / "evidence/summary-1.json")
    assert auxiliary["request"]["provider_settings"]["response_format"] == "json_object"
    raw = auxiliary["response"]["content"]
    try:
        json.loads(raw)
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("Primary strict JSON unexpectedly valid")
    assert not result["attempts"][0]["adopted"]
    assert result["attempts"][0]["error"]["type"] == "JSONDecodeError"
    facts = json.loads(auxiliary["request"]["prompt"]["messages"][1]["content"])
    payload, normalized = summary_payload(raw, allow_json_fence=True)
    note = validate_summary(payload, {int(i): r["digest"] for i, r in facts["records"].items()}, frozenset(facts["replacement_indices"]), {})
    assert normalized and note.role == "assistant" and not note.tool_calls
    analysis = load(HERE / "analysis.json")
    assert analysis["offline_projection_bytes"] == 4301
    assert analysis["offline_source_witnesses"] == 0
    assert analysis["frozen_focus_oracle_defect"]["correct_expected"] == 2
    assert "(2, 6), 3" in (HERE / "fixture/focused.py").read_text(encoding="utf-8")
    print("Frozen inputs, 5 acting requests, 6 correlated reads, strict rejection, offline envelope validation and qualified oracle defect verified; no inference or effect replay.")


if __name__ == "__main__":
    main()
