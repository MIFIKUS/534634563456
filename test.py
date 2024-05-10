from ClientLauncher.Database.get_info_from_archive import get_info
from ClientLauncher.Database.add_info import AddInfo


a = AddInfo()

b = get_info('E:\\poker\\PS__3749900568__The_Fast_6_$33_[6-Max_6_Minute_Levels_Progressive_KO]__BI$33__KO__6MAX__TURBO__2024_05_08.zip')

#b = get_info_for_tables('PS__3749900568__T9__The_Fast_6_$33_[6-Max_6_Minute_Levels_Progressive_KO]__BI$33__KO__6MAX__TURBO__2024_05_08.txt')

a.add_tables_additional_info(b)