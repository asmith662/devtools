"""Transport status is independent of event identity."""


def accepted(event):
    return event["status"] == "accepted"
