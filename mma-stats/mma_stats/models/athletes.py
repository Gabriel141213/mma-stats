from dataclasses import dataclass
from typing import Optional

@dataclass
class AthleteStats:
    # Basic Stats
    significant_strikes_landed: str
    significant_strikes_attempted: str
    takedowns_landed: str
    takedowns_attempted: str
    
    # Bio Info
    age: str
    height: str
    weight: str
    ufc_debut: str
    reach: str
    leg_reach: str
    
    # Performance Stats
    significant_strikes_landed_per_min: str
    significant_strikes_absorbed_per_min: str
    takedowns_average_per_15min: str
    submissions_average_per_15min: str
    significant_strike_defense_percentage: str
    takedown_defense: str
    knockdowns_average: str
    average_fight_time: str
    
    # Strike Distribution
    head_strikes_percent: str
    head_strikes_count: str
    body_strikes_percent: str
    body_strikes_count: str
    leg_strikes_percent: str
    leg_strikes_count: str
    
    # Win Methods
    win_by_ko_tko_count: str
    win_by_ko_tko_percentage: str
    win_by_dec_count: str
    win_by_dec_percentage: str
    win_by_fin_count: str
    win_by_fin_percentage: str
    
    # Additional Info
    fighting_style: str
    hometown: str

@dataclass
class Athlete:
    athlete_id: str
    name: str
    nickname: Optional[str]
    wins: int
    losses: int
    draws: int
    weight_class: str
    stats: AthleteStats

    @classmethod
    def from_dict(cls, data: dict) -> 'Athlete':
        stats = AthleteStats(
            # Basic Stats
            significant_strikes_landed=data.get('Significant Strikes Landed', 'N/A'),
            significant_strikes_attempted=data.get('Significant Strikes Attempted', 'N/A'),
            takedowns_landed=data.get('Takedowns Landed', 'N/A'),
            takedowns_attempted=data.get('Takedowns Attempted', 'N/A'),
            
            # Bio Info
            age=data.get('Age', 'N/A'),
            height=data.get('Height', 'N/A'),
            weight=data.get('Weight', 'N/A'),
            ufc_debut=data.get('UFC_Debut', 'N/A'),
            reach=data.get('Reach', 'N/A'),
            leg_reach=data.get('Leg_Reach', 'N/A'),
            
            # Performance Stats
            significant_strikes_landed_per_min=data.get('Significant_Strikes_Landed_Per_Min', 'N/A'),
            significant_strikes_absorbed_per_min=data.get('Significant_Strikes_Absorbed_Per_Min', 'N/A'),
            takedowns_average_per_15min=data.get('Takedowns_Average_Per_15min', 'N/A'),
            submissions_average_per_15min=data.get('Submissions_Average_Per_15min', 'N/A'),
            significant_strike_defense_percentage=data.get('Significant_Strike_Defense_Percentage', 'N/A'),
            takedown_defense=data.get('Takedown_Defense', 'N/A'),
            knockdowns_average=data.get('Knockdowns_Average', 'N/A'),
            average_fight_time=data.get('Average_Fight_Time', 'N/A'),
            
            # Strike Distribution
            head_strikes_percent=data.get('Head_Strikes_Percent', 'N/A'),
            head_strikes_count=data.get('Head_Strikes_Count', 'N/A'),
            body_strikes_percent=data.get('Body_Strikes_Percent', 'N/A'),
            body_strikes_count=data.get('Body_Strikes_Count', 'N/A'),
            leg_strikes_percent=data.get('Leg_Strikes_Percent', 'N/A'),
            leg_strikes_count=data.get('Leg_Strikes_Count', 'N/A'),
            
            # Win Methods
            win_by_ko_tko_count=data.get('Win by KO/TKO Count', 'N/A'),
            win_by_ko_tko_percentage=data.get('Win by KO/TKO Percentage', 'N/A'),
            win_by_dec_count=data.get('Win by DEC Count', 'N/A'),
            win_by_dec_percentage=data.get('Win by DEC Percentage', 'N/A'),
            win_by_fin_count=data.get('Win by FIN Count', 'N/A'),
            win_by_fin_percentage=data.get('Win by FIN Percentage', 'N/A'),
            
            # Additional Info
            fighting_style=data.get('Fighting_Style', 'N/A'),
            hometown=data.get('Hometown', 'N/A')
        )

        return cls(
            athlete_id=data['Athlete ID'],
            name=data['Name'],
            nickname=data['Nickname'],
            wins=int(data['Wins']) if data['Wins'] != 'N/A' else 0,
            losses=int(data['Losses']) if data['Losses'] != 'N/A' else 0,
            draws=int(data['Draws']) if data['Draws'] != 'N/A' else 0,
            weight_class=data['Weight Class'],
            stats=stats
        )

    def to_dict(self) -> dict:
        """Converte o objeto Athlete para um dicionário"""
        return {
            'Athlete_ID': self.athlete_id,
            'Name': self.name,
            'Nickname': self.nickname,
            'Wins': str(self.wins),
            'Losses': str(self.losses),
            'Draws': str(self.draws),
            'Weight_Class': self.weight_class,
            'Significant_Strikes_Landed': self.stats.significant_strikes_landed,
            'Significant_Strikes_Attempted': self.stats.significant_strikes_attempted,
            'Takedowns_Landed': self.stats.takedowns_landed,
            'Takedowns_Attempted': self.stats.takedowns_attempted,
            'Age': self.stats.age,
            'Height': self.stats.height,
            'Weight': self.stats.weight,
            'UFC_Debut': self.stats.ufc_debut,
            'Reach': self.stats.reach,
            'Leg_Reach': self.stats.leg_reach,
            'Significant_Strikes_Landed_Per_Min': self.stats.significant_strikes_landed_per_min,
            'Significant_Strikes_Absorbed_Per_Min': self.stats.significant_strikes_absorbed_per_min,
            'Takedowns_Average_Per_15min': self.stats.takedowns_average_per_15min,
            'Submissions_Average_Per_15min': self.stats.submissions_average_per_15min,
            'Significant_Strike_Defense_Percentage': self.stats.significant_strike_defense_percentage,
            'Takedown_Defense': self.stats.takedown_defense,
            'Knockdowns_Average': self.stats.knockdowns_average,
            'Average_Fight_Time': self.stats.average_fight_time,
            'Head_Strikes_Percent': self.stats.head_strikes_percent,
            'Head_Strikes_Count': self.stats.head_strikes_count,
            'Body_Strikes_Percent': self.stats.body_strikes_percent,
            'Body_Strikes_Count': self.stats.body_strikes_count,
            'Leg_Strikes_Percent': self.stats.leg_strikes_percent,
            'Leg_Strikes_Count': self.stats.leg_strikes_count,
            'Win_by_KO/TKO_Count': self.stats.win_by_ko_tko_count,
            'Win_by_KO/TKO_Percentage': self.stats.win_by_ko_tko_percentage,
            'Win_by_DEC_Count': self.stats.win_by_dec_count,
            'Win_by_DEC_Percentage': self.stats.win_by_dec_percentage,
            'Win_by_FIN_Count': self.stats.win_by_fin_count,
            'Win_by_FIN_Percentage': self.stats.win_by_fin_percentage,
            'Fighting_Style': self.stats.fighting_style,
            'Hometown': self.stats.hometown
        }