from time import sleep
from rich.console import Console
import os
os.system('cls||clear')



console = Console()

# ----------- Rich Markdown ----------- #
from rich.markdown import Markdown
console = Console()
with open("README.md") as md:
    markdown = Markdown(md.read())
# console.print(markdown)


# ------------ Rich Tables ------------ #
from rich.table import Table

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row(
    "Dev 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
)
table.add_row(
    "May 25, 2018",
    "[red]Solo[/red]: A Star Wars Story",
    "$275,000,000",
    "$393,151,347",
)
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    "[bold]$1,332,539,889[/bold]",
)
console.print(table)



# ----------- Task looper ----------- #
tasks = [f"task {n}" for n in range(1, 6)]

with console.status("[bold green]Working on tasks...") as status:
    while tasks:
        task = tasks.pop(0)
        sleep(0.5)
        console.log(f"{task} complete")
