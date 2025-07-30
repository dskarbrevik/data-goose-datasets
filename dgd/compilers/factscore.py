from dgd.scrapers.wikipedia_scraper import WikipediaScraper
import datasets

def get_entities(data_path: str) -> list[str]:
    """Gets entities from FActScore dataset"""

    dataset = datasets.load_from_disk(data_path)
    df = dataset.to_pandas()
    entities = df["entity"].unique().tolist()

    return entities


def compile(data_path: str, language: str = 'en', output_jsonl_path: str = None) -> None:
    """
    Scrapes Wikipedia articles for entities from the FActScore dataset and writes results to a JSONL file.
    Args:
        data_path: Path to the FActScore dataset.
        output_jsonl_path: Path to write the scraped articles as JSONL.
        language: Wikipedia language code (default 'en').
    """

    # get entities
    dataset = datasets.load_from_disk(data_path)
    df = dataset.to_pandas()
    entities = df["entity"].unique().tolist()

    # scrape wikipedia for entities
    scraper = WikipediaScraper(language=language)
    results = scraper.scrape(entities, output='dict')

    # merge wikipedia data into df
    df['wikipedia_text'] = df['entity'].map(results)

    # clean df columns
    df = df.drop(columns=["id"],errors='ignore')

    # write to jsonl file
    if output_jsonl_path:
        df.to_json(output_jsonl_path, orient='records', lines=True, force_ascii=False)
    return df
