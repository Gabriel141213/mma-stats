from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import csv

from constants import BASE_RECORDS_URL, BASE_PROFILES_URL
from utils.exceptions import RequestException, ParsingException
from models.athletes import Athlete
from utils.requests_utils import retry_on_failure, make_request
import time

class UFCRecordsScraper:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    @retry_on_failure()
    def scrape_athletes_records(self, url: str) -> List[Dict]:
        try:
            response = make_request(url)
            records_soap = BeautifulSoup(response.text, "html.parser")
            next_page = records_soap.find('a', class_='button', title='Load more items')
            if next_page:
                page_url = url + next_page['href']
                time.sleep(2)
            else:
                page_url = None
            return [self._process_athlete_records(__) for record in records_soap]
        except Exception as e:
            raise RequestException(f"Erro ao processar página {url}: {e}")
    
    def _process_athlete_records(self, athlete_soap: BeautifulSoup, athlete_id: str) -> Dict:
        
        fight_history = []
        record_element = athlete_soap.find_all('article', class_='c-card-event--athlete-results')
        
        # Itera sobre cada luta encontrada
        for fight in record_element:
            try:
                opponent_id = next(id for id in [item["href"].split('/')[-1] for item in fight.find('div', class_='c-card-event--athlete-results__info').find_all('a')] if id != athlete_id)               
                round_info = fight.find('div', string='Round')
                if round_info:
                    round_info = round_info.find_next('div').text.strip()
                else:
                    round_info = "N/A"
    
                time_info = fight.find('div', string='Tempo')
                if time_info:
                    time_info = time_info.find_next('div').text.strip()
                else:
                    time_info = "N/A"

                method_info = fight.find('div', string='Método')
                if method_info:
                    method_info = method_info.find_next('div').text.strip()
                else:
                    method_info = "N/A"

                link_element = fight.find('div', class_='c-card-event--athlete-results__image c-card-event--athlete-results__red-image win')
              
                if not link_element:
                    link_element = fight.find('div', class_='c-card-event--athlete-results__image c-card-event--athlete-results__blue-image win')
         
                if not link_element:
                    victory_athlete_id = "N/A"
                else:
                    href = link_element.find('a', href=True)['href']
                    victory_athlete_id = href.split('/')[-1]
                    if victory_athlete_id == athlete_id:
                        result = "Victory"
                    if victory_athlete_id != athlete_id:
                        result = "Loss"
                    if victory_athlete_id == "N/A":
                        result = "N/A"
                fight_history.append({
                    "opponent_id": opponent_id,
                    "round": round_info,
                    "time": time_info,
                    "method": method_info,
                    "result": result
                })
            except Exception as e:
                print(f"Erro ao processar luta: {e}")

        return fight_history

    def scrape_all_athletes_records(self, athete_ids: List) -> List[Dict]:
        all_athletes_records = []
        for athlete_id in athete_ids:
            url = self.base_url + athlete_id
            athete_record = self.scrape_athletes_records(url)
            all_athletes_records.append(athete_record)
        return all_athletes_records
    

if __name__ == "__main__":
    scraper = UFCRecordsScraper()
    list_ = scraper.scrape_all_athletes_records(["michael-bisping", "jon-jones", "ilia-topuria", "alexander-volkanovski"])
    print(list_)