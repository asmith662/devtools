"""A side-effect-free command projection used by an external UI."""

from .paths import artifact_filename


def selection_summary(catalog, project, platform, *, include_previews=False):
    selected = catalog.choose(project, platform, include_previews=include_previews)
    if selected is None:
        return {"status": "unavailable"}
    return {
        "status": "selected",
        "version": selected.version,
        "uri": selected.uri,
        "filename": artifact_filename(selected),
    }
