from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("app/web/templates"),
    autoescape=select_autoescape()
)


def set_timezone():
    template = env.get_template("set_timezone.html")
    return template.render()
