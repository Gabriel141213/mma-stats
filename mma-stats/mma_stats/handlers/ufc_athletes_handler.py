from pandas import DataFrame
import pandas as pd
from ..utils.time_to_seconds import time_to_seconds
import numpy as np

def ufc_athletes_handler(athletes: DataFrame) -> DataFrame:
    athletes['Average_Fight_Time'] = athletes['Average_Fight_Time'].apply(time_to_seconds).astype(float)
        
    fill_values = {
    "Name": "NO NAME",
    "Nickname": "NO NICKNAME",
    "Wins": 0,
    "Losses": 0,
    "Draws": 0,
    "Weight_Class": "NO WEIGHT CLASS",
    "Significant_Strikes_Landed": 0,
    "Significant_Strikes_Attempted": 0,
    "Takedowns_Landed": 0,
    "Takedowns_Attempted": 0,
    "Age": 0,
    "Height": 0,
    "Weight": 0,
    "UFC_Debut": "NO UFC DEBUT",
    "Reach": 0,
    "Leg_Reach": 0,
    "Significant_Strikes_Landed_Per_Min": 0,
    "Significant_Strikes_Absorbed_Per_Min": 0,
    "Takedowns_Average_Per_15min": 0,
    "Submissions_Average_Per_15min": 0,
    "Significant_Strike_Defense_Percentage": 0,
    "Takedown_Defense": 0,
    "Knockdowns_Average": 0,
    "Average_Fight_Time": 0,
    "Head_Strikes_Percent": 0,
    "Head_Strikes_Count": 0,
    "Body_Strikes_Percent": 0,
    "Body_Strikes_Count": 0,
    "Leg_Strikes_Percent": 0,
    "Leg_Strikes_Count": 0,
    "Win_by_KO/TKO_Count": 0,
    "Win_by_KO/TKO_Percentage": 0,
    "Win_by_DEC_Count": 0,
    "Win_by_DEC_Percentage": 0,
    "Win_by_FIN_Count": 0,
    "Win_by_FIN_Percentage": 0,
    "Fighting_Style": "NO FIGHTING STYLE",
    "Hometown": "NO HOMETOWN",
    }

    athletes = athletes.fillna(value=fill_values)

    mapping_weight_class = {
        "Featherweight": "Featherweight",
        "Lightweight": "Lightweight",
        "Heavyweight": "Heavyweight",
        "Middleweight": "Middleweight",
        "Welterweight": "Welterweight",
        "Peso-galo": "Bantamweight",
        "Light Heavyweight": "Light Heavyweight",
        "Peso-médio": "Middleweight",
        "Peso Meio-Médio": "Welterweight",
        "Flyweight": "Flyweight",
        "Peso-galo feminino": "Bantamweight",
        "Women's Strawweight": "Strawweight",
        "Peso-leve": "Lightweight",
        "Peso-pesado": "Heavyweight",
        "Bantamweight": "Bantamweight",
        "N/A": "N/A",
        "Peso-pena": "Featherweight",
        "Peso meio-pesado": "Light Heavyweight",
        "Peso-mosca": "Flyweight",
        "Peso-mosca feminino": "Flyweight",
        "Women's Bantamweight": "Bantamweight",
        "Peso-palha feminino": "Strawweight",
        "Women's Flyweight": "Flyweight",
        "Women's Featherweight": "Featherweight",
        "Peso-Pena Feminino": "Featherweight",
    }

    athletes['Weight_Class'] = athletes['Weight_Class'].replace(mapping_weight_class)
    athletes['Nickname'] = athletes['Nickname'].replace({"": "NO NICKNAME"})

    int_cols_to_fill = [
        "Wins",
        "Losses",
        "Draws",
        "Significant_Strikes_Landed",
        "Significant_Strikes_Attempted",
        "Takedowns_Landed",
        "Takedowns_Attempted",
        "Age",
        "Head_Strikes_Count",
        "Body_Strikes_Count",
        "Leg_Strikes_Count",
        "Win_by_KO/TKO_Count",
        "Win_by_DEC_Count",
        "Win_by_FIN_Count",
    ]

    float_cols_to_fill = [
        "Height",
        "Weight",
        "Reach",
        "Leg_Reach",
        "Significant_Strikes_Landed_Per_Min",
        "Significant_Strikes_Absorbed_Per_Min",
        "Takedowns_Average_Per_15min",
        "Submissions_Average_Per_15min",
        "Significant_Strike_Defense_Percentage",
        "Takedown_Defense",
        "Knockdowns_Average",
        "Average_Fight_Time",
        "Head_Strikes_Percent",
        "Body_Strikes_Percent",
        "Leg_Strikes_Percent",
        "Win_by_KO/TKO_Percentage",
        "Win_by_DEC_Percentage",
        "Win_by_FIN_Percentage"
    ]
    for column in int_cols_to_fill:
        athletes[column] = athletes[column].replace("N/A", "0")
        athletes[column] = athletes[column].replace("", "0")
        athletes[column] = athletes[column].astype(int)

    for column in float_cols_to_fill:
        athletes[column] = athletes[column].replace("N/A", "0")
        athletes[column] = athletes[column].replace("", "0")
        athletes[column] = athletes[column].astype(float)

    athletes["Significant_Strikes_Ratio"] = athletes["Significant_Strikes_Landed"] / athletes["Significant_Strikes_Attempted"]
    athletes["Takedowns_Ratio"] = athletes["Takedowns_Landed"] / athletes["Takedowns_Attempted"]

    athletes["Significant_Strikes_Ratio"] = athletes["Significant_Strikes_Ratio"].replace(np.inf, 0)
    athletes["Takedowns_Ratio"] = athletes["Takedowns_Ratio"].replace(np.inf, 0)

    athletes["Significant_Strikes_Ratio"] = athletes["Significant_Strikes_Ratio"].replace(np.nan, 0)
    athletes["Takedowns_Ratio"] = athletes["Takedowns_Ratio"].replace(np.nan, 0)

    # Dicionário de mapeamento inicial
    style_mapping = {
        "Jiu-Jitsu": "Grappling",
        "Brazilian Jiu-Jitsu": "Grappling",
        "Wrestling": "Grappling",
        "Wrestler": "Grappling",
        "Judo": "Grappling",
        "Sambo": "Grappling",
        "Grappler": "Grappling",
        "Striker": "Striking",
        "Muay Thai": "Striking",
        "Kickboxer": "Striking",
        "Boxing": "Striking",
        "Boxer": "Striking",
        "Karate": "Striking",
        "Taekwondo": "Striking",
        "Kung Fu": "Striking",
        "Kung-Fu": "Striking",
        "Brawler": "Striking",
        "MMA": "Mixed",
        "Freestyle": "Mixed",
        "N/A": "Mixed"
    }

    # Aplicar o mapeamento inicial
    athletes["Fighting_Category"] = athletes["Fighting_Style"].replace(style_mapping)

    # Função para definir a categoria com base nas estatísticas
    def define_category(row):
        if row["Fighting_Category"] == "Mixed":
            # Calcular proporção de strikes e takedowns
            strike_ratio = row["Significant_Strikes_Ratio"]
            takedown_ratio = row["Takedowns_Ratio"]
            
            # Definir categoria com base na proporção dominante
            if strike_ratio > takedown_ratio:
                return "Striking"
            else:
                return "Grappling"
        else:
            return row["Fighting_Category"]

    # Aplicar a função para definir a categoria final
    athletes["Fighting_Category"] = athletes.apply(define_category, axis=1)

    return athletes