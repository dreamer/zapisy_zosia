from django import template

register = template.Library()

class WikiBlurbNode(template.Node):
    # usage: {% wiki_blurb <id> %}
    # id will be string name used to 
    # identify particular blurb

    def __init__(self, id_string, is_staff):
        self.id_string = id_string
        self.is_staff  = is_staff

    def render(self, context):
        return u"<strong>bar</strong> <a>[edit:%s] %s</a>" % (self.id_string, self.is_staff)


@register.tag(name="wiki_blurb")
def do_wiki_blurb(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, id_string, is_staff = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires id_string argument" % token.contents.split()[0]
    return WikiBlurbNode(id_string, is_staff)

