from pandas import DataFrame
from ..utils.time_to_seconds import time_to_seconds

def ufc_athletes_record_handler(fights: DataFrame) -> DataFrame:
    fights["End_Time"] = fights["End_Time"].apply(time_to_seconds)

    victory_method_mapping = {
        # Categoria: KO/TKO
        'KO/TKO': 'KO/TKO',
        'TKO': 'KO/TKO',
        'ko/tko': 'KO/TKO',
        'KO': 'KO/TKO',
        "TKO - Doctor's Stoppage": 'KO/TKO',
        'TKO - Doctor Stoppage': 'KO/TKO',
        'FIN': 'KO/TKO',
        'Fin': 'KO/TKO',

        # Categoria: Submission
        'Submissão': 'Submission',
        'sub': 'Submission',
        'submission': 'Submission',

        # Categoria: Unanimous Decision
        'Decision - Unanimous': 'Unanimous Decision',
        'DECISION - UNANIMOUS': 'Unanimous Decision',
        'DECISION-UNANIMOUS': 'Unanimous Decision',
        'Unanimous Decision': 'Unanimous Decision',
        'Decision- Unanimous': 'Unanimous Decision',
        'UD': 'Unanimous Decision',
        'DEC': 'Unanimous Decision',
        'Dec': 'Unanimous Decision',
        'DEc': 'Unanimous Decision',

        # Categoria: Split Decision
        'Decision - Split': 'Split Decision',
        'Split Decision': 'Split Decision',

        # Categoria: Majority Decision
        'Decision - Majority': 'Majority Decision',
        'DECISION - MAJORITY': 'Majority Decision',
        'Majority Decision': 'Majority Decision',

        # Categoria: Draw
        'DRAW': 'Draw',
        'Draw': 'Draw',

        # Categoria: No Contest
        'No Contest': 'No Contest',
        'Could Not Continue': 'No Contest',
        'Overturned': 'No Contest',

        # Categoria: Disqualification
        'DQ': 'Disqualification',

        # Categoria: Outros
        'TBD': 'Outros',
        '2': 'Outros',
        'Outros': 'Outros',
        'N/A': 'Outros',
    }

    fights["Victory_Method"] = fights["Victory_Method"].replace(victory_method_mapping)
    fights["Last_Round"] = fights["Last_Round"].replace({"N/A": "0"}).astype(int)

    fights["Fight_Time"] = fights["End_Time"] + (fights["Last_Round"] - 1) * 360
    
    fights["Athlete_ID"] = fights["Athlete_ID"].astype(str)
    fights["Opponent_ID"] = fights["Opponent_ID"].astype(str)
    fights["Fight_Date"] = fights["Fight_Date"].astype(str)
    fights["Fight_Time"] = fights["Fight_Time"].astype(int)
    fights["Last_Round"] = fights["Last_Round"].astype(int)
    fights["End_Time"] = fights["End_Time"].astype(int)
    fights["Victory_Method"] = fights["Victory_Method"].astype(str)
    fights["Fight_Result"] = fights["Fight_Result"].astype(str)
    
    return fights