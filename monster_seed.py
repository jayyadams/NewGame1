import json

def calculate_stat(base, growth, level, extra_growth_interval=5, extra_growth_factor=1.15):
    stat = base * (1 + growth) ** (level - 1)
    if level % extra_growth_interval == 0:
        stat *= extra_growth_factor
    return round(stat)

