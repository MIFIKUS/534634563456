import re

a = 'PS__3740601912__T12__SCOOP_104-L_$33_NLHE_[Turbo_The_Copacabana]__BI$33__FREEZE__FalseMAX__REG__2024_05_23'


def get_tournament_id(filename: str) -> str:
    return re.search(r'PS__(.*?)__T', filename).group(1)

print(get_tournament_id(a))