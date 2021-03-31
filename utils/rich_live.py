import time
import random

from rich.live import Live
from rich.table import Table
from rich.console import Console

import os
os.system('cls||clear')


console = Console()

# ----------- Task looper ----------- #
tasks = [f"task {n}" for n in range(1, 6)]

with console.status("[bold green]Working on tasks...") as status:
    while tasks:
        task = tasks.pop(0)
        time.sleep(0.5)
        console.log(f"{task} complete")


def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(
            f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
        )
    return table


with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(10):
        time.sleep(0.4)
        live.update(generate_table())

table = Table("foo", "bar", "baz")
table.add_row("1", "2", "3")
console.print(table)