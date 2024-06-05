a = """NEO13	
Ninja99	
Trivian	
sley	
itoni	
ok4rin	
Nahlobu4u	
Biofire	
ALABA	
Bulochka	
Сиська1	
Сиська2	
ChosSorc	
Мати	S1imShady
Batasay	Cuke
Свиныч	
Писюнчик	
ZEMLYA	
orionus	
галченок	
F3	
НюхачПісьок	
BigDigOwner 	
ДядяВолодя	
BelPeol	
Porsche	
Harrier	
АнальныйКлещ	
Daaabu	
ИгрокЧленом	
Рокфордыч	
ФиолЧлен	
Фермер	
Hollabolla	holz
ВеселыйФармер	
АлхимкаЧленом	Ликвидус
r3make	
Членыч	
RachelRoxxx	
ShadowBlade	
Some	
К0ЗАК	
Никитаа	
zBrz	
DeadlyBlow	
guard26	
Legalaiz	
Киря	
boms	
Ифрит	
HugoBoss	
ИграюЧленом	
Iskanderchik	
оПЛЯ	
Yola	
Укимаги	
mayba	
Fa1conWay	
TomiKai	
Icasperl	
jeens	
rale	tirel
Членистор	
troublemakerme	
krambambulya	
Rozvell	
Анальный Ювелир 	"""


b = a.split('\n')
LIST = ""
num = 2
print('{')
for i in b:
    for j in i.split('	'):
        if len(j) < 2:
            continue
        print(f'"{j}": "G{num}",')
    num += 1
print('}')