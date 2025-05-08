from datetime import datetime
from typing import Dict

WATERING_INTERVALS = {
    "Frequent": 2,        
    "Average": 5,         
    "Minimum": 10
}

SUNLIGHT_THRESHOLD = 1.0  

def calculate_days_since(date: datetime) -> float:
    """Обчислює кількість днів, що минули з вказаної дати до зараз"""
    now = datetime.utcnow()
    delta = now - date
    return delta.total_seconds() / (60 * 60 * 24)  

def get_watering_level(days_ago: float, interval: int) -> int:
    """
    Визначає рівень необхідного поливу від 1 до 5, 
    де 1 - щойно полито, 5 - терміново потребує поливу
    """
    percent = min(days_ago / interval, 1.0)
    
    if percent <= 0.2:
        return 1
    elif percent <= 0.4:
        return 2
    elif percent <= 0.6:
        return 3
    elif percent <= 0.8:
        return 4
    else:
        return 5

def get_sunfilling_level(days_ago: float) -> int:
    """
    Визначає рівень необхідного сонценасичування: 1 або 5,
    де 1 - рослина отримала сонце сьогодні,
    5 - рослина не отримувала сонце більше доби
    """
    return 5 if days_ago > SUNLIGHT_THRESHOLD else 1

def calculate_care_status(last_watering: datetime, last_sunfilling: datetime, 
                         watering_type: str) -> Dict:
    """
    Обчислює статус догляду для рослини на основі останніх дат догляду
    та рекомендованих інтервалів для виду рослини.
    """
    watering_interval = WATERING_INTERVALS.get(watering_type, 7)
    
    watering_days_ago = calculate_days_since(last_watering)
    sunfilling_days_ago = calculate_days_since(last_sunfilling)
    
    watering_level = get_watering_level(watering_days_ago, watering_interval)
    sunfilling_level = get_sunfilling_level(sunfilling_days_ago)
    
    return {
        "watering_level": watering_level,
        "watering_days_ago": round(watering_days_ago, 1),
        "watering_interval": watering_interval,
        
        "sunfilling_level": sunfilling_level,
        "sunfilling_days_ago": round(sunfilling_days_ago, 1),
        "sunfilling_threshold": SUNLIGHT_THRESHOLD
    }