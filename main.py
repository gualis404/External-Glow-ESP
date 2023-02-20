import pymem
import pymem.process
import requests
import re
from colorama import Fore, Back, Style
import os
import pymem
import ctypes
import time

os.system('cls')
os.system('title CSGO ESP By Gualis1337')
os.system('color b')
os.system('mode 100, 30')

def scrapeOffset(value):
    url = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.hpp'
    response = requests.get(url)

    resp = re.findall(r'(\w+)\s*=\s*(\w+)', response.text)

    for i in resp:
        if i[0] == value:
            return i[1]

colors = {
    'red': [1.0, 0.0, 0.0, 0.0],
    'white': [1.0, 1.0, 1.0, 0.0],
    'yellow': [1.0, 1.0, 0.0, 0.0],
    'purple': [1.0, 0.0, 1.0, 0.0],
    'light_blue': [1.0, 1.0, 1.0],
    'orange_brown': [1.0, 0.5, 0.0, 0.0],
    'green': [0.0, 0.0, 1.0, 0.0],
    'blue': [0.0, 0.0, 0.0, 1.0],
    'cyan': [0.0, 0.5, 1.0, 1.0],
    'black': [0.0, 0.0, 0.0, 0.0],
    'purple': [0.0, 1.0, 0.0, 1.0],
    'orange': [0.0, 1.0, 0.5, 0.0],
    'violet': [0.0, 0.5, 0.5, 0.5],
    'blue_green': [0.0, 0.0, 0.5, 0.5],
    'baby_blue': [0.0, 0.0, 0.5, 1.0],
    'lilac': [0.0, 2.0, 0.5, 1.0],
    'dark_grey': [0.0, 0.1, 0.1, 0.1],
    'dark_purple': [0.0, 0.1, 0.0, 0.1],
    'bronze': [0.0, 0.1, 0.1, 0.0],
    'dark_blue': [0.0, 0.0, 0.1, 0.1],
    'forest_green': [0.0, 0.0, 0.1, 0.0],
    'brown': [0.0, 0.1, 0.0, 0.0]
}

def Colors():
    print(Fore.RED + '1. Kırmızı')
    print(Fore.WHITE + '2. Beyaz')
    print(Fore.YELLOW + '3. Sarı')
    print(Fore.MAGENTA + '4. Mor')
    print(Fore.BLUE + '5. Mavi')
    print(Fore.LIGHTRED_EX + '6. Turuncu')
    print(Fore.GREEN + '7. Yeşil')
    print(Fore.LIGHTMAGENTA_EX + '8. Pembe')
    print(Fore.LIGHTCYAN_EX + '9. Turkuaz' + Fore.RESET)
    print("")

Colors()

colorSelect = input('Renk Seçiniz: ')

if colorSelect == '1':
    color = colors['red']
elif colorSelect == '2':
    color = colors['white']
elif colorSelect == '3':
    color = colors['yellow']
elif colorSelect == '4':
    color = colors['purple']
elif colorSelect == '5':
    color = colors['light_blue']
elif colorSelect == '6':
    color = colors['orange_brown']
elif colorSelect == '7':
    color = colors['green']
elif colorSelect == '8':
    color = colors['blue']
elif colorSelect == '9':
    color = colors['cyan']
else:
    print('Hatalı Seçim Yaptınız!')
    exit()

offsets = {
    'dwEntityList': int(scrapeOffset('dwEntityList'), 16),
    'dwGlowObjectManager': int(scrapeOffset('dwGlowObjectManager'), 16),
    'm_iGlowIndex': int(scrapeOffset('m_iGlowIndex'), 16),
    'm_iTeamNum': int(scrapeOffset('m_iTeamNum'), 16),
    'm_bDormant': int(scrapeOffset('m_bDormant'), 16),
    'dwLocalPlayer': int(scrapeOffset('dwLocalPlayer'), 16),
    'm_flFlashMaxAlpha': int(scrapeOffset('m_flFlashMaxAlpha'), 16),
    'dwForceJump': int(scrapeOffset('dwForceJump'), 16),
    'm_fFlags': int(scrapeOffset('m_fFlags'), 16),
    'm_MoveType': int(scrapeOffset('m_MoveType'), 16),
    'dwForceLeft': int(scrapeOffset('dwForceLeft'), 16),
    'dwForceRight': int(scrapeOffset('dwForceRight'), 16),
    'dwClientState_ViewAngles': int(scrapeOffset('dwClientState_ViewAngles'), 16)
}

def glow(pm, client, engine, enginePointer, glowColor):
    glowManager = pm.read_int(client + offsets['dwGlowObjectManager'])
    try:
        for i in range(1, 32):
            entity = pm.read_int(client + offsets['dwEntityList'] + i * 0x10)
            if entity:
                entityTeamID = pm.read_int(entity + offsets['m_iTeamNum'])
                entityGlow = pm.read_int(entity + offsets['m_iGlowIndex'])
                player = pm.read_int(client + offsets['dwLocalPlayer'])
                playerTeam = pm.read_int(player + offsets['m_iTeamNum'])
                if entityTeamID != playerTeam:
                    pm.write_float(glowManager + entityGlow * 0x38 + 0x8, float(glowColor[0]))
                    pm.write_float(glowManager + entityGlow * 0x38 + 0xC , float(glowColor[1]))
                    pm.write_float(glowManager + entityGlow * 0x38 + 0x10, float(glowColor[2]))
                    pm.write_float(glowManager + entityGlow * 0x38 + 0x14, float(glowColor[3]))
                    pm.write_int( glowManager + entityGlow * 0x38 + 0x28, 1 )
    except:
        pass

def main():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    enginePointer = pm.read_int((client + offsets['dwLocalPlayer']))

    print(Fore.MAGENTA + 'Hile Başlatıldı!' + Fore.RESET)

    while True:
        glow(pm, client, engine, enginePointer, color)
        time.sleep(0.01)

if __name__ == '__main__':
    main()
