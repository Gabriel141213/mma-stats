import pandas as pd

def time_to_seconds(time_str):
    # Remove espaços em branco e divide a string em partes
    
    def convert_to_int(part):
        try:
            return int(part)
        except ValueError:
            return 0
        
    if pd.isna(time_str) or time_str == '':
        return 0
    
    parts = time_str.strip().split(':')
    
    # Converte cada parte para inteiro
    if len(parts) == 3:  # Formato HH:MM:SS
        hours = convert_to_int(parts[0])
        minutes = convert_to_int(parts[1])
        seconds = convert_to_int(parts[2])
    elif len(parts) == 2:  # Formato MM:SS
        hours = 0
        minutes = convert_to_int(parts[0])
        seconds = convert_to_int(parts[1])
    else:  # Caso inválido
        return 0  # Ou outro valor padrão
    
    # Calcula o total de segundos
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds