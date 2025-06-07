
from bs4 import BeautifulSoup
from typing import List, Dict

from ..constants import BASE_PROFILES_URL
from ..utils.exceptions import RequestException, ScrapingException
from ..models.records import Record
from ..utils.requests_utils import retry_on_failure, make_request
import time

class UFCRecordsScraper:
    def __init__(self, base_url: str = BASE_PROFILES_URL):
        self.base_url = base_url

    @retry_on_failure()
    def scrape_athletes_records(self, athlete_id: str) -> List[Record]:
        athlete_url = f"{self.base_url}{athlete_id}"
        page_url = f"{athlete_url}#athlete-record"

        records = []
        while page_url:
        
            print(f"Scraping records for {page_url}")

            try:
                response = make_request(page_url)
                records_soap = BeautifulSoup(response.text, "html.parser")
                try:
                    record = self._process_athlete_records(records_soap, athlete_id)
                except Exception as e:
                    raise ScrapingException(f"Erro ao processar luta: {e} | url: {page_url}")

                records.extend([Record.from_dict(record) for record in record])

                next_page = records_soap.find('a', class_='button', title='Load more items')
                if next_page:
                    page_url = athlete_url + next_page['href']
                    time.sleep(2)  # Delay para evitar sobrecarga no servidor
                else:
                    page_url = None

            except Exception as e:
                raise RequestException(f"Erro ao processar página {athlete_url}: {e}")
        
        return records
    
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

                date_info = fight.find('div', class_='c-card-event--athlete-results__date')
                if date_info:
                    date_info = date_info.text.strip()
                else:
                    date_info = "N/A"

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
                    result = "N/A"
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
                    "Athlete_ID": athlete_id,
                    "Opponent_ID": opponent_id,
                    "Fight_Date": date_info,
                    "Last_Round": round_info,
                    "End_Time": time_info,
                    "Victory_Method": method_info,
                    "Fight_Result": result
                })
            except Exception as e:
                print(f"Erro ao processar luta: {e}")

        return fight_history
    
    def scrape_all_athletes_records(self, athlete_ids: List[str]) -> List[Dict]:
        all_athletes_records = []
        for athlete_id in athlete_ids:
            print(f"Scraping records for {athlete_id}...")
            athlete_record = self.scrape_athletes_records(athlete_id)
            all_athletes_records.extend(fight for fight in athlete_record)
        return all_athletes_records

if __name__ == "__main__":
    scraper = UFCRecordsScraper()
    list_ = scraper.scrape_all_athletes_records(["islam-makhachev"])
    list_.to_dict()['Athlete_ID']