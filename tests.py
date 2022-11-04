from quartodoc import get_function, MdRenderer
from griffe.docstrings import dataclasses as ds


def test_get_function():
    f_obj = get_function("quartodoc", "get_function")

    assert f_obj.name == "get_function"
    assert any(isinstance(x, ds.DocstringSectionExamples) for x in f_obj.docstring.parsed)


def test_render_to_md():
    # TODO: use snapshots?
    f_obj = get_function("quartodoc", "get_function")

    renderer = MdRenderer()
    assert isinstance(renderer.to_md(f_obj), str)
