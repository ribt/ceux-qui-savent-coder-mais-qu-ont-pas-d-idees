import discord
import asyncio
from html import unescape
from urllib.request import urlopen, Request
import json
from calendar import timegm

def joliStr(n, signed=False):
    if type(n) == int :
        ent, dec = n, None

    elif type(n) == float :
        ent, dec = int(n), str(n).split(".")[1]
        
    if type(n) == str:
        t = n.split(".")
        ent = int(t[0])
        if len(t) == 2 and int(t[1]) > 0 : dec = t[1]
        else : dec = None


    result = ""
    while ent > 0:
        result = "{:03d}".format(ent%1000) + " " + result
        ent //= 1000

    result = result.lstrip("0")
    if result == "" : result = "0 "

    if signed and n > 0:
        result = "+" + result

    if dec :
        result = result[:-1]+"," 
        for i in range(0, len(dec), 3):
            result += dec[i:i+3] +" "

    return result[:-1]

def getUrl(url, headers={"Accept":"application/json", "Accept-Language":"fr", "User-Agent": "Je n'suis pas un robot (enfin si mais un gentil ^^) !"}) :
    req = Request(url, headers=headers)
    result = urlopen(req)
    result = unescape(result.read().decode("utf-8"))
    return json.loads(result)

def p4Affichage(client, grille):
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
