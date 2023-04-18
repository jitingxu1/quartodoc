from quartodoc import get_object, get_function, MdRenderer
from griffe.docstrings import dataclasses as ds
from griffe import dataclasses as dc


def test_get_function():
    f_obj = get_function("quartodoc", "get_function")

    assert f_obj.name == "get_function"
    assert any(
        isinstance(x, ds.DocstringSectionExamples) for x in f_obj.docstring.parsed
    )


def test_renderer_render():
    # TODO: use snapshots?
    f_obj = get_function("quartodoc", "get_function")

    renderer = MdRenderer()
    assert isinstance(renderer.render(f_obj), str)


def test_replace_docstring():
    from quartodoc.autosummary import get_object, replace_docstring
    from quartodoc.tests.example_dynamic import f

    obj = get_object("quartodoc", "tests.example_dynamic.f")
    old = obj.docstring

    replace_docstring(obj, f)
    assert obj.docstring is not old

    # just check the end of the piece dynamically added to docstring, since
    # griffe strips the left padding from docstrings.
    assert obj.docstring.value.endswith("I am a note")


def test_attribute_docstring():
    a = get_object("quartodoc", "tests.example_attribute.a")
    assert a.docstring.value == "I am an attribute docstring"


def test_class_attribute_docstring():
    a = get_object("quartodoc", "tests.example_attribute.SomeClass.a")
    assert a.docstring.value == "I am a class attribute docstring"


def test_render_attribute():
    # TODO: snapshot tests
    a = get_object("quartodoc", "tests.example_attribute.a")

    assert (
        MdRenderer().render(a)
        == "`tests.example_attribute.a`\n\nI am an attribute docstring"
    )


def test_get_object_dynamic_module_root():
    obj = get_object("quartodoc", dynamic=True)
    assert isinstance(obj, dc.Module)
    assert obj.path == "quartodoc"


def test_get_object_dynamic_module():
    obj = get_object("quartodoc.renderers", dynamic=True)
    assert isinstance(obj, dc.Module)
    assert obj.path == "quartodoc.renderers"


def test_get_object_dynamic_function():
    obj = get_object("quartodoc.tests.example_dynamic:f", dynamic=True)
    assert obj.docstring.value.endswith("I am a note")


def test_get_object_dynamic_class_method_doc():
    obj = get_object("quartodoc.tests.example_dynamic:AClass", dynamic=True)

    meth = obj.members["dynamic_doc"]
    assert meth.docstring.value == "A dynamic method"


def test_get_object_dynamic_class_method_doc():
    obj = get_object("quartodoc.tests.example_dynamic:AClass", dynamic=True)

    meth = obj.members["dynamic_create"]
    assert meth.docstring.value == "A dynamic method"