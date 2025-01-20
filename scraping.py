import requests
from bs4 import BeautifulSoup
import csv
import time

# URL principal para os atletas
BASE_URL = "https://www.ufc.com.br/athletes/all"

# Função para extrair os dados de cada atleta
def scrape_athletes_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Encontrando todos os atletas na página
    athletes = soup.find_all("div", class_="c-listing-athlete-flipcard__inner")
    
    all_athletes = []
    
    for athlete in athletes:
        try:
            athlete_id = athlete.find("a", class_="e-button--black")
            athlete_id = athlete_id.get("href")
            athlete_url = f"https://www.ufc.com.br{athlete_id}"
            athlete_id = athlete_id.split("/")[-1]
            
            # Nome do atleta
            name = athlete.find("span", class_="c-listing-athlete__name")
            name = name.get_text(strip=True) if name else "N/A"
            
            # Apelido do atleta
            nickname = athlete.find("span", class_="c-listing-athlete__nickname")
            nickname = nickname.get_text(strip=True) if nickname else "N/A"
            
            # Record (Vitórias, Derrotas e Empates)
            record = athlete.find("span", class_="c-listing-athlete__record")
            record = record.get_text(strip=True) if record else "N/A"
            
            # Separando vitórias, derrotas e empates
            wins, losses, draws = record.replace(" (V-D-E)", "").split("-") if record != "N/A" else ("N/A", "N/A", "N/A")
            
            # Categoria de peso
            weight_class = athlete.find("div", class_="field--name-stats-weight-class")
            try:
                weight_class = weight_class.find("div", class_="field__item")
                weight_class = weight_class.get_text(strip=True) if weight_class else "N/A"
            except:
                weight_class = "N/A"
            
            # Dados adicionais do perfil
            athlete_profile = scrape_athlete_profile(athlete_url)
            
            # Organizando os dados do atleta
            athlete_data = {
                "Athlete ID": athlete_id,
                "Name": name,
                "Nickname": nickname,
                "Wins": wins,
                "Losses": losses,
                "Draws": draws,
                "Weight Class": weight_class,
                **athlete_profile
            }
            
            all_athletes.append(athlete_data)
        except Exception as e:
            print(f"Erro ao processar atleta {athlete}: {e}")
            continue
    
    return all_athletes

# Função para extrair informações detalhadas do perfil do atleta
def scrape_athlete_profile(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        # Informações detalhadas
        stats = {}
        
        # Número de vitórias
        stats_section = soup.find("div", class_="hero-profile__stats")
        stats["KO Wins"] = stats_section.find("p", text="Vitórias por nocaute").find_previous("p").text.strip() if stats_section else "N/A"
        stats["Submission Wins"] = stats_section.find("p", text="Vitórias por finalização").find_previous("p").text.strip() if stats_section else "N/A"
        stats["First Round Wins"] = stats_section.find("p", text="Vitórias no 1º round").find_previous("p").text.strip() if stats_section else "N/A"
        
        # Golpes conectados/desferidos
        overlap_stats = soup.find_all("dl", class_="c-overlap__stats")
        stats["Significant Strikes Landed"] = overlap_stats[0].find("dd").text.strip() if len(overlap_stats) > 0 else "N/A"
        stats["Significant Strikes Attempted"] = overlap_stats[1].find("dd").text.strip() if len(overlap_stats) > 1 else "N/A"
        
        # Informações adicionais como idade, altura, etc.
        bio = soup.find_all("div", class_="c-bio__row--3col")
        if bio:
            stats["Age"] = bio[0].find("div", class_="field--name-age").text.strip() if bio[0] else "N/A"
            stats["Height"] = bio[0].find("div", class_="c-bio__text").text.strip() if bio[0] else "N/A"
            stats["Weight"] = bio[0].find_all("div", class_="c-bio__text")[1].text.strip() if len(bio[0].find_all("div", class_="c-bio__text")) > 1 else "N/A"
            stats["Reach"] = bio[1].find("div", class_="c-bio__text").text.strip() if len(bio) > 1 else "N/A"
        return stats
    except Exception as e:
        print(f"Erro ao processar perfil do atleta: {url}. Erro: {e}")
        return {}

# Função para percorrer as páginas e coletar todos os atletas
def scrape_all_athletes(base_url):
    all_athletes = []
    page = 1
    
    while True:
        print(f"Scraping page {page}...")
        url = f"{base_url}?page={page}"
        athletes = scrape_athletes_from_page(url)
        
        if not athletes:
            break
        
        all_athletes.extend(athletes)
        page += 1
        
        # Pausar entre requisições para evitar sobrecarga no servidor
        time.sleep(2)  # Atraso de 2 segundos entre requisições
        
    return all_athletes

# Função para salvar os dados em um arquivo CSV
def save_to_csv(data, filename="ufc_athletes.csv"):
    if data:
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    else:
        print("Nenhum dado para salvar.")

# Main
if __name__ == "__main__":
    print("Iniciando o scraping...")
    all_athletes = scrape_all_athletes(BASE_URL)
    print(f"Total de atletas extraídos: {len(all_athletes)}")
    save_to_csv(all_athletes)
    print("Dados salvos em 'ufc_athletes.csv'.")
