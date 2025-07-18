import jinja2

SYS_PROMPT_PATH: str = "sys_prompt.jinja"


def get_system_prompt() -> jinja2.Template:
    with open(SYS_PROMPT_PATH, "r") as fin:
        return jinja2.Template(fin.read())
