import discord
import asyncio
from html import unescape
from urllib.request import urlopen, Request
import json
from calendar import timegm

def joliStr(n):
    if isinstance(n, float) :
        ent, dec = str(n).split(".")
        ent = int(ent)
    elif isinstance(n, str) :
        if "." in n :
            ent, dec = n.split(".")
            ent = int(ent)
        else : ent, dec = int(n), ""
    else : 
        ent = n
        dec = 0

    result = ""
    while ent >= 1000:
        ent, r = divmod(ent, 1000)
        if ent > 0 and r < 100 :
            if r < 10 : result = " 00" + str(r) + result
            else : result = " 0" + str(r) + result
        else : result = " " + str(r) + result

    result = str(ent) + result

    if dec :
        result += "," 
        i = 0
        while i < len(dec):
            try :
                result += dec[i]
                result += dec[i+1]
                result += dec[i+2]
                result += " "
            except IndexError : pass
            i += 3
    return result

def getUrl(url) :
    req = Request(url, headers={'User-Agent': "Je n'suis pas un robot (enfin si mais un gentil ^^) !"})
    result = urlopen(req)
    result = unescape(result.read().decode("utf-8"))
    return json.loads(result)

def p4Affichage(grille):
    reponse = ""
    for i in range(7): reponse += str(i+1)+"\N{COMBINING ENCLOSING KEYCAP}"
    reponse += "\n"
    for line in grille:
        for i in line:
            if i == "J" : reponse += str(discord.utils.get(client.get_all_emojis(), name="p4jaune"))
            elif i == "R" : reponse += str(discord.utils.get(client.get_all_emojis(), name="p4rouge"))
            else : reponse += "\N{MEDIUM BLACK CIRCLE}"
        reponse += "\n"
    return reponse

def p4Winner(grille):
    for y in range(6):
        for x in range(7):
            if y+3 <= 5 and grille[y][x] == grille[y+1][x] == grille[y+2][x] == grille[y+3][x] != "" : return grille[y][x]
            if x+3 <= 6 and grille[y][x] == grille[y][x+1] == grille[y][x+2] == grille[y][x+3] != "" : return grille[y][x]
            if y+3 <= 5 and x+3 <= 6 and grille[y][x] == grille[y+1][x+1] == grille[y+2][x+2] == grille[y+3][x+3] != "" : return grille[y][x]
            if x+3 <= 6 and y-3 >= 0 and grille[y][x] == grille[y-1][x+1] == grille[y-2][x+2] == grille[y-3][x+3] != "" : return grille[y][x]
    return None

def flatten(grille):
    reponse = []
    for line in grille:
        for i in line : reponse.append(i)
    return reponse