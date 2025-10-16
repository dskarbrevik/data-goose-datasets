import typer
from pathlib import Path
from datetime import datetime
from dgd.compilers import factscore as fs

app = typer.Typer()

scrape_app = typer.Typer()
app.add_typer(scrape_app, name="scrape")

@scrape_app.command()
def factscore(
    data_path: str = typer.Argument(..., help="Path to the FactScore dataset directory"),
    output: str = typer.Option(..., "-o", "--output", help="Path to write the scraped articles as JSONL or directory for output"),
    language: str = typer.Option('en', help="Wikipedia language code (default: 'en')")
):
    """Scrape Wikipedia articles for the FactScore dataset and write to JSONL."""


    output_path = Path(output)
    if output_path.is_dir() or output_path.suffix == '':
        # If output is a directory or has no extension, treat as directory
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"factscore_wikiscrape_{timestamp}.jsonl"
        output_file = output_path / filename
    else:
        # If output is a file, check extension
        if output_path.suffix != '.jsonl':
            typer.echo("Error: Output file must have a .jsonl extension.", err=True)
            raise typer.Exit(code=1)
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_file = output_path

    fs.compile(data_path=data_path, 
               language=language, 
               output_jsonl_path=output_file)

if __name__ == "__main__":
    app()
