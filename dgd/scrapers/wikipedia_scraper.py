
import wikipediaapi
import json
import pandas as pd
from rich.progress import Progress

class WikipediaScraper:
    def __init__(self, language: str = 'en', user_agent: str = 'data-goose-wikipedia-scraper/1.0'):
        self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=language)

    def scrape(
        self,
        entities: str | list[str],
        output: str = 'dict',
        output_file: str | None = None
    ) -> dict[str, str] | str | pd.DataFrame:
        """
        Scrape Wikipedia pages for given entities.
        Args:
            entities: str or list of str, names of Wikipedia pages to scrape
            output: 'dict', 'json', or 'pandas' (DataFrame)
            output_file: optional file path to save the result
        Returns:
            Data in the requested format
        """
        if isinstance(entities, str):
            entities = [entities]
        result = {}
        max_entity_len = max(len(str(e)) for e in entities) + 2
        with Progress() as progress:
            start_time = progress.get_time()
            task = progress.add_task("Scraping Wikipedia", total=len(entities))
            for entity in entities:
                page = self.wiki.page(entity)
                result[entity] = page.text if page.exists() else ''
                progress.update(task, advance=1, description=f"Scraping: {entity:<{max_entity_len}}")
            end_time = progress.get_time()
            elapsed = end_time - start_time
            progress.console.print(f"\nTotal elapsed time: {elapsed:.2f} seconds")
        
        if output == 'dict':
            data = result
        elif output == 'json':
            data = json.dumps(result, ensure_ascii=False, indent=2)
        elif output == 'pandas':
            data = pd.DataFrame(list(result.items()), columns=['entity', 'text'])
        else:
            raise ValueError("output must be one of: 'dict', 'json', 'pandas'")

        if output_file:
            if output == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(data)
            elif output == 'dict':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            elif output == 'pandas':
                data.to_csv(output_file, index=False)
        return data
