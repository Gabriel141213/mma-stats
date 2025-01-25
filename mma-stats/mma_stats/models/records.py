from dataclasses import dataclass

@dataclass
class Record:
    athlete_id: str
    opponent_id: str
    date: str
    round: str
    time: str
    method: str
    result: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Record':
        return cls(
            athlete_id=data['Athlete_ID'],
            opponent_id=data['Opponent_ID'],
            date=data['Fight_Date'],
            round=data['Last_Round'],
            time=data['End_Time'],
            method=data['Victory_Method'],
            result=data['Fight_Result']
        )

    def to_dict(self) -> dict:
        """Converts Record object to a dictionary"""
        return {
            'Athlete_ID': self.athlete_id,
            'Opponent_ID': self.opponent_id,
            'Fight_Date': self.date,
            'Last_Round': self.round,
            'End_Time': self.time,
            'Victory_Method': self.method,
            'Fight_Result': self.result
        }
