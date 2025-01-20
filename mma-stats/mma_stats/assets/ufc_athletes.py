from . import constants
import time
from ..functions.scraping_functions.ufc_athletes import (
    scrape_athletes_from_page,
    save_to_csv
)
from dagster import asset

BASE_URL = constants.BASE_ATHLETES_URL

@asset
# Função para percorrer as páginas e coletar todos os atletas
def ufc_athletes_data() -> None:
    all_athletes = []
    page = 1
    
    while True:
        print(f"Scraping page {page}...")
        url = f"{BASE_URL}?page={page}"
        athletes = scrape_athletes_from_page(url)
        
        if not athletes:
            break
        
        all_athletes.extend(athletes)
        page += 1
        
        # Pausar entre requisições para evitar sobrecarga no servidor
        time.sleep(2)  # Atraso de 2 segundos entre requisições
        
        save_to_csv(all_athletes)