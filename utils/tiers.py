from . import config


def get_tier_name(tier):
    if tier in config.TIERS:
        return config.TIERS[tier]['name']
    else:
        return 'unknown'


def get_color(tier):
    if tier in config.TIERS:
        return config.TIERS[tier]['color']
    else:
        return (150, 150, 150)
