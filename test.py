import re
import time
import win32gui

a = 'Bigger €50 | €4,000 Gtd - 600/1,200 ante 150 - Tournament 3769315911 Table 4'


#print(', '.join(re.split(r'^[^ |\|]+', a)[0:-1]))
#print(a.split(', $'))

#print(re.search(r', (€.+?) Gtd', a).group(1))

print(re.search(r'\| (€.+?) Gtd', a).group(1))
time.sleep(5)

a = win32gui.GetForegroundWindow()

print(win32gui.GetWindowText(a))