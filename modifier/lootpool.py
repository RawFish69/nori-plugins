"""
Script Name: Nori-Lootpool 
Github: https://github.com/RawFish69/Nori/blob/main/modifier/lootpool.py
Description: Lootpool json and log generation for Nori-bot
Last update: 10/28/2023
"""
import json
import time
from datetime import datetime
import math

# Constants
seconds_per_week = 604800
first_week_timestamp = 1690567200  # First week recorded
current_datetime = datetime.now().strftime("%Y-%m-%d")


# Weekly lootpool
mythics = {
    "SE": ["Archangel","Boreal","Olympic","Toxoplasmosis","Thrundacrack","Corkian Insulator"],
    "Corkus": ["Nirvana","Quetzalcoatl","Pure","Gaia","Warp","Corkian Insulator","Corkian Simulator"],
    "Sky": ["Archangel","Cataclysm","Monster","Oblivion","Warp","Corkian Insulator","Corkian Simulator"],
    "Molten": ["Lament","Archangel","Hero","Singularity","Idol","Divzer","Corkian Simulator"]
}

shiny = {
    "SE": {"Item": "Immolation", "Tracker": "Players Killed"},
    "Corkus": {"Item": "Galleon", "Tracker": "Deaths"},
    "Sky": {"Item": "Monster", "Tracker": "Raids Won"},
    "Molten": {"Item": "Olympic", "Tracker": "Lootruns Completed "}
}


def estimate_week_number():
    current_time = int(time.time())
    elapsed_time = current_time - first_week_timestamp
    elapsed_weeks = elapsed_time / seconds_per_week
    week_number = math.floor(elapsed_weeks) + 1
    return week_number


def create_weekly_lootpool():
    week = estimate_week_number()
    starting_time = (week - 1) * seconds_per_week + first_week_timestamp
    lootpool = {
        "Loot": {
            region: {
                "Shiny": shiny[region],
                "Mythic": mythics[region],
                "Fabled": [],
                "Legendary": [],
                "Rare": [],
                "Unique": []
            }
            for region in ["SE", "Corkus", "Sky", "Molten"]
        },
        "Timestamp": starting_time
    }
    return lootpool


def update_lootpool(weekly_lootpool):
    with open("data/weekly_lootpool.json", "w") as file:
        json.dump(weekly_lootpool, file, indent=3)
    print(json.dumps(weekly_lootpool, indent=3))
    print(f"\nFile updated\nTimestamp: {weekly_lootpool['Timestamp']}")


def history_log(weekly_lootpool, update: bool):
    if update is True:
        log_data = f"Week of {current_datetime}:\n"
        for region, pool in weekly_lootpool["Loot"].items():
            log_data += f"{region}:\nShiny {pool['Shiny']['Item']}\n{pool['Shiny']['Tracker']} Tracker\n"
            for mythic in pool["Mythic"]:
                log_data += f"- {mythic}\n"
        log_data += "\n"
        with open("changelogs/lootpool_history.log", "a") as file:
            file.write(log_data)
        print(log_data)
        return log_data


def main():
    with open("changelogs/lootpool_history.log", "r") as log:
        if current_datetime in log.read():
            check = False
        else:
            check = True
    weekly_lootpool = create_weekly_lootpool()
    update_lootpool(weekly_lootpool)
    history_log(weekly_lootpool, update=check)


main()
