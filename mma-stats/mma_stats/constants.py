from typing import Final

BASE_ATHLETES_URL = "https://www.ufc.com.br/athletes/all"
BASE_PROFILES_URL = "https://www.ufc.com.br/athlete/"
BASE_RECORDS_URL = "https://www.ufc.com.br/athlete/records/"
REQUEST_DELAY: Final = 2  # segundos
MAX_RETRIES: Final = 3

UFC_ATHLETES_COLUMNS = {
    'Athlete_ID': 'String',
    'Name': 'String',
    'Nickname': 'String',
    'Wins': 'String',
    'Losses': 'String',
    'Draws': 'String',
    'Weight_Class': 'String',
    'Significant_Strikes_Landed': 'String',
    'Significant_Strikes_Attempted': 'String',
    'Takedowns_Landed': 'String',
    'Takedowns_Attempted': 'String',
    'Age': 'String',
    'Height': 'String',
    'Weight': 'String',
    'UFC_Debut': 'String',
    'Reach': 'String',
    'Leg_Reach': 'String',
    'Significant_Strikes_Landed_Per_Min': 'String',
    'Significant_Strikes_Absorbed_Per_Min': 'String',
    'Takedowns_Average_Per_15min': 'String',
    'Submissions_Average_Per_15min': 'String',
    'Significant_Strike_Defense_Percentage': 'String',
    'Takedown_Defense': 'String',
    'Knockdowns_Average': 'String',
    'Average_Fight_Time': 'String',
    'Head_Strikes_Percent': 'String',
    'Head_Strikes_Count': 'String',
    'Body_Strikes_Percent': 'String',
    'Body_Strikes_Count': 'String',
    'Leg_Strikes_Percent': 'String',
    'Leg_Strikes_Count': 'String',
    'Win_by_KO/TKO_Count': 'String',
    'Win_by_KO/TKO_Percentage': 'String',
    'Win_by_DEC_Count': 'String',
    'Win_by_DEC_Percentage': 'String',
    'Win_by_FIN_Count': 'String',
    'Win_by_FIN_Percentage': 'String',
    'Fighting_Style': 'String',
    'Hometown': 'String'
}

UFC_ATHLETES_RECORDS_COLUMNS = {
    'Athlete_ID': 'String',
    'Opponent_ID': 'String',
    'Fight_Date': 'String',
    'Last_Round': 'String',
    'End_Time': 'String',
    'Victory_Method': 'String',
    'Fight_Result': 'String'
}

SELECTORS = {
    'name': 'span.c-listing-athlete__name',
    'nickname': 'span.c-listing-athlete__nickname',
    'record': 'span.c-listing-athlete__record',
    'weight_class': 'div.field--name-stats-weight-class .field__item',
    'athlete_link': 'a.e-button--black'
}