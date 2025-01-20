import requests
from bs4 import BeautifulSoup
import csv
import time

# URL principal para os atletas

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

def scrape_athlete_profile(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
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
            stats['fighting_style'] = fighting_style
        else:
            stats['fighting_style'] = "N/A"

        location_divs = soup.find_all("div", class_="c-bio__field c-bio__field--border-bottom-small-screens")
        if location_divs:
            location = next(
                (tag.find("div", class_="c-bio__text").text.strip()
                for tag in location_divs
                if tag.find("div", class_="c-bio__label").text.strip() == "Cidade natal"),
                "N/A"
            )
            stats['hometown'] = location
        else:
            stats['hometown'] = "N/A"

        return stats
    except Exception as e:
        print(f"Erro ao processar perfil do atleta: {url}. Erro: {e}")
        return {}


# Função para salvar os dados em um arquivo CSV
def save_to_csv(data, filename="/home/gassuncao/mma-status/mma-stats/data/raw/ufc_athletes.csv"):
    if data:
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    else:
        print("Nenhum dado para salvar.")

