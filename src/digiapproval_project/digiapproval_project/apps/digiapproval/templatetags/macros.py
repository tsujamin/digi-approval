#
# templatetags/macros.py - Support for macros in Django templates
#
# Based on snippet by
#     Michal Ludvig <michal@logix.cz>
#     http://www.logix.cz/michal
#
# Extended for args and kwargs into templatetags/kwacro.py by
#     Skylar Saveland http://skyl.org
#     https://gist.github.com/skyl/1715202
#
# Modified to support rendering into context by matt@peloquin.com
#
"""

Usage example:

0) Save this file as <yourapp>/templatetags/macros.py

1) In your template load the library:
    {% load macros %}

2) Define a new macro called 'my_macro' that takes args and/or kwargs
   All will be optional.

    {% macro my_macro arg1 arg2 baz="Default baz" %}
        {% firstof arg1 "default_arg1" %}
        {% if arg2 %}{{ arg2 }}{% else %}default_arg2{% endif %}
        {{ baz }}
    {% endmacro %}

3) Use the macro with string parameters or context variables:

    {% usemacro my_macro "foo" "bar" baz="KW" %}
    <br>
    {% usemacro my_macro num_pages "bar" %}
    <br>
    {% setmacro my_macro %} {{ my_macro }}

    renders like

    foo bar KW
    77 bar Default baz
    default_arg1 default_arg2 Default baz

4) Alternatively save your macros in a separate file, e.g. "mymacro.html"
    and load it to the current template with:

        {% loadmacros "mymacros.html" %}

    Then use these loaded macros in as described above.

Bear in mind that defined and loaded macros are local to each template
file and are not inherited through {% extends ... %} tags.
"""

from django import template
from django.template import FilterExpression
from django.template.loader import get_template

register = template.Library()


def _setup_macros_dict(parser):
    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    try:
        ## Only try to access it to eventually trigger an exception
        parser._macros
    except AttributeError:
        parser._macros = {}


class DefineMacroNode(template.Node):
    def __init__(self, name, nodelist, args):

        self.name = name
        self.nodelist = nodelist
        self.args = []
        self.kwargs = {}
        for a in args:
            if "=" not in a:
                self.args.append(a)
            else:
                name, value = a.split("=")
                self.kwargs[name] = value

    def render(self, context):
        ## empty string - {% macro %} tag does no output
        return ''


@register.tag(name="macro")
def do_macro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, args = args[0], args[1], args[2:]
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
            % token.contents.split()[0])
        raise template.TemplateSyntaxError, m
    # TODO: could do some validations here,
    # for now, "blow your head clean off"
    nodelist = parser.parse(('endmacro', ))
    parser.delete_first_token()

    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_macros_dict(parser)
    parser._macros[macro_name] = DefineMacroNode(macro_name, nodelist, args)
    return parser._macros[macro_name]


class LoadMacrosNode(template.Node):
    def render(self, context):
        ## empty string - {% loadmacros %} tag does no output
        return ''


@register.tag(name="loadmacros")
def do_loadmacros(parser, token):
    try:
        tag_name, filename = token.split_contents()
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
            % token.contents.split()[0])
        raise template.TemplateSyntaxError, m
    if filename[0] in ('"', "'") and filename[-1] == filename[0]:
        filename = filename[1:-1]
    t = get_template(filename)
    macros = t.nodelist.get_nodes_by_type(DefineMacroNode)
    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_macros_dict(parser)
    for macro in macros:
        parser._macros[macro.name] = macro
    return LoadMacrosNode()


class UseMacroNode(template.Node):

    def __init__(self, macro, fe_args, fe_kwargs, context_only):
        self.macro = macro
        self.fe_args = fe_args
        self.fe_kwargs = fe_kwargs
        self.context_only = context_only

    def render(self, context):

        for i, arg in enumerate(self.macro.args):
            try:
                fe = self.fe_args[i]
                context[arg] = fe.resolve(context)
            except IndexError:
                context[arg] = ""

        for name, default in self.macro.kwargs.iteritems():
            if name in self.fe_kwargs:
                context[name] = self.fe_kwargs[name].resolve(context)
            else:
                context[name] = FilterExpression(default,
                                                 self.macro.parser
                                                 ).resolve(context)

        # Place output into context variable
        context[self.macro.name] = self.macro.nodelist.render(context)
        return '' if self.context_only else context[self.macro.name]


def parse_usemacro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, values = args[0], args[1], args[2:]
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
             % token.contents.split()[0])
        raise template.TemplateSyntaxError, m

    try:
        macro = parser._macros[macro_name]
    except (AttributeError, KeyError):
        m = "Macro '%s' is not defined" % macro_name
        raise template.TemplateSyntaxError, m

    fe_kwargs = {}
    fe_args = []

    for val in values:
        if "=" in val:
            # kwarg
            name, value = val.split("=")
            fe_kwargs[name] = FilterExpression(value, parser)
        else:  # arg
            # no validation, go for it ...
            fe_args.append(FilterExpression(val, parser))

    macro.name = macro_name
    macro.parser = parser
    return macro, fe_args, fe_kwargs


@register.tag(name="usemacro")
def do_usemacro(parser, token):
    return UseMacroNode(*parse_usemacro(parser, token), context_only=False)


@register.tag(name="setmacro")
def do_setmacro(parser, token):
    return UseMacroNode(*parse_usemacro(parser, token), context_only=True)
