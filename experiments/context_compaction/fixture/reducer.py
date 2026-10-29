"""Aggregate accepted event deltas by stream with retry suppression."""

from rules import accepted


def totals(events):
    seen = set()
    result = {}
    for event in events:
        identity = event["id"]
        if identity in seen:
            continue
        seen.add(identity)
        if accepted(event):
            stream = event["stream"]
            result[stream] = result.get(stream, 0) + event["delta"]
    return result
