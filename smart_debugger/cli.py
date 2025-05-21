import typer
from rich import print
from smart_debugger.parser import parse_error_log
from smart_debugger.context_builder import extract_code_context
from smart_debugger.llm_client import get_llm_suggestion

app = typer.Typer()

@app.command()
def run(
    log: str = typer.Option(..., help="Path to the error log file"),
    codebase: str = typer.Option(..., help="Path to the codebase directory")
):
    print(f"[bold blue]Log file:[/bold blue] {log}")
    print(f"[bold blue]Codebase directory:[/bold blue] {codebase}\n")

    # Step 1: Parse error log
    stack, error_msg = parse_error_log(log)

    print("[bold yellow]Parsed Stack Trace:[/bold yellow]")
    for entry in stack:
        print(f"[cyan]{entry['file']}[/cyan]: line {entry['line']} in [green]{entry['function']}[/green]")

    print(f"\n[red bold]Error:[/red bold] {error_msg}\n")

    # Step 2: Extract code snippets
    context = extract_code_context(stack, codebase)
    print("[bold magenta]Code Snippets Around Error:[/bold magenta]")
    for item in context:
        print(f"\n[bold underline]{item['file']}[/bold underline] at line {item['line']}:")
        print(f"[dim]{item['snippet']}[/dim]")

    # Step 3: Call LLM for suggestions
    print("\n[bold green]Getting suggestions from LLM...[/bold green]\n")
    suggestion = get_llm_suggestion(error_msg, context)

    print("[bold green]LLM Suggestion:[/bold green]")
    print(suggestion)


if __name__ == "__main__":
    app()
