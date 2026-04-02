import pandas as pd
import numpy as np

class FreshnessPredictor:
    @staticmethod
    def predict(data):
        """
        Calculates Freshness Score based on Time, Temp, and Storage.
        No .json or .pkl files required! Works instantly.
        """
        # 1. Start with a perfect score
        score = 100.0
        
        # --- INPUTS ---
        # Get values safely, defaulting to 0 if missing
        hours_cooked = float(data.get('time_since_cooking_hours', 0) or 0)
        hours_stored = float(data.get('storage_time_hours', 0) or 0)
        temp = float(data.get('temperature', 25)) # Default 25°C
        condition = data.get('storage_condition', 'room_temperature')
        food_type = data.get('food_type', 'Vegetarian')

        # --- SMART LOGIC RULES ---

        # Rule 1: Time Decay (Food spoils over time)
        # Lose 5 points for every hour it sits out
        total_hours = hours_cooked + hours_stored
        score -= (total_hours * 5)

        # Rule 2: Temperature Penalty (Heat kills food) 🌡️
        if temp > 35:
            score -= 25  # Extreme heat penalty
        elif temp > 30:
            score -= 15  # Hot day penalty
        elif temp < 10:
            score += 5   # Bonus for cold weather (natural fridge)

        # Rule 3: Storage Condition
        if condition == 'outside' or condition == 'room_temperature':
            # Room temp degrades faster
            score -= 10 
        elif condition == 'refrigerated':
            # Fridge preserves freshness (Bonus!)
            score += 15 
        elif condition == 'heated':
            # Keeping it hot is good for short term, bad for long term
            if total_hours > 4:
                score -= 20

        # Rule 4: Food Type Sensitivity
        if food_type == 'Non-Veg':
            score -= 15 # Meat spoils faster than veg
        elif food_type == 'Vegan':
            score += 5  # Veggies last longer

        # --- FINAL CALCULATIONS ---
        
        # Ensure score stays between 0 and 100
        score = max(0, min(100, score))
        
        # Determine Label
        if score >= 75:
            label = "Fresh 🟢"
        elif score >= 40:
            label = "Moderate 🟡"
        else:
            label = "Spoiled 🔴"

        return {
            "freshness_score": int(score), # Return as integer (e.g., 85)
            "freshness_label": label
        }