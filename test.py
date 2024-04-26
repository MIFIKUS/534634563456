import zipfile

path = r'E:\poker\PS__3743747148__BI$55__The_Fast_7_$55_[7-Max_7_Minute_Levels_Progressive_KO]__KO__TURBO__7MAX__2024_04_22.zip'

with zipfile.ZipFile(r'E:\poker\PS__3743747148__BI$55__The_Fast_7_$55_[7-Max_7_Minute_Levels_Progressive_KO]__KO__TURBO__7MAX__2024_04_22.zip', 'a') as zipf:
    print(zipf.namelist())


