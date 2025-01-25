from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import csv

from ..constants import BASE_ATHLETES_URL, SELECTORS
from ..utils.exceptions import RequestException, ParsingException
from ..models.athletes import Athlete
from ..utils.requests_utils import retry_on_failure, make_request

class UFCScraper:
    def __init__(self, base_url: str = BASE_ATHLETES_URL):
        self.base_url = base_url

    @retry_on_failure()
    def scrape_athletes_from_page(self, url: str) -> List[Dict]:
        try:
            response = make_request(url)
            soup = BeautifulSoup(response.text, "html.parser")
            athletes = soup.find_all("div", class_="c-listing-athlete-flipcard__inner")
            
            return [self._process_athlete(athlete) for athlete in athletes]
        except Exception as e:
            raise RequestException(f"Erro ao processar página {url}: {e}")

    def _process_athlete(self, athlete_element: BeautifulSoup) -> Dict:
        try:
            athlete_link = athlete_element.find("a", class_="e-button--black")
            athlete_id = athlete_link.get("href").split("/")[-1]
            athlete_url = f"https://www.ufc.com.br{athlete_link.get('href')}"
            
            name = self._get_text(athlete_element, SELECTORS['name'])
            nickname = self._get_text(athlete_element, SELECTORS['nickname'])
            record = self._get_text(athlete_element, SELECTORS['record'])
            wins, losses, draws = self._parse_record(record)
            weight_class = self._get_text(athlete_element, SELECTORS['weight_class'])
            
            athlete_profile = self.scrape_athlete_profile(athlete_url)
            
            return {
                "Athlete ID": athlete_id,
                "Name": name,
                "Nickname": nickname,
                "Wins": wins,
                "Losses": losses,
                "Draws": draws,
                "Weight Class": weight_class,
                **athlete_profile
            }
        except Exception as e:
            logging.error(f"Erro ao processar atleta: {e}")
            return {}

    @retry_on_failure()
    def scrape_athlete_profile(self, url: str) -> Dict:
        try:
            response = make_request(url)
            soup = BeautifulSoup(response.text, "html.parser")
            return self._extract_profile_data(soup, url)
        except Exception as e:
            raise ParsingException(f"Erro ao processar perfil {url}: {e}")

    def scrape_all_athletes(self) -> List[Athlete]:
        all_athletes = []
        page = 1
        
        print(f"Scraping page {page}...")
        while True:
            logging.info(f"Scraping página {page}...")
            url = f"{self.base_url}?page={page}"
            athletes = self.scrape_athletes_from_page(url)
            
            if not athletes:
                break
            
            all_athletes.extend([Athlete.from_dict(athlete) for athlete in athletes if athlete])
            page += 1
            
        return all_athletes

    @staticmethod
    def _get_text(element: BeautifulSoup, selector: str) -> str:
        found = element.select_one(selector)
        return found.get_text(strip=True) if found else "N/A"

    @staticmethod
    def _parse_record(record: str) -> tuple[str, str, str]:
        if record == "N/A":
            return "N/A", "N/A", "N/A"
        return record.replace(" (V-D-E)", "").split("-")

    def _extract_profile_data(self, soup: BeautifulSoup, url: str) -> Dict:
        try:
            # Informações detalhadas
            stats = {}
            
            overlap_stats = soup.find_all("dl", class_="c-overlap__stats")
            for stat in overlap_stats:
                label = stat.find("dt").text.strip()
                value = stat.find("dd").text.strip()
                
                if label == "Golpes Sig. Conectados":
                    stats["Significant Strikes Landed"] = value
                elif label == "Golpes Sig. Desferidos":
                    stats["Significant Strikes Attempted"] = value
                elif label == "Quedas aplicadas":
                    stats["Takedowns Landed"] = value
                elif label == "Tentativas de queda":
                    stats["Takedowns Attempted"] = value

            bio = soup.find_all("div", class_="c-bio__row--3col")
            if bio:
                # Primeira linha de informações
                try:
                    stats["Age"] = bio[0].find("div", class_="field__item").text.strip() if bio[0].find("div", class_="field__item") else "N/A"
                except:
                    stats["Age"] = "N/A"
                try:
                    stats["Height"] = bio[0].find_all("div", class_="c-bio__text")[1].text.strip() if bio[0].find_all("div", class_="c-bio__text")[1] else "N/A"
                except:
                    stats["Height"] = "N/A"
                try:
                    stats["Weight"] = bio[0].find_all("div", class_="c-bio__text")[2].text.strip() if bio[0].find_all("div", class_="c-bio__text")[2] else "N/A"
                except:
                    stats["Weight"] = "N/A"
                # Segunda linha de informações
                try:
                    stats["UFC_Debut"] = bio[1].find_all("div", class_="c-bio__text")[0].text.strip() if bio[1].find_all("div", class_="c-bio__text")[0] else "N/A"
                except:
                    stats["UFC_Debut"] = "N/A"
                try:
                    stats["Reach"] = bio[1].find_all("div", class_="c-bio__text")[1].text.strip() if bio[1].find_all("div", class_="c-bio__text")[1] else "N/A"
                except:
                    stats["Reach"] = "N/A"
                try:
                    stats["Leg_Reach"] = bio[1].find_all("div", class_="c-bio__text")[2].text.strip() if bio[1].find_all("div", class_="c-bio__text")[2] else "N/A"
                except:
                    stats["Leg_Reach"] = "N/A"       
                        
            defense_stats = soup.find_all("div", class_="c-stat-compare__group")
            if defense_stats:
                # Golpes Significativos
                try:
                    stats["Significant_Strikes_Landed_Per_Min"] = defense_stats[0].find("div", class_="c-stat-compare__number").text.strip() if defense_stats[0].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Significant_Strikes_Landed_Per_Min"] = "N/A"
                try:
                    stats["Significant_Strikes_Absorbed_Per_Min"] = defense_stats[1].find("div", class_="c-stat-compare__number").text.strip() if defense_stats[1].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Significant_Strikes_Absorbed_Per_Min"] = "N/A"

                # Quedas e Finalizações
                try:
                    stats["Takedowns_Average_Per_15min"] = defense_stats[2].find("div", class_="c-stat-compare__number").text.strip() if defense_stats[2].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Takedowns_Average_Per_15min"] = "N/A"
                try:
                    stats["Submissions_Average_Per_15min"] = defense_stats[3].find("div", class_="c-stat-compare__number").text.strip() if defense_stats[3].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Submissions_Average_Per_15min"] = "N/A"

                # Defesas
                try:
                    stats["Significant_Strike_Defense_Percentage"] = defense_stats[4].find("div", class_="c-stat-compare__number").text.strip().replace(" ", "").replace("\n", "").replace("%", "") if defense_stats[4].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Significant_Strike_Defense_Percentage"] = "N/A"
                try:
                    stats["Takedown_Defense"] = defense_stats[5].find("div", class_="c-stat-compare__number").text.strip().replace(" ", "").replace("\n", "").replace("%", "") if defense_stats[5].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Takedown_Defense"] = "N/A"

                # Knockdowns e Tempo
                try:
                    stats["Knockdowns_Average"] = defense_stats[6].find("div", class_="c-stat-compare__number").text.strip() if defense_stats[6].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Knockdowns_Average"] = "N/A"
                try:
                    stats["Average_Fight_Time"] = defense_stats[7].find("div", class_="c-stat-compare__number").text.strip() if defense_stats[7].find("div", class_="c-stat-compare__number") else "N/A"
                except:
                    stats["Average_Fight_Time"] = "N/A"

            significant_strikes_area = soup.find("div", class_="c-stat-body")
            if significant_strikes_area:

                head_percent = significant_strikes_area.find("text", id="e-stat-body_x5F__x5F_head_percent")
                head_value = significant_strikes_area.find("text", id="e-stat-body_x5F__x5F_head_value")
                stats["Head_Strikes_Percent"] = head_percent.text.strip().replace("%", "") if head_percent else "N/A"
                stats["Head_Strikes_Count"] = head_value.text.strip() if head_value else "N/A"

                # Golpes no corpo
                body_percent = significant_strikes_area.find("text", id="e-stat-body_x5F__x5F_body_percent")
                body_value = significant_strikes_area.find("text", id="e-stat-body_x5F__x5F_body_value")
                stats["Body_Strikes_Percent"] = body_percent.text.strip().replace("%", "") if body_percent else "N/A"
                stats["Body_Strikes_Count"] = body_value.text.strip() if body_value else "N/A"

                # Golpes nas pernas
                leg_percent = significant_strikes_area.find("text", id="e-stat-body_x5F__x5F_leg_percent")
                leg_value = significant_strikes_area.find("text", id="e-stat-body_x5F__x5F_leg_value")
                stats["Leg_Strikes_Percent"] = leg_percent.text.strip().replace("%", "") if leg_percent else "N/A"
                stats["Leg_Strikes_Count"] = leg_value.text.strip() if leg_value else "N/A"
            else:
                    stats["Head_Strikes_Percent"] = stats["Head_Strikes_Count"] = "N/A"
                    stats["Body_Strikes_Percent"] = stats["Body_Strikes_Count"] = "N/A"
                    stats["Leg_Strikes_Percent"] = stats["Leg_Strikes_Count"] = "N/A"
            
            # Encontrar a seção de vitórias por método
            win_by_method_section = soup.find_all("div", class_="c-stat-3bar c-stat-3bar--no-chart")
            if win_by_method_section:
                for section in win_by_method_section:
                    title = section.find("h2", class_="c-stat-3bar__title")
                    if title and "Win by Method" in title.text:
                        method_groups = section.find_all("div", class_="c-stat-3bar__group")
                        for method in method_groups:
                            method_label = method.find("div", class_="c-stat-3bar__label").text.strip()
                            if method_label in ['KO/TKO', 'DEC', 'FIN']:
                                value_text = method.find("div", class_="c-stat-3bar__value").text.strip()
                                count, percentage = value_text.replace(" %", "%").split()
                                percentage = percentage.strip('()%')
                                stats[f"Win by {method_label} Count"] = count
                                stats[f"Win by {method_label} Percentage"] = percentage
                        break
            else:
                stats["Win by KO/TKO Count"] = stats["Win by KO/TKO Percentage"] \
                        = stats["Win by DEC Count"] = stats["Win by DEC Percentage"] \
                        = stats["Win by FIN Count"] = stats["Win by FIN Percentage"] = "N/A"

            fighting_style_divs = soup.find_all("div", class_="c-bio__field c-bio__field--border-bottom-small-screens")

            if fighting_style_divs:
                fighting_style = next(
                    (tag.find("div", class_="c-bio__text").text.strip()
                    for tag in fighting_style_divs
                    if tag.find("div", class_="c-bio__label").text.strip() == "Estilo de luta"),
                    "N/A"
                )
                stats['Fighting_Style'] = fighting_style
            else:
                stats['Fighting_Style'] = "N/A"

            location_divs = soup.find_all("div", class_="c-bio__field c-bio__field--border-bottom-small-screens")
            if location_divs:
                location = next(
                    (tag.find("div", class_="c-bio__text").text.strip()
                    for tag in location_divs
                    if tag.find("div", class_="c-bio__label").text.strip() == "Cidade natal"),
                    "N/A"
                )
                stats['Hometown'] = location
            else:
                stats['Hometown'] = "N/A"

            return stats
        except Exception as e:
            print(f"Erro ao processar perfil do atleta: {url}. Erro: {e}")
            return {}

