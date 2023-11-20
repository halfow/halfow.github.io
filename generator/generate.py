from pathlib import Path
from time import sleep

from jinja2 import Environment, FileSystemLoader
from rich.console import Console

console = Console()

templates = Path(__file__).parent / "templates"
root = Path(__file__).parent.parent

jinja = Environment(loader=FileSystemLoader(templates))


def refresh():
    for template in jinja.list_templates():
        page = (root / template).with_suffix("")
        try:
            with page.open("w+") as file:
                file.write(jinja.get_template(template).render())
        except FileNotFoundError:
            page.parent.mkdir(parents=True, exist_ok=True)


def stats():
    return {template: template.stat().st_mtime for template in map(templates.joinpath, jinja.list_templates())}


def main():
    try:
        with console.status("Auto refresh"):
            refresh()
            last = stats()
            while True:
                files = stats()
                for file, time in files.items():
                    if last.get(file) != time:
                        console.log(f"Change detected {file.name!r}")
                        break
                else:
                    sleep(1)
                    continue
                last = files
                refresh()
    except KeyboardInterrupt as e:
        raise SystemExit(0) from e
