import discord
import asyncio
import time
from calendar import timegm
from datetime import date
import random
from traceback import format_exc
import re
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
import urllib.error
from html import unescape
import json
from os import popen
from glob import glob
import feedparser
import codecs
import speedtest
import unicodedata
from hashlib import sha256
from base64 import *
import qrcode
from unidecode import unidecode
from math import ceil
from PIL import Image
from bs4 import BeautifulSoup
import io
from constantes import fast, aide_fast, caracteres, feeds, pendu, ytCategories
from fonctions import joliStr, getUrl, int_to_bytes

commandes = {"ascii":      ["<texte>",                                       "Je te convertis ton texte (ASCII) en d'autres bases."],
             "avatar":     ["[@quelqu'un]",                                  "Je t'envois ta photo de profil (ou celle de l'utilisateur mentionné) convertie en PNG spécialemnt pour toi !"],
             "base32":     ["<base32>",                                      "Je te convertis ton texte (base32) en d'autres bases."],
             "base64":     ["<base64>",                                      "Je te convertis ton texte (base64) en d'autres bases."],
             "base85":     ["<base85>",                                      "Je te convertis ton texte (base85) en d'autres bases."],
             "bin":        ["<binaire>",                                     "Je te convertis ton nombre (binaire) en d'autres bases."],
             "blague":     ["[add <Votre blague.>]",                         "Je te raconte une blague au hasard parmis celles que je connais ou alors tu m'en apprends une nouvelle (mettre un `|` pour que je fasse une pause au moment de raconter votre blague)."],
             "chr":        ["<c>",                                           "Je te donne le nom et le code Unicode de ce caractère."],
             "citation":   ['[add <"Votre citation.", auteur>]',             "Je te raconte une citation au hasard parmis celles que je connais ou alors tu m'en apprends une nouvelle."],
             "clear":      ["<nombre>",                                      "**uniquement pour les modérateurs**\nJe supprime les <nombre> derniers messages dans le salon où la commande a été effectuée."],
             "crypto":     ["<nom>",                                         "Je te donne des infos sur l'état actuel de la crypto monnaie."],
             "date":       ["",                                              "la date d'aujourd'hui, tout simplement ^^"],
             "dec":        ["<nombre décimal>",                              "Je te convertis ton nombre (décimal) en d'autres bases."],
             "defis":      ["[@quelqu'un]",                                  "Cette commande va de paire avec https://ribt.fr/defis/\nJe te donne le leaderboard ou le détail pour la personne mentionnée."],
             "devine":     ["",                                              "Un super jeu ! (Je choisis un nombre entre 0 et 100 et tu dois le deviner)."],
             "dis":        ["<du blabla>",                                   "Je te lis le texte en vocal."],
             "emoticon":   ["",                                              "Je t'envoies un des 4404 jolis emoticons que je connais."],
             "ext":        ["<extension>",                                   "Je t'envois plein d'infos croustillantes sur une extension de nom de domaine (`.fr`, `.com`...) totalement pompées sur https://www.gandi.net/."],
             "fast":       ["<niveau>",                                      aide_fast],
             "findinpi":   ["<nombre ou texte>",                             "Je cherche ton nombre dans les 1 000 000 000 premières décimales du nombre pi (et si tu m'envoies du texte je le convertis)."],
             "friend":     ["<@user1> <@user2>",                             "Je calcule le pourcentage d'amitié entre les deux personnes."],
             "gif":        ["[<termes à rechercher>]",                       "Je vais te chercher un GIF sur https://giphy.com/ (une recherche vide donne un GIF aléatoire)."],
             "gps":        ["<latitude,longitude>",                          "Je te donne les trois mots what3words et l'adresse postale correspondants aux coordonnées GPS."],
             "haddock":    ["",                                              "Un des nombreux jurons du capitaine Haddock"],
             "help":       ["[<commande>]",                                  "Je te donne la liste des commandes disponibles ou toutes les infos sur une commande."],
             "heure":      ["",                                              "l'heure qu'il est, tout simplement ^^"],
             "hex":        ["<hexadécimal>",                                 "Je te convertis ton nombre (en hexadécimal) en d'autres bases."],
             "invite":     ["",                                              "Je t'envoies le lien pour m'inviter sur ton serveur ainsi qu'une invitation pour rejoindre mon serveur principal."],
             "ljdc":       ["",                                              "Les Joies Du Code, un super GIF piqué sur https://lesjoiesducode.fr/"],
             "lmgtfy":     ["<termes à rechercher>",                         "Let Me Google That For You, je fais une recherche sur Internet pour toi (avec Qwant bien entendu)."],
             "loc":        ["",                                              "Lines Of Code, je te dis combien de lignes comporte actuellement mon programme Python."],
             "love":       ["<@user1> <@user2>",                             "Je calcule le pourcentage d'amour entre les deux personnes."],
             "mute":       ["<@utilisateur> <temps><s|m|h|j> <motif>",       "**uniquement pour les modérateurs**\nPour mute temporairement quelqu'un."],
             "p4":         ["[v2]",                                          "Un super jeu de Puissance4 ! L'argument `v2` sert à jouer à la version moderne où l'on peut éjecter un pion de la dernière ligne au lieu de jouer. Tout le reste est expliqué !"],
             "pi2image":   ["<largeur> <hauteur> [<début>]",                 "Je fabrique une image à partir du nombre pi. `largeur` désigne la largeur de l'image en pixels, `hauteur` pour sa hauteur et `début` représente le rang le la première décimale à utiliser."],
             "ping":       ["",                                              "Je te donne le temps qui s'écoule entre le moment où tu postes ton message et celui où je le reçois."],
             "proverbe":   ["[add <Votre proverbe.>]",                       "Je te donne un proverbe au hasard parmis ceux que je connais ou alors tu m'en apprends un nouveau."],
             "qr":         ["<du blabla>",                                   "Je te fabrique un joli QR code avec ton texte de stocké dessus."],
             "r2d":        ["<nombre en chiffres romains>",                  "Je te convertis gratuitement un nombre en chiffres romains en un nombre en chiffres décimaux."],
             "role":       ["<list|add|remove> [rôle1] [rôle2] [rôle3] ...", "Je liste tous les rôles disponibles ou je t'ajoute/enlève celui/ceux que tu me demandes."],
             "roll":       ["",                                              "Je te fournis un nombre (pseudo-)aléatoire entre 0 et 100."],
             "rot13":      ["<texte>",                                       "Je te chiffre/déchiffre ton message en ROT13."],
             "rug":        ["",                                              "Random User Generator, Je te fournis une identité aléatoire un peu crédible si tu veux te faire des faux papiers."],
             "savoir":     ["",                                              "Je te raconte une petite anecdote piochée sur https://www.savoir-inutile.com/"],
             "speedtest":  ["",                                              "Je me la pète un peu avec ma conexion de taré \N{FACE WITH STUCK-OUT TONGUE AND WINKING EYE}"],
             "table":      ["<un chiffre>",                                  "Je te montre la table de multiplication de ce chiffre."],
             "tts":        ["<du blabla>",                                   "Je t'envois un petit fichier MP3 où je lis ton blabla."],
             "unmute":     ["<@quelqu'un>",                                  "**uniquement pour les modérateurs**\nPour unmute dès maintenant quelqu'un qui est toujours mute."],
             "urban":      ["<an English word>",                             "Je te donne la définition du mot sur Urban Dictionnary (en anglais)."],
             "unicode":    ["<code décimal>",                                "Je renvois le caractère correspondant au code Unicode donné."],
             "user":       ["@mention",                                      "Je te donne quelques infos sur la personne emntionnée."],
             "vps":        ["",                                              "Je te donne quelques infos essentielles sur le VPS qui m'héberge."],
             "w3w":        ["<mot1.mot2.mot3> [langue]",                     "Je te donne les coordonnées GPS et l'adresse postale du lieu à partir des ses trois mots what3words. La langue est le code ISO 639-1 de deux lettres coorespondant. Ce paramètre est facultatif si les mots sont français. Plus d'infos sur https://what3words.com/fr/a-propos/"],
             "weather":    ["<ville> <jours>",                               "Je te prédis la météo de la ville pendant un certain nombre de jours (pas plus de 7 non plus, faut pas déconner non plus)."],
             "whois":      ["<nom de domaine>",                              "Je te donne queqlues infos sur le nom de domaine"],
             "wiki":       ["<termes à rechercher>",                         "Je fais la recherche sur Wikipédia à ta place."],
             "youtube":    ["<nom de la vidéo/chaîne>",                      "Je te montre plein d'infos sur cette vidéo/chaîne."]
             }

alias = {"devine":    ["+ou-"],
         "dis":       ["parle"],
         "findinpi":  ["fip"],
         "help":      ["aide"],
         "lmgtfy":    ["lmqtfy", "qwant"],
         "pi2image":  ["pi2img", "p2i"],
         "urban":     ["ud"],
         "user":      ["profile"],
         "weather":   ["meteo"],
         "youtube":   ["ytb", "yt"]
         }

configInfos = {"prefix":             ["text", "Le préfixe pour utiliser une des mes commandes."],
               "welcomeMP":          ["text", "Le message que j'envois aux nouveaux quand ils rejoignent le serv."],
               "modoRole":           ["role", "Le rôle que doivent avoir ceux qui peuvent utiliser mes commandes de modération."],
               "TuxAdminRole":       ["role", "Le rôle que l'on doit avoir pour utiliser la sacro-sainte commande `config`."],
               "muteRole":           ["role", "Le rôle que je peux mettre aux gens qui sont mute pour les humilier publiquement."],
               "humorPercent":       ["percent", "Mon pourcentage d'humour."],
               "spamChannel":        ["channel", "Le seul salon où sont autorisées les commandes qui risquent de pas mal flood (comme les jeux)."],
               "managedRolesColor":  ["color", "Si configuré, ce paramètre permet à tous les membres d'utiliser la commande `role` pour s'ajouter eux-même les rôles ayant cette couleur."],
               "suggestionsChannel": ["channel", "Le salon où les membres peuvent proposer des améliorations pour le serveur."],
               "welcomeChannel":     ["channel", "Si configuré, je poste un message de bienvenue dans le salon correspondant à chaque nouvel arrivant."],
               "goodbyeChannel":     ["channel", "Si configuré, je poste un message de au revoir dans le salon correspondant à chaque membre qui nous quitte."]
               }

defaultConfig = {"prefix": "!",
                 "welcomeMP": None,
                 "modoRole": None,
                 "TuxAdminRole": None,
                 "muteRole": None,
                 "humorPercent": 10,
                 "spamChannel": None,
                 "managedRolesColor": None,
                 "suggestionsChannel": None,
                 "welcomeChannel": None,
                 "goodbyeChannel": None
                 }

def usage(p, commande, mini=False):
    commandeAff = commande
    if not commande in commandes :
        for test in alias :
            if commande in alias[test]:
                commande = test
    txt = ""
    if not mini : txt = "Usage : "
    txt += "`" + p + commandeAff + " " + commandes[commande][0] + "`"
    if not mini : txt += " (`" + p + "help " + commandeAff + "` pour plus de détails)."
    return txt

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



with open("wordlist/courants.txt", "r") as f : mots = f.read().split("\n")
with open("secret.json", "r") as f : secret = json.loads(f.read())
with open("pokemons-trad.json", "r") as f : pokeTrad = json.loads(f.read())

tmp = logFilename = None 

try :    
    client = discord.Client()
            
    @client.event
    async def on_ready():
        try :
            global logFilename, ribt
            logFilename = time.strftime("log/%Y%m%d", time.localtime())
            with open(logFilename,"a") as f : f.write(time.strftime('\n\n***[%H:%M:%S]', time.localtime()) + ' Connecté en tant que ' + client.user.name + ' (id : ' + client.user.id + ')\n')
            await client.change_presence(game=discord.Game(name='jouer avec vous'))
            ribt = await client.get_user_info("321675705010225162")
            with open("config.json", "r") as f : config = json.loads(f.read())
            for server in client.servers :
                if server.id in config :
                    for param in defaultConfig :
                        if not param in config[server.id] : config[server.id][param] = defaultConfig[param]
                    oldConfig = config[server.id].copy()
                    for param in oldConfig:
                        if not param in defaultConfig : del config[server.id][param]
                else :
                    config[server.id] = defaultConfig
            with open("config.json", "w") as f : f.write(json.dumps(config, indent=4))
            await client.send_message(ribt, 'OK v2.0')
        except:
            txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n', time.localtime()) + format_exc() + "\n\n"
            with open("log/erreurs.txt","a") as f : f.write(txt)

    @client.event
    async def on_server_join(server):
        await client.send_message(ribt, "J'ai été invité sur le serv **"+server.name+"** (de **"+server.owner.name+"**) !")
        with open("config.json", "r") as f : config = json.loads(f.read())
        for server in client.servers :
            if server.id in config :
                for param in defaultConfig :
                    if not param in config[server.id] : config[server.id][param] = defaultConfig[param]
                oldConfig = config[server.id].copy()
                for param in oldConfig:
                    if not param in defaultConfig : del config[server.id][param]
            else :
                config[server.id] = defaultConfig
        with open("config.json", "w") as f : f.write(json.dumps(config, indent=4))


    @client.event
    async def on_member_join(member):
        with open("config.json", "r") as f : config = json.loads(f.read())[member.server.id]
        if config["welcomeMP"] :
            await client.send_message(member, config["welcomeMP"])
        channel = discord.utils.get(member.server.channels, id=config["welcomeChannel"])
        if channel : await client.send_message(channel, "Bienvenue à toi " + member.mention + " \N{WAVING HAND SIGN}")

    @client.event
    async def on_member_remove(member):
        with open("config.json", "r") as f : config = json.loads(f.read())[member.server.id]
        channel = discord.utils.get(member.server.channels, id=config["goodbyeChannel"])
        if channel : await client.send_message(channel, "Au revoir **" + member.name + "** \N{WAVING HAND SIGN}")

    @client.event
    async def on_message(message):
        try:
            if message.author == client.user : return

            if message.content == "!reboot" and message.author == ribt :
                    with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + "Tux va tenter de redemarrer sur demande de ribt\n")
                    cmd = popen("./restart-tux.sh")
                    exit()
            
            if message.server == None : # MP
                if message.content.startswith("!flag") :
                    args = message.content.split(" ")
                    if len(args) != 2: await client.send_message(message.channel, "Usage : `!flag <le_flag_d-un_defi>`.")
                    else : 
                        hashed = sha256(bytes(args[1], "utf-8")).hexdigest()
                        with open("flags.json", "r") as f : flags = json.loads(f.read())
                        if hashed in flags :
                            n = flags[hashed]["defi"]
                            pts = flags[hashed]["points"]
                            userId = message.author.id
                            with open("score.json", "r") as f : score = json.loads(f.read())
                            if not userId in score : score[userId] = {"points": 0, "reussis": []}
                            if n in score[userId]["reussis"] : await client.send_message(message.author, "Tu as déjà réussi ce défi !")
                            else :
                                score[userId]["points"] += pts
                                score[userId]["reussis"].append(n)
                                with open("score.json", "w") as f : f.write(json.dumps(score, indent=4))
                                
                                serv = discord.utils.get(client.servers, id="401667451189985280")
                                role = discord.utils.get(serv.roles, name="défi-"+str(n))
                                member = discord.utils.find(lambda m: m.name == message.author.name, serv.members)
                                await client.add_roles(member, role)

                                await client.send_message(message.author, 'Ceci est bien le flag du défi n°' + str(n) + ", tu gagnes " + str(pts) + " points ! Tu peux désormais accéder au channel solutions pour regarder comment les autres ont fait et pour poster ta solution.")
                                await client.send_message(client.get_channel("451818508389580801"), "**" + message.author.name + "** a réussi le défi n°" + str(n) + " (il gagne " + str(pts) + " points).")
  
                        else : await client.send_message(message.author, 'Mauvais flag, essaie encore \N{WINKING FACE}')
                else : await client.send_message(message.author, 'Je ne répond pas au MP désolé \N{HEAVY BLACK HEART}')
                return

            if message.content == "" : return # nouvel arrivant on envoi de fichier sans commentaire

            global logFilename
            t = timegm(message.timestamp.timetuple())
            msg = message.content
            serv = message.server.id
            logTxt = time.strftime('\n[%H:%M:%S] #', time.localtime(t)) + str(message.channel) + ' ' + str(message.author) + ' : ' + msg
            if logFilename != time.strftime("log/%Y%m%d", time.localtime()): logFilename = time.strftime("log/%Y%m%d", time.localtime())
            with open(logFilename, "a") as f : f.write(logTxt)
        
            with open("config.json", "r") as f : config = json.loads(f.read())[message.server.id]
            p = config["prefix"]
            muteRole = discord.utils.get(message.server.roles, id=config["muteRole"])
            modo = discord.utils.get(message.server.roles, id=config["modoRole"])
            admin = discord.utils.get(message.server.roles, id=config["TuxAdminRole"])
            spamBot = discord.utils.get(message.server.channels, id=config["spamChannel"])
            suggestion = discord.utils.get(message.server.channels, id=config["suggestionsChannel"])
            humour = config["humorPercent"]

            with open("mute.json", "r") as f : mute = json.loads(f.read())
            if serv in mute :
                if message.author.id in mute[serv] :
                    if mute[serv][message.author.id]['expires'] < time.time() :
                        del mute[serv][message.author.id]
                        with open("mute.json", "w") as f : f.write(json.dumps(mute, indent=4))
                        if muteRole in message.author.roles :
                            try : await client.remove_roles(message.author, muteRole)
                            except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de t'enlever le rôle "+muteRole.mention+" \N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT}")
                    else :    
                        try : await client.delete_message(message)
                        except discord.errors.Forbidden : await client.send_message(message.channel, "Si je n'ai pas le droit de supprimer les messages des gens mute ça peut vite devenir chiant \N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT}")
                        try : await client.send_message(message.author, "Il te reste encore " + str(round(mute[serv][message.author.id]['expires'] - time.time())) + " secondes pour réfléchir à ce que tu as fait.")
                        except discord.errors.Forbidden : pass
                        return
            if muteRole in message.author.roles :
                try : await client.remove_roles(message.author, muteRole)
                except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de t'enlever le rôle "+muteRole.mention+" \N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT}")

            if random.randint(0, 99) < humour :
                if re.match(r"(?i)^ah?\W*$", msg) : await client.send_message(message.channel, 'tchoum')
                if re.match(r"(?i)^[kq]u?oi?\W*$", msg) : await client.send_message(message.channel, 'ffeur')
                if re.match(r"(?i)^lol\W*$", msg) : await client.send_message(message.channel, 'ita')
                if re.match(r"(?i)^hein\W*$", msg) : await client.send_message(message.channel, 'deux')
                if re.match(r"(?i)^trois\W*$", msg) : await client.send_message(message.channel, 'soleil')
                if re.match(r"(?i)^oui\W*$", msg) : await client.send_message(message.channel, 'stiti')
                if client.user.mentioned_in(message) : await client.add_reaction(message, u"\N{WAVING HAND SIGN}")

            """
            elif re.match(r"^[0-9+/() *-]+$", msg):
              result = str(eval(msg))
              if result != msg : await client.send_message(message.channel, result)
            """

            if not msg.startswith(p) : return 

            args = msg.split(" ")
            cmd = args[0][len(p):]
            cmd = unidecode(cmd).lower() # on vire les accents et on met en minuscules
            del args[0]
            arg = " ".join(args)

            if cmd == "flag" :
                await client.delete_message(message)
                await client.send_message(message.author, "Envoie-moi le flag **PAR MP** (avec le préfixe `!`) sinon tout le monde reçoit une notif avec la réponse \N{TIRED FACE}")

            elif cmd == "ping" :
                embed = discord.Embed(title="\N{TABLE TENNIS PADDLE AND BALL} Pong !", color=0x00ff00)
                embed.add_field(name=message.author.name+" -> "+client.user.name+" :", value=str(round(time.time() * 1000 - t * 1000 , 1))+" ms", inline=True)
                debut = time.time()
                reponse = await client.send_message(message.channel, embed=embed)
                embed.add_field(name=message.author.name+" <- "+client.user.name+" :", value=str(round(time.time() * 1000 - debut * 1000 , 1))+" ms", inline=True)
                await client.edit_message(reponse, embed=embed)

            elif cmd == "help" or cmd in alias["help"]:
                if len(args) == 0 :
                    page = -1
                    liste = sorted(commandes.keys())
                    pageMax = ceil(len(liste)/5)
                    boucle = True
                    embed = discord.Embed(color=0x00ff00)
                    embed.add_field(name="Bienvenue dans ce superbe menu help ^^", value="** **")
                    embed.add_field(name="Vous pouvez naviguez de page en page avec les réactions ci-dessous.", value="** **")
                    embed.add_field(name="Si vous voulez ENCORE PLUS de détails sur une commande, vous pouvez faire `"+p+"help <commande>`.", value="** **")
                    interface = await client.send_message(message.channel, embed=embed)
                    await client.add_reaction(interface, "\N{BLACK RIGHT-POINTING TRIANGLE}")
                    res = await client.wait_for_reaction(["\N{BLACK RIGHT-POINTING TRIANGLE}"], user=message.author, timeout=120, message=interface)
                    while boucle:
                        if res == None :
                            boucle = False
                            await client.delete_message(interface)
                            break
                        try : await client.clear_reactions(interface)
                        except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de supprimer les réactions sous me propres messages il va donc falloir que tu enlèves et remettes ta réaction pour continuer et que tu engeules les gestionnaires de ce serveur.")
                        emo = str(res.reaction.emoji)
                        if emo == "\N{BLACK LEFT-POINTING TRIANGLE}" : page -= 1
                        elif emo == "\N{BLACK RIGHT-POINTING TRIANGLE}" : page += 1
                        if page >= pageMax :
                            page = pageMax
                            embed = discord.Embed(color=0x00ff00)
                            embed.add_field(name="Et voilà c'est fini ^^", value="** **")
                            embed.add_field(name="C'était cool, hein ?", value="** **")
                        elif page < 0:
                            page = -1
                            embed = discord.Embed(title="Super menu help", description="Bienvenue dans ce superbe menu help ^^\nVous pouvez naviguez de page en page avec les réactions ci-dessous. Si vous voulez **ENCORE PLUS** de détails sur une commande, vous pouvez faire `"+p+"help <commande>`.", color=0x00ff00)
                        else :
                            embed = discord.Embed(title="Super menu help", color=0x00ff00)
                            embed.clear_fields()
                            for commande in liste[page*5:page*5+5]:
                                embed.add_field(name=p+commande+" "+commandes[commande][0]+" :", value=commandes[commande][1], inline=True)
                        embed.set_footer(text="\N{BOOKMARK TABS} page "+str(page+1)+"/"+str(pageMax+1))
                        interface = await client.edit_message(interface, embed=embed)
                        if page > -1 : await client.add_reaction(interface, "\N{BLACK LEFT-POINTING TRIANGLE}")
                        if page < pageMax : await client.add_reaction(interface, "\N{BLACK RIGHT-POINTING TRIANGLE}")
                        res = await client.wait_for_reaction(["\N{BLACK LEFT-POINTING TRIANGLE}","\N{BLACK RIGHT-POINTING TRIANGLE}"], user=message.author, timeout=120, message=interface)
                        if res == None :
                            boucle = False
                            await client.delete_message(interface)                        

                elif len(args) == 1 :
                    commande = unidecode(args[0]).lower()
                    if not commande in commandes :
                        for test in alias :
                            if commande in alias[test]:
                                commande = test
                    if commande in commandes :
                        embed = discord.Embed(title=p+commande, color=0x00ff00)
                        embed.add_field(name="Usage :", value=usage(p, commande, mini=True), inline=True)
                        embed.add_field(name="Description :", value=commandes[commande][1], inline=True)
                        if commande in alias : embed.add_field(name="Alias :", value=", ".join(alias[commande]), inline=True)
                        await client.send_message(message.channel, embed=embed)
                    else :
                        await client.send_message(message.channel, "Pas d'infos pour cette commande...")
                else : await client.send_message(message.channel, usage(p, cmd))

            elif cmd == 'roll' :
                await client.send_message(message.channel, str(random.randint(0, 100)))

            elif cmd == 'heure' :
                await client.send_message(message.channel, time.strftime('Il est %H:%M passé de %S secondes.', time.localtime()))


            elif cmd == 'date':
                await client.send_message(message.channel, time.strftime('Nous sommes le %d/%m/%Y.', time.localtime()))

            elif cmd == 'blague':
                with open("blagues.txt", "r") as f : c = f.read().split('\n')
                if len(args) == 0 :
                    blague = random.choice(c).split('|')
                    while blague == [""] : blague = random.choice(c).split('|')
                    for txt in blague :
                        await client.send_message(message.channel, txt)
                        time.sleep(2)               

                elif args[0] == "add" :
                    blague = " ".join(args[1:]).replace("\n", "|")
                    if blague in c : await client.send_message(message.channel, message.author.mention + 'Je connais déjà cette blague.')
                    else :
                        with open("blagues.txt", "a") as f : f.write('\n' + blague)
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                else : await client.send_message(message.channel, usage(p, cmd))

            elif cmd == 'proverbe':
                with open("proverbes.txt", "r") as f : c = f.read().split('\n')
                if len(args) == 0 :
                    proverbe = random.choice(c)
                    while proverbe == "" : proverbe = random.choice(c)
                    await client.send_message(message.channel, proverbe)

                elif args[0] == "add" :
                    proverbe = " ".join(args[1:])
                    if proverbe in c : await client.send_message(message.channel, message.author.mention + 'Je connais déjà ce proverbe.')
                    else :
                        with open("proverbes.txt", "a") as f : f.write('\n' + proverbe)
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                else : await client.send_message(message.channel, usage(p, cmd))

            elif cmd == 'citation':
                with open("citations.txt", "r") as f : c = f.read().split('\n')
                if len(args) == 0 :
                    citation = random.choice(c)
                    while citation == "" : citation = random.choice(c)
                    await client.send_message(message.channel, citation)

                elif args[0] == "add" :
                    citation = " ".join(args[1:])
                    if citation in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà cette citation.')
                    else :
                        with open("citations.txt", "a") as f : f.write('\n' + citation)
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                else : await client.send_message(message.channel, usage(p, cmd))

            elif  cmd == 'wiki':
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    req = quote_plus(arg)
                    resultat = getUrl("https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exsentences=2&explaintext&exintro&redirects=true&titles=" + req)["query"]["pages"]
                    id = list(resultat)[0]
                    titre = resultat[id]["title"]
                    if id == "-1" :
                        resultat = getUrl("https://fr.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&search=" + req)
                        if resultat[2] != [] and resultat[2][0] != "" :
                            embed = discord.Embed(description=resultat[2][0], color=0x00ff00)
                            titre = quote_plus(resultat[1][0])
                            image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + titre)["query"]["pages"]
                            id = list(image)[0]
                            if "thumbnail" in image[id] : embed.set_image(url=image[id]["thumbnail"]["source"])
                            await client.send_message(message.channel, embed=embed)
                        else : await client.send_message(message.channel, "Auncun résultat pour cette recherche...")
                    else :
                        embed = discord.Embed(description=resultat[id]["extract"], color=0x00ff00)
                        image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + req)["query"]["pages"]
                        id = list(image)[0]
                        if "thumbnail" in image[id] : embed.set_image(url=image[id]["thumbnail"]["source"])
                        await client.send_message(message.channel, embed=embed)                  
                        
                    
            elif cmd == 'fast':
                if message.channel != spamBot :
                    if spamBot : await client.send_message(message.channel, "On va quand même pas jouer ici alors qu'il y'a un salon " + spamBot.mention + " !")
                    else : await client.send_message(message.channel, "Vous pouvez contacter le responsable de ce serveur car à cause de lui aucun salon n'a été configuré pour autoriser cette commande !")
                elif len(args) != 1 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    try : niveau = int(args[0])
                    except ValueError: await client.send_message(message.channel, usage(p, cmd))
                    else :
                        if not(1 <= niveau <= 5) : await client.send_message(message.channel, usage(p, cmd))
                        else :             
                            chaine = ""
                            if niveau == 5:
                                choix = caracteres[3]
                                l = random.randint(20, 30)
                            else :
                                choix = caracteres[niveau - 1]
                                l = random.randint(10, 20)
                            i = 0
                            while i < l:
                                chaine += random.choice(choix)
                                i += 1
                            aff = ""
                            for c in chaine : aff += c + " "
                            debut = time.time()
                            await client.send_message(message.channel, fast + "Chaine à recopier : " + aff[:-1] + "\n\nLes espaces c'est juste pour éviter le copier-coller ;-)")
                            boucle = True
                            while boucle :
                                proposition = await client.wait_for_message(timeout=60-int(time.time()-debut), channel=spamBot)
                                if proposition == None :
                                    await client.send_message(message.channel, "Temps écoulé")
                                    boucle = False
                                elif proposition.content == chaine :
                                    await client.send_message(message.channel, "Bien joué " + proposition.author.mention + ", tu as réussi en "+str(round(time.time()-debut, 2))+" secondes !")
                                    boucle = False
                                else :
                                    await client.add_reaction(proposition, "\N{CROSS MARK}")

            elif cmd == 'r2d' :
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    r = arg
                    r = r.replace(' ', '').upper()
                    dico = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
                    d = 0
                    erreur = False
                    i = 0
                    while i < len(r):
                        if not(r[i] in dico) :
                            erreur = True
                            break
                        if i == len(r) - 1:
                            d += dico[r[i]]
                        else :
                            if dico[r[i]] < dico[r[i + 1]] :
                                d -= dico[r[i]]
                            else :
                                d += dico[r[i]]
                        i += 1
                    if erreur :
                        await client.send_message(message.channel, "Le nombre entré n'est pas correct.")
                    else : await client.send_message(message.channel, str(d))


            elif cmd == "cnf" :
                fact = getUrl("https://www.chucknorrisfacts.fr/api/get?data=tri:alea;nb:1")[0]['fact']
                await client.send_message(message.channel, fact)

            elif cmd == "urban" or cmd in alias["urban"] :
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    data = getUrl("http://api.urbandictionary.com/v0/define?term=" + quote_plus(arg))["list"]
                    if len(data) == 0 : await client.send_message(message.channel, 'Aucun résultat...')
                    else :
                        data = data[0]
                        em = discord.Embed(title="Urban Dictionnary", colour=0x00ff00)
                        em.add_field(name="Définition :", value=data["definition"], inline=True)
                        em.add_field(name="Exemple :", value=data["example"], inline=True)
                        em.add_field(name="Auteur :", value=data["author"], inline=True)
                        em.add_field(name="Vote :", value=joliStr(data["thumbs_up"])+" \N{THUMBS UP SIGN}   "+joliStr(data["thumbs_down"])+" \N{THUMBS DOWN SIGN}", inline=True)
                        await client.send_message(message.channel, embed=em)

            elif cmd == "rug" :
                data = getUrl("https://randomuser.me/api/?nat=fr")['results'][0]
                em = discord.Embed(title=data['name']['first'].capitalize() + " " + data['name']['last'].capitalize(), colour=0x00ff00)
                em.set_image(url=data['picture']['large'])
                em.add_field(name="adresse mail :", value=data['email'].replace("example.com", random.choice(["gmail.com","yahoo.com","neuf.fr","laposte.net","orange.fr","ovh.net",])), inline=False)
                jour, heure = data['dob']['date'].split("T")
                jour = jour.split("-")
                em.add_field(name="date de naissance :", value=jour[2] + "/" + jour[1] + "/" + jour[0] + " à " + heure[:-1], inline=False)
                em.add_field(name="age :", value=str(data['dob']['age']) + " ans", inline=False)
                em.add_field(name="numéro de téléphone :", value=data['phone'].replace("-", " "), inline=False)
                em.add_field(name="adresse :", value=data['location']['street'] + " à " + data['location']['city'].title(), inline=False)
                em.add_field(name="pseudo :", value=data['login']['username'], inline=False)
                em.add_field(name="mot de passe :", value=data['login']['password'], inline=False)
                await client.send_message(message.channel, embed=em)

            elif cmd == "vps" :
                txt = "Je suis allumé depuis " + popen("uptime -p").read().replace("up ","").replace("\n","").replace("hour","heure").replace("day","jour").replace("week","semaine") + ".\n"
                txt += "Il me reste " + popen("df -h /").read().split("\n")[1].split()[3] + "o de libre sur mon disque dur.\n"
                txt += popen("mpstat").read().split("\n")[3].split()[-1] + "% de mon CPU est diponible.\n"
                m = popen("free -m").read().split("\n")[1].split()
                txt += "J'ai " + popen("free -mh").read().split("\n")[1].split()[3] + "o de RAM de dispo (soit " + str(round(int(m[3])/int(m[1])*100, 2)) + "%).\n"
                txt += "Mon nom d'hôte est " + popen("hostname --fqdn").read().replace("\n","") + ".\n"
                await client.send_message(message.channel, txt)

            elif cmd == "gif" :            
                if len(args) == 0 :
                    loader = await client.send_message(message.channel, "Recherche d'un GIF...")
                    url = "http://api.giphy.com/v1/gifs/random?api_key=" + secret["giphy-key"]
                    gif = getUrl(url)['data']
                    await client.edit_message(loader, "Téléchargement du GIF...")
                    with open("/home/ribt/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['image_url']).read())
                    await client.edit_message(loader, "Upload du GIF...")
                    await client.send_file(message.channel, "tmp.gif", filename="random.gif")
                    await client.delete_message(loader)
                
                else :
                    loader = await client.send_message(message.channel, "Recherche d'un GIF...")
                    url = "http://api.giphy.com/v1/gifs/search?api_key="+ secret["giphy-key"] + "&lang=fr&limit=1&q=" + quote_plus(arg)
                    gif = getUrl(url)['data'][0]
                    await client.edit_message(loader, "Téléchargement du GIF...")
                    with open("/home/ribt/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['images']['original']['url']).read())
                    await client.edit_message(loader, "Upload du GIF...")
                    await client.send_file(message.channel, "tmp.gif", filename=gif['title'].replace(" ", "_").replace("_GIF", "")+".gif")
                    await client.delete_message(loader)

            elif cmd == "devine" or cmd in alias["devine"] :
                if message.channel != spamBot :
                    if spamBot : await client.send_message(message.channel, "On va quand même pas jouer ici alors qu'il y'a un salon " + spamBot.mention + " !")
                    else : await client.send_message(message.channel, "Vous pouvez contacter le responsable de ce serveur car à cause de lui aucun salon n'a été configuré pour autoriser cette commande !")
                else :
                    coups = 0
                    nombreChoisis = random.randint(0, 100)
                    await client.send_message(message.channel, "C'est parti mon kiki ! (devine mon nombre entre 0 et 100)")
                    boucle = True
                    while boucle:
                        proposition = await client.wait_for_message(timeout=60, channel=spamBot)
                        if proposition == None :
                            await client.send_message(spamBot, "Vous êtes trop lents ! (Mon nombre était " + str(nombreChoisis) + ".)")
                            boucle = False
                        else :
                           try :
                                nombreTest = int(proposition.content)
                                if nombreTest == nombreChoisis : await client.send_message(spamBot, "Gagné en "+str(coups)+" coups "+proposition.author.mention+" !")
                                elif nombreTest < nombreChoisis : await client.send_message(spamBot, "C'est plus que "+str(nombreTest)+"...")
                                else : await client.send_message(spamBot, "C'est moins que "+str(nombreTest)+"...")
                           except ValueError : pass

            elif cmd == "weather" or cmd in alias["weather"] :
                try :
                    ville, jours = args
                    jours = int(jours)
                except ValueError :
                    await client.send_message(message.channel, usage(p, cmd))
                else :
                    if not(1 <= jours <= 7) : await client.send_message(message.channel, "<jours> doit être un nombre entre 1 et 7")
                    else :
                        try : data = feedparser.parse("http://api.meteorologic.net/forecarss?p=" + quote_plus(ville))['entries'][0]['summary']
                        except IndexError : await client.send_message(message.channel, "Pas de données météo pour cette ville...")
                        else :
                            if data == "" : await client.send_message(message.channel, "Pas de données météo pour cette ville...")
                            else :
                                data = data.replace("<strong>", "").replace("</strong>", "").replace("\t", "").replace("<br />", "\n")
                                data = data.split("\n\n\n")[:-1]
                                data[0] = "\n" + data[0]
                                i = 0
                                while i < len(data) and i < jours :
                                    data[i] = data[i].split("\n")[1:-1]
                                    data[i][0] = "__" + data[i][0][:-1] + "__"
                                    await client.send_message(message.channel, "\n".join(data[i]))
                                    i += 1

            elif cmd == "rot13" :
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else : await client.send_message(message.channel, codecs.encode(arg, 'rot_13'))

            elif cmd == "whois" :
                if len(args) != 1 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    dn = args[0]
                    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=" + secret["whois-key"] + "&outputFormat=JSON&domainName=" + quote_plus(dn)
                    data = getUrl(url)
                    if "ErrorMessage" in data : await client.send_message(message.channel, "L'API renvoit l'erreur suivante : `"+data["ErrorMessage"]["msg"]+"`.")
                    else :
                        data = data['WhoisRecord']
                        if "dataError" in data : await client.send_message(message.channel, "L'API renvoit l'erreur suivante : `"+data["dataError"]+"`.")
                        else :
                            if not "administrativeContact" in data["registryData"] :
                                txt = "```"+data['registryData']['rawText']+"```"
                            else :
                                txt = "```"+data['registryData']['administrativeContact']['rawText']+"```"
                            if len(txt) > 2000:
                                txt = txt[:1992]+"```[...]"
                            await client.send_message(message.channel, txt)

            elif cmd == "pi" : await client.send_message(message.channel, "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420198938095257201065485863278865936153381827968230301952035301852968995773622599413891249721775283479131515574857242454150695950829533116861727855889075098381754637464939319255060400927701671139009848824012858361603563707660104710181942955596198946767837449448255379774726847104047534646208046684259069491293313677028989152104752162056966024058038150193511253382430035587640247496473263914199272604269922796782354781636009341721641219924586315030286182974555706749838505494588586926995690927210797509302955321165344987202755960236480665499119881834797753566369807426542527862551818417574672890977772793800081647060016145249192173217214772350141441973568548161361157352552133475741849468438523323907394143334547762416862518983569485562099219222184272550254256887671790494601653466804988627232791786085784383827967976681454100953883786360950680064225125205117392984896084128488626945604241965285022210661186306744278622039194945047123713786960956364371917287467764657573962413890865832645995813390478027590")

            elif cmd == "pendu" :
                if message.channel != spamBot :
                    if spamBot : await client.send_message(message.channel, "On va quand même pas jouer ici alors qu'il y'a un salon " + spamBot.mention + " !")
                    else : await client.send_message(message.channel, "Vous pouvez contacter le responsable de ce serveur car à cause de lui aucun salon n'a été configuré pour autoriser cette commande !")
                else :
                    vies = len(pendu)
                    mot = random.choice(mots)
                    aff = ["_"]*len(mot)
                    await client.send_message(message.channel, "C'est parti !")
                    await client.send_message(message.channel, " ".join(aff).replace("_", r"\_"))
                    while "_" in aff and vies > 0:
                        proposition = await client.wait_for_message(timeout=60, channel=spamBot)
                        if proposition == None :
                            await client.send_message(spamBot, "Vous êtes trop lents le mot était *" + mot + "* \N{CONFUSED FACE}")
                            vies = 0
                        elif len(proposition.content) == 1:
                            lettre = unidecode(proposition.content).lower()
                            if lettre in unidecode(mot) :
                                for i in range(len(aff)) :
                                    if unidecode(mot[i]) == lettre : aff[i] = mot[i]
                                await client.send_message(spamBot, " ".join(aff).replace("_", r"\_")) 
                            else :
                                await client.send_message(spamBot, pendu[-vies])
                                await client.send_message(spamBot, " ".join(aff).replace("_", r"\_")) 
                                vies -= 1
                                if vies == 0 :
                                    await client.send_message(spamBot, "PERDU !!! (le mot était... " + mot + " !)")
                    if not "_" in aff : await client.send_message(spamBot, "Gagné ^^")
            
            elif cmd == "role" :
                if not config["managedRolesColor"] :
                    await client.send_message(message.channel, "La gestion des rôles par mon humble personne est désactivée sur ce serveur.")
                    return
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                elif args[0] == "list" :
                    txt = "__Liste des rôles disponibles :__\n\n"
                    aucun = True
                    for i in message.server.roles :
                        if str(i.colour) == config["managedRolesColor"] :
                            txt += "- **" + i.name + "**\n"
                            aucun = False
                    if aucun : await client.send_message(message.channel, "Vous ne pouvez vous ajouter aucun rôle.")
                    else :
                        if suggestion : txt += "\n(Vous pouvez proposer de nouveaux rôles proposer dans " + suggestion.mention + " \N{WINKING FACE})"
                        await client.send_message(message.channel, txt)
                elif len(args) < 2 : await client.send_message(message.channel, usage(p, cmd))

                elif args[0] == "add" :
                    for arg in args[1:] :
                        role = None
                        for i in message.server.roles :
                            if i.name.lower() == arg.lower() : role = i
                        if role == None :
                            if suggestion : await client.send_message(message.channel, "Le rôle *" + arg + "* n'existe pas.")
                            else : await client.send_message(message.channel, "Le rôle *" + arg + "* n'existe pas encore mais vous pouvez le proposer dans " + suggestion.mention + " \N{WINKING FACE}")
                        elif str(role.colour) != config["managedRolesColor"] : await client.send_message(message.channel, "Le rôle *" + arg + "*, t'as pas le droit de le prendre \N{WINKING FACE}")
                        else :
                            try :
                                await client.add_roles(message.author, role)
                                await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                            except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de t'ajouter ce rôle \N{LOUDLY CRYING FACE} (va taper un admin)")
                            
                elif args[0] == "remove" :
                    for arg in args[1:] :
                        role = None
                        for i in message.author.roles :
                            if i.name.lower() == arg.lower() : role = i
                        if role == None : await client.send_message(message.channel, "Tu n'as pas le rôle *" + arg + "*...")
                        else :
                            await client.remove_roles(message.author, role)
                            await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

            elif cmd == "w3w":
                if not(1 <= len(args) <= 2) or args[0].count(".") != 2: await client.send_message(message.channel, usage(p, cmd))
                else :
                    url = "https://api.what3words.com/v2/forward?addr=" + quote_plus(args[0]) + "&key=" + secret["w3w-key"] + "&format=json&display=minimal"
                    if len(args) == 1 and args[1].lower() != "fr" : url += "&lang=" + quote_plus(args[1].lower())
                    else : url += "&lang=fr"
                    gps = getUrl(url)['geometry']
                    if gps == None : await client.send_message(message.channel, "Aucun résultat avec ces trois mots...")
                    else :
                        lat = str(gps['lat'])
                        lng = str(gps['lng'])
                        await client.send_message(message.channel, "coordonées GPS : " + lat + "," + lng)
                        url = "https://services.gisgraphy.com/reversegeocoding/search?format=json&lat=" + lat + "&lng=" + lng
                        adresse = getUrl(url)['result'][0]
                        await client.send_message(message.channel, "adresse complète : " + adresse['formatedFull'])

            elif cmd == "gps":
                try : lat, lng = arg.split(",")
                except :
                    await client.send_message(message.channel, usage(p, cmd))
                    return
                url = "https://api.what3words.com/v2/reverse?coords=" + lat + "," + lng + "&key=" + secret["w3w-key"] + "&lang=fr&format=json&display=minimal"
                w3w = getUrl(url)['words']
                if w3w == None : await client.send_message(message.channel, "Les coordonnées semblent être incorrectes... Respectez la syntaxe : `"+p+"gps <latitude,longitude>`.")
                else :
                    await client.send_message(message.channel, "w3w : " + w3w)              
                    url = "https://services.gisgraphy.com/reversegeocoding/search?format=json&lat=" + lat + "&lng=" + lng
                    adresse = getUrl(url)['result'][0]
                    await client.send_message(message.channel, "adresse complète : " + adresse['formatedFull'])

            elif cmd == "speedtest":
                loader = await client.send_message(message.channel, "Recherche du meilleur serveur...")
                s = speedtest.Speedtest()
                s.get_best_server()
                await client.edit_message(loader, "Mesure du débit descendant (ça peut prendre un certain temps)...")
                s.download()
                await client.edit_message(loader, "Mesure du débit montant (ça peut prendre un certain temps)...")
                s.upload()
                await client.edit_message(loader, "Génération d'une jolie image trop stylée...")
                url = s.results.share()
                await client.delete_message(loader)
                await client.send_message(message.channel, "Ma connexion : " + url)


            elif cmd == "lmgtfy" or cmd in alias["lmgtfy"]:
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    url = "https://api.qwant.com/egp/search/web?count=5&q=" + quote_plus(arg)
                    resultats = getUrl(url)
                    if resultats['status'] == "error" : await client.send_message(message.channel, "Une erreur s'est produite, j'espère que c'est pas parce que t'as écrit n'importe quoi \N{WINKING FACE}")
                    else :
                        txt = "Voici les 5 premiers liens de ta recherche sur Qwant :\n"
                        if cmd == "lmgtfy" : txt +=  "(t'as quand même pas cru que j'allais utiliser Google \N{SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES})\n"
                        for i in resultats['data']['result']['items'] : txt += i['url'] + "\n"
                        txt += "Voilà, voilà..."
                        await client.send_message(message.channel, txt)

            elif cmd == "chr" :
                if len(args) != 1 or len(args[0]) != 1 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    c = arg
                    try : await client.send_message(message.channel, "Le caractère `" + c + "` répond au doux nom de **" + unicodedata.name(c) + "** et son code Unicode est **" + str(ord(c)) + "**.")
                    except : await client.send_message(message.channel, "Une erreur s'est produite...")

            elif cmd == "unicode" :
                if len(args) != 1 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    try :
                        c = chr(int(arg))
                        await client.send_message(message.channel, "Le caractère correspondant au code " + arg + " est le suivant : `" + c + "` (" + unicodedata.name(c) + ").")
                    except (ValueError, OverflowError) : await client.send_message(message.channel, "Aucun caractère ne correspond à ce numéro...")

            elif cmd == "loc" :
                l = popen("wc -l tux-v2.py").read().split(" ")[0]
                s = popen("ls -lh tux-v2.py").read().split(" ")[4] + "o"
                await client.send_message(message.channel, "Mon code source (écrit en Python) comporte actuellement " + joliStr(l) + " lignes (" + s + ").")

            elif cmd == "crypto" :
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    req = arg
                    crypto = getUrl("https://api.coinmarketcap.com/v1/ticker/?limit=0")
                    cid = None
                    for i in crypto :
                        if i["id"].lower() == req or i["name"].lower() == req or i["symbol"].lower() == req : cid = i["id"]
                    if cid :
                        data = getUrl("https://api.coinmarketcap.com/v1/ticker/" + cid + "/?convert=EUR")[0]
                        txt = "**valeur :** " + joliStr(data["price_eur"]) + " € (" + joliStr(data["price_usd"]) + " $ ou encore " + joliStr(data["price_btc"]) + " \u20BF)\n"
                        if data["percent_change_1h"][0] != "-" : data["percent_change_1h"] = "+" + joliStr(data["percent_change_1h"])
                        txt += "**évolution depuis 1 h :** " + data["percent_change_1h"] + " %\n"
                        if data["percent_change_24h"][0] != "-" : data["percent_change_24h"] = "+" + joliStr(data["percent_change_24h"])
                        txt += "**évolution depuis 24 h :** " + data["percent_change_24h"] + " %\n"
                        if data["percent_change_7d"][0] != "-" : data["percent_change_7d"] = "+" + joliStr(data["percent_change_7d"])
                        txt +="**évolution depuis une semaine :** " + data["percent_change_7d"] + " %\n"
                        txt += "**volume (24 h) :** " + joliStr(data["24h_volume_eur"]) + " €\n"
                        if data["market_cap_eur"] : txt +="**capitalisation boursière :** " + joliStr(data["market_cap_eur"]) + " €"
                        embed=discord.Embed(title=data["name"] + " (" + data["symbol"] + ")", description=txt, color=0x00ff00)
                        await client.send_message(message.channel, embed=embed)
                    else : await client.send_message(message.channel, "Je n'ai pas trouvé cette crypto-monnaie...")

            elif cmd == "user" or cmd in alias["user"] :
                if len(message.mentions) == 1 :
                    member = message.mentions[0]
                    user = await client.get_user_info(member.id)
                    em = discord.Embed(title=user.name, colour=0x00ff00)
                    em.set_image(url=user.avatar_url)
                    if user.bot : em.add_field(name="bot :", value="oui", inline=True)
                    else : em.add_field(name="bot :", value="non", inline=True)
                    em.add_field(name="id :", value=user.id, inline=True)
                    em.add_field(name="discriminator :", value=user.discriminator, inline=True)
                    em.add_field(name="compte créé le", value=time.strftime("%d/%m/%Y", date.timetuple(user.created_at)), inline=True)
                    em.add_field(name="serveur rejoint le", value=time.strftime("%d/%m/%Y", date.timetuple(member.joined_at)), inline=True)
                    em.add_field(name="statut :", value=str(member.status), inline=True)
                    if member.game : em.add_field(name="jeu :", value=str(member.game), inline=True)
                    if member.top_role : em.add_field(name="plus grand role :", value=str(member.top_role), inline=True)
                    if member.nick : em.add_field(name="surnom :", value=member.nick, inline=True)
                    await client.send_message(message.channel, embed=em)
                else : await client.send_message(message.channel, usage(p, cmd))

            elif cmd == "life": await client.send_file(message.channel, "life.gif")

            elif cmd == "obvious": await client.send_file(message.channel, "obvious.gif")

            elif cmd == "ah": await client.send_file(message.channel, "ah.gif")
            
            elif cmd == "gratuit": await client.send_file(message.channel, "gratuit.png")

            elif cmd == 'haddock':
                with open("haddock.txt","r") as f : c = f.read().split('\n')
                await client.send_message(message.channel, random.choice(c))

            elif modo in message.author.roles and cmd == "mute" :
                if len(message.mentions) != 1 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    user = message.mentions[0]
                    try :
                        if args[1][-1] == "s" : temps = int(args[1][:-1])
                        elif args[1][-1] == "m" : temps = int(args[1][:-1])*60
                        elif args[1][-1] == "h" : temps = int(args[1][:-1])*3600
                        elif args[1][-1] == "j" : temps = int(args[1][:-1])*3600*24
                    except ValueError : await client.send_message(message.channel, "Le temps donné est invalide.")
                    motif = " ".join(args[2:])
                    em = discord.Embed(title="Confirmation de mute", description="Tu as une minute pour confirmer ou annuler le mute.", colour=0x00ff00)
                    em.add_field(name="utilisateur :", value=user.name)
                    em.add_field(name="durée :", value=args[1]+" ("+str(temps)+" secondes)")
                    em.add_field(name="motif :", value=motif)
                    demande = await client.send_message(message.channel, embed=em)
                    await client.add_reaction(demande, "\N{WHITE HEAVY CHECK MARK}")
                    await client.add_reaction(demande, "\N{CROSS MARK}")
                    res = await client.wait_for_reaction(user=message.author, timeout=60, message=demande)
                    if res and str(res.reaction.emoji) == "\N{WHITE HEAVY CHECK MARK}" :
                        with open("mute.json", "r") as f : mute = json.loads(f.read())
                        if not serv in mute : mute[serv] = {}
                        mute[serv][user.id] = {}
                        mute[serv][user.id]['time'] = args[1]
                        mute[serv][user.id]['by'] = message.author.name
                        mute[serv][user.id]['expires'] = time.time() + temps
                        mute[serv][user.id]['motif'] = motif
                        with open("mute.json", "w") as f : f.write(json.dumps(mute, indent=4))
                        if muteRole : 
                            try : await client.add_roles(user, muteRole)
                            except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de lui ajouter le rôle "+muteRole.mention+" \N{LOUDLY CRYING FACE} (va taper un admin)")
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                        await client.delete_message(demande)
                        await client.send_message(user, "Tu a été mute pendant " + args[1] + " par **" + message.author.name + "** pour le motif suivant : *" + motif + "*.")
                    else :
                        await client.send_message(message.channel, "Le mute a été annulé.")


            elif modo in message.author.roles and cmd == "unmute" :
                if len(message.mentions) != 1 : await cient.send_message(message.channel, usage(p, cmd))
                else :
                    with open("mute.json", "r") as f : mute = json.loads(f.read())
                    if message.mention.id in mute[server.id] :
                        del mute[server.id][message.mention.id]
                        with open("mute.json", "w") as f : f.write(json.dumps(mute, indent=4))
                    else : await cient.send_message(message.channel, "Cette personne n'est pas mute...")


            elif cmd == "youtube" or cmd in alias["youtube"] :
                 if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                 else :
                    recherche = getUrl("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=" + quote_plus(arg) + "&key=" + secret["google-key"])["items"][0]["id"]
                    if recherche == [] : await client.send_message(message.channel, "Aucun résultat...")
                    else :
                        if recherche["kind"] == "youtube#channel" :
                            channelId = recherche["channelId"]
                            data = getUrl("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=" + channelId + "&key=" + secret["google-key"])["items"][0]
                            em = discord.Embed(title=data["snippet"]["title"], colour=0x00ff00)
                            #em.set_image(url=data["snippet"]["thumbnails"]["high"]["url"])
                            em.add_field(name="id :", value=data["id"], inline=True)
                            desc = data["snippet"]["description"]
                            if len(desc) < 1000 : em.add_field(name="description :", value=desc, inline=True)
                            else : em.add_field(name="description :", value=desc[:1000]+"\n\n[...]", inline=True)
                            em.add_field(name="date de création de la chaîne :", value=data["snippet"]["publishedAt"].replace("T", " à ")[:-5], inline=True)
                            if "country" in data["snippet"] : em.add_field(name="pays :", value=data["snippet"]["country"], inline=True)
                            if not data["statistics"]["hiddenSubscriberCount"] :
                                em.add_field(name="nombre total de vues :", value=joliStr(data["statistics"]["viewCount"]), inline=True)
                                em.add_field(name="nombre d'abonnés :", value=joliStr(data["statistics"]["subscriberCount"]), inline=True)
                                em.add_field(name="nombre de vidéos :", value=joliStr(data["statistics"]["videoCount"]), inline=True)
                                em.add_field(name="nombre de commentaires postés :", value=joliStr(data["statistics"]["commentCount"]), inline=True)
                                await client.send_message(message.channel, embed=em)
                                await client.send_message(message.channel, "https://www.youtube.com/channel/"+channelId)
                        elif recherche["kind"] == "youtube#video" :
                            videoId = recherche["videoId"]
                            data = getUrl("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=" + videoId + "&key=" + secret["google-key"])["items"][0]
                            em = discord.Embed(title=data["snippet"]["title"], colour=0x00ff00)
                            #em.set_image(url=data["snippet"]["thumbnails"]["high"]["url"])
                            em.add_field(name="id :", value=data["id"], inline=True)
                            desc = data["snippet"]["description"]
                            if len(desc) < 1000 : em.add_field(name="description :", value=desc, inline=True)
                            else : em.add_field(name="description :", value=desc[:1000]+"\n\n[...]", inline=True)
                            em.add_field(name="tags :", value=", ".join(data["snippet"]["tags"]), inline=True)
                            em.add_field(name="date de publication :", value=data["snippet"]["publishedAt"].replace("T", " à ")[:-5], inline=True)
                            em.add_field(name="nom de la chaîne :", value=data["snippet"]["channelTitle"], inline=True)
                            if "country" in data["snippet"] : em.add_field(name="pays :", value=data["snippet"]["country"], inline=True)
                            em.add_field(name="nombre de vues :", value=joliStr(data["statistics"]["viewCount"]), inline=True)
                            if "likeCount" in data["statistics"] :
                                pourcent = round(int(data["statistics"]["likeCount"])*100/(int(data["statistics"]["likeCount"])+int(data["statistics"]["dislikeCount"])),2)
                                em.add_field(name="nombre de likes :", value=joliStr(data["statistics"]["likeCount"]) + " (" + str(pourcent) + "%)", inline=True)
                                em.add_field(name="nombre de dislikes :", value=joliStr(data["statistics"]["dislikeCount"]) + " (" + str(round(100-pourcent, 2)) + "%)", inline=True)
                            if "commentCount" in data["statistics"] :
                                em.add_field(name="nombre de commentaires :", value=joliStr(data["statistics"]["commentCount"]), inline=True)
                            em.add_field(name="résolution :", value=data["contentDetails"]["definition"].upper(), inline=True)
                            em.add_field(name="dimension :", value=data["contentDetails"]["dimension"].upper(), inline=True)
                            em.add_field(name="projection :", value=data["contentDetails"]["projection"], inline=True)
                            em.add_field(name="catégorie :", value=ytCategories[data["snippet"]["categoryId"]], inline=True)
                            if data["contentDetails"]["licensedContent"] : em.add_field(name="contenu sous licence :", value="oui", inline=True)
                            else : em.add_field(name="contenu sous licence :", value="non", inline=True)
                            await client.send_message(message.channel, embed=em)
                            await client.send_message(message.channel, "https://www.youtube.com/watch?v="+videoId)
                        else : await client.send_message(message.channel, "Aucun résultat...")

            elif cmd == "code" :
                await client.send_message(message.channel, "Mon code source (en Python) : https://github.com/ribt/ceux-qui-savent-coder-mais-qu-ont-pas-d-idees/blob/master/bots/tux/bot.py")

            elif cmd == "ecris" :
                await client.delete_message(message)
                await client.send_typing(message.channel)

            elif cmd == "defis":
                with open("score.json", "r") as f : score = json.loads(f.read())
                with open("flags.json", "r") as f : l = len(json.loads(f.read()))
                if len(args) == 0 :
                    leaders = []
                    pos = 1
                    exaquo = 0
                    for i in range(10):
                        best = 0
                        tmp = None
                        for userId in score :
                            if score[userId]["points"] >= best and not userId in [leader["id"] for leader in leaders]:
                                best = score[userId]["points"]
                                tmp = userId
                        if tmp != None :
                            if len(leaders) == 0 : leaders.append({"pos":1, "id":tmp})
                            else :
                                if score[tmp]["points"] == score[leaders[-1]["id"]]["points"] : exaquo += 1 # égalité avec le précédent
                                else : exaquo = 0
                                leaders.append({"pos":pos-exaquo, "id":tmp})
                            pos += 1
                          
                              
                    txt = "classement de https://ribt.fr/defis/ (TOP 10) :\n\n"
                    for leader in leaders:
                        txt += str(leader["pos"]) + ". "
                        txt += "**" + discord.utils.get(message.server.members, id=leader["id"]).name + "** "
                        txt += str(score[leader["id"]]["points"]) + " pts ("
                        txt += str(round(len(score[leader["id"]]["reussis"])/l*100)) + " %) \n"
                    await client.send_message(message.channel, txt)
  
                elif len(message.mentions) == 1 :
                    userId = message.mentions[0].id
                    if not userId in score : await client.send_message(message.channel, "**" + message.mentions[0].name + "** n'a réussi aucun défi donc son score est logiquement de zéro...")
                    else :
                        txt = "Le score de **" + message.mentions[0].name + "** est actuellement de " + str(score[userId]["points"]) + " points (il a réussi les défis suivants : "
                        for i in score[userId]["reussis"]:
                            txt += str(i)
                            if score[userId]["reussis"].index(i) != len(score[userId]["reussis"])-1 : txt += ", "
                        txt += ")."
                        await client.send_message(message.channel, txt)
                else : await client.send_message(message.channel, usage(p, cmd))

            elif cmd == "qr" :
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    qrcode.make(arg).save("qr.png")
                    await client.send_file(message.channel, "qr.png")

            elif cmd == "pokemon" :
                pokemons = glob("pokemons/*.gif")
                file = random.choice(pokemons)
                name = re.search(r"pokemons\/([a-z]+)(-[a-z]+)?\.gif", file).group(1)
                await client.send_file(message.channel, file, content="Et ton pokémon est... **" + pokeTrad[name] + "** !")

            elif cmd == "table" :
                try : n = int(arg)
                except : await client.send_message(message.channel, usage(p, cmd))
                txt = "__La table de **" + str(n) + "** :__\n\n"
                for i in range(1, 11):
                    txt += str(n) + " \N{MULTIPLICATION SIGN} " + str(i) + " = " + str(i*n) + "\n"
                await client.send_message(message.channel,  txt)

            elif cmd in ["hex", "dec", "bin", "base32", "base64", "base85", "ascii"] :
                try :
                    if cmd == "hex" : n = int(arg.replace(" ", "").replace("0x", ""), 16)
                    elif cmd == "dec" : n = int(arg)
                    elif cmd == "bin" : n = int(arg.replace(" ", "").replace("0b", ""), 2)
                    elif cmd == "base32" :
                        arg = b32decode(arg).decode("utf-8")
                        cmd = "ascii"
                    elif cmd == "base64" :
                        arg = b64decode(arg).decode("utf-8")
                        cmd = "ascii"
                    elif cmd == "base85" :
                        arg = b85decode(arg).decode("utf-8")
                        cmd = "ascii"
                    if cmd == "ascii" :
                        nchars = len(arg)
                        n = 0
                        for i in range(nchars) : n += ord(arg[i]) << 8*(nchars-i-1)
                except ValueError :
                    await client.send_message(message.channel, "Une erreur s'est produite, vérifiez vos arguments...")
                    return
                b = str(bin(n))[2:]

                em = discord.Embed(title="Convertisseur de base", colour=0x00ff00)
                em.add_field(name="hexadécimal :", value=str(hex(n)[2:]).upper())
                em.add_field(name="binaire :", value=b)
                em.add_field(name="décimal :", value=str(n))
                #em.add_field(name="base64 :", value=str(base64.b64encode(bytes([n])))[2:-1])
                txt = ""
                size = 1
                boucle = True
                while boucle:
                    try :
                        for i in (n).to_bytes(size, 'big') : txt += chr(i)
                        boucle = False
                    except OverflowError : size += 1
                em.add_field(name="ASCII :", value=txt)
                em.add_field(name="base64 :", value=b64encode(bytes(txt.encode())).decode("utf-8"))
                em.add_field(name="base32 :", value=b32encode(bytes(txt.encode())).decode("utf-8"))
                em.add_field(name="base85 :", value=b85encode(bytes(txt.encode())).decode("utf-8"))
                await client.send_message(message.channel, embed=em)

            elif cmd == "savoir":
                data = getUrl("https://www.savoir-inutile.com/quizz/androidapplilite")
                em = discord.Embed(title="Savoir inutile", description=data["valcitation"], colour=0x00ff00)
                for source in data["sources"]:
                    em.add_field(name="Source "+str(data["sources"].index(source)+1)+" :", value=source["urlsource"], inline=True)
                await client.send_message(message.channel, embed=em)

            elif cmd == "avatar" :
                if len(message.mentions) == 0 : url = message.author.avatar_url
                else : url = message.mentions[0].avatar_url
                req = Request(url, headers={'User-Agent': "Je n'suis pas un robot (enfin si mais un gentil ^^) !"})
                with open("avatar.webp", "wb") as f : f.write(urlopen(req).read())
                im = Image.open("avatar.webp").convert("RGB")
                im.save("avatar.png")
                await client.send_file(message.channel, "avatar.png")

            elif cmd == "clear" and modo in message.author.roles :
                if len(args) == 1:
                    demande = await client.send_message(message.channel, "Es-tu sûr de ce que tu veux faire (c'est irrémédiable) ?")
                    await client.add_reaction(demande, "\N{WHITE HEAVY CHECK MARK}")
                    await client.add_reaction(demande, "\N{CROSS MARK}")
                    res = await client.wait_for_reaction(user=message.author, timeout=60, message=demande)
                    if res and str(res.reaction.emoji) == "\N{WHITE HEAVY CHECK MARK}" :
                        n = int(args[0])+2
                        try : await client.purge_from(message.channel, limit=n)
                        except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de supprimer des messages \N{LOUDLY CRYING FACE}")
                    else :
                        await client.send_message(message.channel, "La manip a bien été annulée.")
                else : await client.send_message(message.channel, usage(p, cmd))

            elif cmd == "dis" or cmd in alias["dis"] :
                if len(args) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    if not message.author.voice.voice_channel : await client.send_message(message.channel, "Va en vocal et refais la commande.")
                    else :
                        if client.is_voice_connected(message.server):
                            voice = client.voice_client_in(message.server)
                            if voice.channel != message.author.voice.voice_channel :
                                voice.move_to(message.author.voice.voice_channel)
                        else :
                            voice = await client.join_voice_channel(message.author.voice.voice_channel)
                        if not voice.is_connected() : await client.join_voice_channel(message.author.voice.voice_channel)
                        url = "http://tts.readspeaker.com/a/speak?key="+secret["tts-key"]+"&lang=fr_fr&voice=Louis&text=" + quote_plus(arg)
                        try :
                            with open("out.mp3", "wb") as f : f.write(urlopen(url).read())
                            player = voice.create_ffmpeg_player('out.mp3')
                            player.start()
                        except urllib.error.HTTPError as error :
                            if error.code == 503 : await client.send_message(message.channel, "Réessaie plus tard, je n'ai plus de crédit pour l'API \N{LOUDLY CRYING FACE}")
                            else : raise

            elif cmd == "tts" :
                url = "http://tts.readspeaker.com/a/speak?key="+secret["tts-key"]+"&lang=fr_fr&voice=Louis&text=" + quote_plus(arg)
                try :
                    with open("out.mp3", "wb") as f : f.write(urlopen(url).read())
                    await client.send_message(message.channel, "out.mp3")
                except urllib.error.HTTPError as error :
                    if error.code == 503 : await client.send_message(message.channel, "Réessaie plus tard, je n'ai plus de crédit pour l'API \N{LOUDLY CRYING FACE}")
                    else : raise

            elif cmd == "emoticon" :
                with open("emoticons.json", "r") as f : await client.send_message(message.channel, random.choice(json.loads(f.read())))

            elif cmd == "ext" :
                if len(args) != 1 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    arg = arg.lower().replace(".","")
                    try :
                        source = unescape(urlopen("https://www.gandi.net/fr/tlds/"+arg+"/rules").read().decode("utf-8"))
                        if "Erreur 404" in source or "Désolé, l'affichage du prix n'est pas disponible en raison d'une erreur." in source : await client.send_message(message.channel, "Pas d'infos pour cette extension...")
                        else :
                            soup = BeautifulSoup(source, "html.parser")
                            infos = soup.find("ul", {"class": "ProductFeatures-list"}).find_all("p")
                            champs = soup.find("ul", {"class": "ProductFeatures-list"}).find_all("h3")
                            em = discord.Embed(title="."+arg, colour=0x00ff00)
                            for i in range(len(infos)) :
                                champ = champs[i].string
                                if not "Whois" in champ :
                                    info = re.sub(r"<[^>]*>", "", infos[i].string)
                                    em.add_field(name=champ+" :", value=info)
                            soup = BeautifulSoup(re.search(r'<h3 class="TldRules-title">Les règles</h3>(.*)<h3 class="TldRules-title">', source).group(1), "html.parser")
                            rules = soup.find_all("strong")[:5]
                            champs = ["Attribution", "Syntaxe", "IDN (noms de domaine accentués)", "Période d'enregistrement", "Sous-extensions disponibles"]
                            for i in range(5) :
                                rule = re.sub(r"<[^>]*>", "", rules[i].string)
                                em.add_field(name=champs[i]+" :", value=rule)
                            await client.send_message(message.channel, embed=em)
                    except urllib.error.HTTPError as error :
                        if error.code == 404 : await client.send_message(message.channel, "Pas d'infos pour cette extension...")
                        else : raise
                    except : await client.send_message(message.channel, embed=em)

            elif cmd == "config" :
                if admin == None :
                    if message.author == message.server.owner : await client.send_message(message.channel, "\N{WARNING SIGN} Le rôle corespondant à mes administrateurs n'ayant pas encore été configuré seul l'owner du serveur (vous) peut utiliser cette commande.")
                    else :
                        await client.send_message(message.channel, "Le rôle corespondant à mes administrateurs n'ayant pas encore été configuré seul l'owner du serveur peut utiliser cette commande.")
                        return
                elif not admin in message.author.roles :
                    await client.send_message(message.channel, "Cette commande est réservée à mes administrateurs (je te dis pas le bordel sinon).")
                    return
                if len(args) == 0 :
                    page = -1
                    liste = sorted(config.keys())
                    boucle = True
                    embed = discord.Embed(title="\N{HAMMER AND WRENCH} Configuration de ma personne", description="Je suis un super bot donc je suis configurable. Pour cela mon super dev a fait une commande `config` qui s'utilise comme cela : `"+p+"config [list|show|reset|set] [paramètre] [valeur]`. La commande `list` fait une simple liste de toutes les options configurables puis `show` permet d'en connaître la valeur actuelle, `reset` remet l'option à sa valeur par défaut et `set` sert à la modifier à ta guise. Mais comme tout ceci est un peu barbant, si la commande `config` est appelée seule c'est ce joli menu interactif qui apparaît pour bien voir et comprendre mes différentes options. Il suffit de naviguer avec les flèches ci-dessous.", color=0x00ff00)
                    interface = await client.send_message(message.channel, embed=embed)
                    await client.add_reaction(interface, "\N{BLACK RIGHT-POINTING TRIANGLE}")
                    res = await client.wait_for_reaction(["\N{BLACK RIGHT-POINTING TRIANGLE}"], user=message.author, timeout=120, message=interface)
                    while boucle:
                        if res == None :
                            boucle = False
                            await client.delete_message(interface)
                            break
                        try : await client.clear_reactions(interface)
                        except discord.errors.Forbidden : await client.send_message(message.channel, "Je n'ai pas le droit de supprimer les réactions sous me propres messages il va donc falloir que tu enlèves et remettes ta réaction pour continuer et que tu engeules les gestionnaires de ce serveur.")
                        emo = str(res.reaction.emoji)
                        if emo == "\N{BLACK LEFT-POINTING TRIANGLE}" : page -= 1
                        elif emo == "\N{BLACK RIGHT-POINTING TRIANGLE}" : page += 1
                        if page == len(liste) :
                            embed = discord.Embed(color=0x00ff00)
                            embed.add_field(name="Et voilà c'est fini ^^", value="** **")
                            embed.add_field(name="Il ne te reste plus qu'a tout configurer avec `"+p+"config [list|show|reset|set] [paramètre] [valeur]`", value="** **")
                        elif page < 0:
                            embed = discord.Embed(title="\N{HAMMER AND WRENCH} Configuration de ma personne", description="Je suis un super bot donc je suis configurable. Pour cela mon super dev a fait une commande `config` qui s'utilise comme cela : `"+p+"config [list|show|reset|set] [paramètre] [valeur]`. La commande `list` fait une simple liste de toutes les options configurables puis `show` permet d'en connaître la valeur actuelle, `reset` remet l'option à sa valeur par défaut et `set` sert à la modifier à ta guise. Mais comme tout ceci est un peu barbant, si la commande `config` est appelée seule c'est ce joli menu interactif qui apparaît pour bien voir et comprendre mes différentes options. Il suffit de naviguer avec les flèches ci-dessous.", color=0x00ff00)
                        else :
                            embed = discord.Embed(title="\N{HAMMER AND WRENCH} Configuration de ma personne", color=0x00ff00)
                            param = liste[page]
                            embed.add_field(name="Nom de l'option : ", value="`"+param+"`", inline=True)
                            embed.add_field(name="Type : ", value=configInfos[param][0], inline=True)
                            embed.add_field(name="Description : ", value=configInfos[param][1], inline=True)
                            embed.add_field(name="Valeur par défaut : ", value=str(defaultConfig[param]), inline=True)
                            if configInfos[param][0] == "role" and config[param] : txt = discord.utils.get(message.server.roles, id=config[param]).mention
                            elif configInfos[param][0] == "channel" and config[param] : txt = discord.utils.get(message.server.channels, id=config[param]).mention
                            else : txt = str(config[param])
                            embed.add_field(name="Valeur actuelle : ", value=txt, inline=True)
                        embed.set_footer(text="\N{BOOKMARK TABS} page "+str(page+1)+"/"+str(len(liste)+1))
                        interface = await client.edit_message(interface, embed=embed)
                        if page > -1 : await client.add_reaction(interface, "\N{BLACK LEFT-POINTING TRIANGLE}")
                        if page < len(liste) : await client.add_reaction(interface, "\N{BLACK RIGHT-POINTING TRIANGLE}")
                        res = await client.wait_for_reaction(["\N{BLACK LEFT-POINTING TRIANGLE}","\N{BLACK RIGHT-POINTING TRIANGLE}"], user=message.author, timeout=120, message=interface)
                        if res == None :
                            boucle = False
                            await client.delete_message(interface)
                else :
                    if args[0] == "list" :
                        txt = "Voici la liste de mes options configurables (cela peut évoluer avec le temps) :\n"
                        for param in sorted(config.keys()) :
                            txt += "\n- `"+param+"`"
                        await client.send_message(message.channel, txt)

                    elif args[0] == "show" :
                        if len(args) != 2 : await client.send_message(message.channel, "Usage : `"+p+"config show <paramètre>`.")
                        else :
                            if args[1] in config :
                                if configInfos[args[1]][0] == "role" and config[args[1]] : await client.send_message(message.channel, args[1]+" = "+discord.utils.get(message.server.roles, id=config[args[1]]).mention)
                                elif configInfos[args[1]][0] == "channel" and config[args[1]] : await client.send_message(message.channel, args[1]+" = "+discord.utils.get(message.server.channels, id=config[args[1]]).mention)
                                else : await client.send_message(message.channel, args[1]+" = "+str(config[args[1]]))
                            else : client.send_message(message.channel, "Je n'ai pas ce paramètre dans ma liste.")

                    elif args[0] == "reset" :
                        if len(args) != 2 : await client.send_message(message.channel, "Usage : `"+p+"config reset <paramètre>`.")
                        else :
                            if args[1] in config :
                                demande = await client.send_message(message.channel, "Es-tu sûr de ce que tu veux faire (c'est irrémédiable) ?")
                                await client.add_reaction(demande, "\N{WHITE HEAVY CHECK MARK}")
                                await client.add_reaction(demande, "\N{CROSS MARK}")
                                res = await client.wait_for_reaction(user=message.author, timeout=60, message=demande)
                                if res == None or str(res.reaction.emoji) != "\N{WHITE HEAVY CHECK MARK}" :
                                    await client.send_message(message.channel, "Le reset a été annulé.")
                                else :
                                    with open("config.json", "r") as f : config = json.loads(f.read())
                                    config[message.server.id][args[1]] = defaultConfig[args[1]]
                                    with open("config.json", "w") as f : f.write(json.dumps(config, indent=4))
                                    await client.add_reaction(message, "\N{WHITE HEAVY CHECK MARK}")
                                await client.delete_message(demande)
                            else : client.send_message(message.channel, "Je n'ai pas ce paramètre dans ma liste.")

                    elif args[0] == "set" :
                        if len(args) < 3 :
                            await client.send_message(message.channel, "Usage : `"+p+"config set <paramètre> <valeur>`.")
                            return
                        if not args[1] in config :
                            await client.send_message(message.channel, "Je n'ai pas ce paramètre dans ma liste.")
                            return
                        valeur = " ".join(args[2:])
                        paramType = configInfos[args[1]][0]
                        if paramType == "int" or paramType == "percent" :
                            try : valeur = int(valeur)
                            except ValueError :
                                await client.send_message(message.channel, "Ce paramètre attend un nombre entier.")
                                return
                            if configInfos[args[1]][0] == "percent" :
                                if not 0 <= valeur <= 100 :
                                    await client.send_message(message.channel, "Ce paramètre attend un nombre entre 0 et 100.")
                                    return
                        elif paramType == "role":
                            if len(message.role_mentions) != 1 :
                                await client.send_message(message.channel, "Ce paramètre attend un rôle.")
                                return
                            valeur = message.role_mentions[0].id
                        elif paramType == "channel":
                            if len(message.channel_mentions) != 1 :
                                await client.send_message(message.channel, "Ce paramètre attend un salon.")
                                return
                            valeur = message.channel_mentions[0].id
                        elif paramType == "color":
                            valeur = valeur.lower()
                            if not re.fullmatch("#[0-9a-f]{6}", valeur) :
                                await client.send_message(message.channel, "Ce paramètre attend une couleur sous la forme `#ffffff`.")
                                return
                        with open("config.json", "r") as f : config = json.loads(f.read())
                        config[message.server.id][args[1]] = valeur
                        with open("config.json", "w") as f : f.write(json.dumps(config, indent=4))
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                    else : await client.send_message(message.channel,  "Usage : `"+p+"config [list|show|reset|set] [paramètre] [valeur]`")

            elif cmd == "friend" :
                if len(message.mentions) != 2 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    prct = (int(message.mentions[0].id[3:6]) + int(message.mentions[1].id[3:6])) % 1000 / 10
                    await client.send_message(message.channel, "\N{SLIGHTLY SMILING FACE} Il y'a **"+str(prct)+" %** d'amitié entre **"+message.mentions[0].name+"** et **"+message.mentions[1].name+"** \N{SLIGHTLY SMILING FACE}")

            elif cmd == "love" :
                if len(message.mentions) != 2 : await client.send_message(message.channel, usage(p, cmd))
                else :
                    prct = (int(message.mentions[0].id[8:11]) + int(message.mentions[1].id[8:11])) % 1000 / 10
                    await client.send_message(message.channel, "\N{HEAVY BLACK HEART} Il y'a **"+str(prct)+" %** d'amour entre **"+message.mentions[0].name+"** et **"+message.mentions[1].name+"** \N{HEAVY BLACK HEART}")

            elif cmd == "ljdc" :
                source = unescape(urlopen("https://lesjoiesducode.fr/").read().decode("utf-8"))
                soup = BeautifulSoup(source, "html.parser")
                randomUrl = re.search('href="([^"]+)"', str(soup.find("i", {"class": "fas fa-random"}).parent)).group(1)
                source = unescape(urlopen(randomUrl).read().decode("utf-8"))
                soup = BeautifulSoup(source, "html.parser")
                commentaire = soup.find("h1", {"class": "blog-post-title"}).string
                fileUrl = re.search('<img[^>]*src="([^"]+)"/>', str(soup.find("div", {"class": "blog-post-content"}))).group(1)
                em = discord.Embed(title="les_joies_du_code();", description=commentaire, colour=0x00ff00)
                em.set_image(url=fileUrl)
                await client.send_message(message.channel, embed=em)

            elif cmd == "p4":
                if len(args) == 1 and args[0] == "v2" : v2 = True
                else : v2 = False
                jetonJaune = str(discord.utils.get(client.get_all_emojis(), name="p4jaune"))
                jetonRouge = str(discord.utils.get(client.get_all_emojis(), name="p4rouge"))
                numbers = [str(i+1)+"\N{COMBINING ENCLOSING KEYCAP}" for i in range(7)]
                interface = await client.send_message(message.channel, "Qui veut jouer avec "+message.author.mention+" clique sur la réaction \N{HAPPY PERSON RAISING ONE HAND} !")
                await client.add_reaction(interface, "\N{HAPPY PERSON RAISING ONE HAND}")
                res = await client.wait_for_reaction("\N{HAPPY PERSON RAISING ONE HAND}", timeout=60, message=interface)
                while res != None and res.user == client.user : res = await client.wait_for_reaction("\N{HAPPY PERSON RAISING ONE HAND}", timeout=60, message=interface)
                await client.clear_reactions(interface)
                if res == None :
                    await client.edit_message(interface, "Personne veut jouer avec toi "+message.author.mention+" \N{DISAPPOINTED BUT RELIEVED FACE}")
                    return
                joueurs = [res.user, message.author]
                grille = [['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', '']]
                joueur = joueurs[0]
                couleur = "J"
                txt = "Voici les règles du jeu :\n- Vous jouez chacun votre tour en posant un jeton dans une colonne.\n- Le gagnant est celui qui aligne 4 jetons de sa couleur verticalement, horizontalement ou en diagonale.\n- Vous choisissez la colonne où vous jouez avec les réactions numéros."
                if v2 : txt += "\n- Vous pouvez utiliser la récation \N{FISTED HAND SIGN} pour éjecter le jeton le plus bas d'une colonne au lieu d'en poser un nouveau."
                txt += "\n\nLe jeux commencera quand les deux joueurs auront réagis avec \N{WHITE HEAVY CHECK MARK}.\nBon jeu !"
                await client.edit_message(interface, txt)
                await client.add_reaction(interface, "\N{WHITE HEAVY CHECK MARK}")  
                agreed = []
                while not (joueurs[0] in agreed and joueurs[1] in agreed) :
                    res = await client.wait_for_reaction("\N{WHITE HEAVY CHECK MARK}", timeout=120, message=interface)
                    if res == None :
                        await client.edit_message(interface, "Bon bah la partie est annulée si personne n'accepte les règles \N{CONFUSED FACE}")
                        return
                    agreed.append(res.user)
                await client.edit_message(interface, "Chargement en cours...")
                await client.clear_reactions(interface)
                if v2 : await client.add_reaction(interface, "\N{FISTED HAND SIGN}")
                for n in numbers : await client.add_reaction(interface, n)
                warn = ""
                while not p4Winner(grille) and "" in flatten(grille) :
                    txt = "À toi de jouer "+joueur.mention
                    if couleur == "J" : txt += " (jeton "+jetonJaune+")"
                    else : txt += "(jeton "+jetonRouge+")"
                    txt += "\n\n"+p4Affichage(grille)
                    if warn != "" : txt += "\n"+warn
                    await client.edit_message(interface, txt)
                    warn = ""
                    if v2 : res = await client.wait_for_reaction(numbers+["\N{FISTED HAND SIGN}"], user=joueur, timeout=120, message=interface)
                    else : res = await client.wait_for_reaction(numbers, user=joueur, timeout=120, message=interface)
                    if res == None : break
                    else :
                        removeReac = False
                        try :
                            await client.remove_reaction(interface, res.reaction.emoji, res.user)
                            removeReac = True
                        except discord.errors.Forbidden :
                            removeReac = False
                            await client.send_message(message.channel, "Je n'ai pas le droit de supprimer vos réactions il va donc falloir que vous enleviez et remettez vos réactions à chaque tour (et puis c'est de la faute de celui qui fait les perms de ce serv, pas la mienne).")
                        if str(res.reaction.emoji) == "\N{FISTED HAND SIGN}" and v2 :
                            await client.edit_message(interface, txt+"\n Utilise les numéros pour choisir la colonne où tu veux éjecter un pion.")
                            res = await client.wait_for_reaction(numbers, user=joueur, timeout=60, message=interface)
                            if res == None : break
                            else :
                                if removeReac : await client.remove_reaction(interface, res.reaction.emoji, res.user)
                                n = numbers.index(str(res.reaction.emoji))
                                if grille[5][n] == "" : warn = "Cette colonne est vide \N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} (reclique sur \N{FISTED HAND SIGN} si tu veux toujours éjecter un pion)"
                                else :
                                    for y in reversed(range(1,6)):
                                        grille[y][n] = grille[y-1][n]
                                        if couleur == "J" :
                                            couleur = "R"
                                            joueur = joueurs[1]
                                        else :
                                            couleur = "J"
                                            joueur = joueurs[0]
                        else :
                            n = numbers.index(str(res.reaction.emoji))
                            if grille[0][n] != "" : warn =  "C'est plus pratique de mettre un pion dans une colonne où il reste de la place..."
                            else :
                                y = 0
                                while y < len(grille) and grille[y][n] == "" : y += 1
                                grille[y-1][n] = couleur
                                if couleur == "J" :
                                    couleur = "R"
                                    joueur = joueurs[1]
                                else :
                                    couleur = "J"
                                    joueur = joueurs[0]
                await client.delete_message(interface)
                await client.send_message(message.channel, p4Affichage(grille))
                if p4Winner(grille) == "J" : await client.send_message(message.channel, "Bravo "+joueurs[0].mention+" tu as battu "+joueurs[1].mention+" !")
                elif p4Winner(grille) == "R" : await client.send_message(message.channel, "Bravo "+joueurs[1].mention+" tu as battu "+joueurs[0].mention+" !")
                elif "" in flatten(grille) : await client.send_message(message.channel, "Personne m'a répondu pendant 2 minutes alors j'ai annulé la partie \N{CONFUSED FACE}")
                else : await client.send_message(message.channel, "Grille complète et match nul...")

            elif cmd == "invite" : await client.send_message(message.channel, "Invitez moi sur votre serveur : https://discordapp.com/oauth2/authorize?client_id=380775694411497493&scope=bot&permissions=271969344\net visitez mon serveur principal : https://discord.gg/MwMpRha")

            elif cmd == "findinpi" or cmd in alias["findinpi"] :
                if len(arg) == 0 : await client.send_message(message.channel, usage(p, cmd))
                else : 
                    try :
                        n = int(arg)
                        n = arg
                    except ValueError :
                        nchars = len(arg)
                        n = 0
                        for i in range(nchars) : n += ord(arg[i]) << 8*(nchars-i-1)
                        n = str(n)
                        await client.send_message(message.channel, "Ton argument ressemblant d'avantage à un texte qu'à un nombre je me suis permis de le convertir en utilisant la table ASCII.")

                    loader = await client.send_message(message.channel, "Chargement en cours...")
                    myStream = io.open('pi-billion.txt', "r", encoding="utf-8")
                    oldEndMatch = ""
                    lastTest = ""
                    curseur = 0
                    positionA = -1
                    bufferring = 2000000
                    piSize = 1000000000
                    for i in range(piSize//bufferring) :
                        if (curseur+bufferring)%(piSize//5) == 0 : await client.edit_message(loader, "Recherche dans les "+joliStr(curseur+bufferring)+" premières décimales de pi.")
                        myStream.seek(curseur+2)
                        test = myStream.read(bufferring)
                        if test.startswith(n[len(oldEndMatch):]) :
                            positionA = curseur - len(oldEndMatch)
                            pattern = lastTest[bufferring-len(oldEndMatch)-10:bufferring-len(oldEndMatch)]+"__"+n+"__"+test[len(n)-len(oldEndMatch):len(n)-len(oldEndMatch)+10]
                            break
                        elif test.find(n) != -1 :
                            positionA = test.find(n)+curseur
                            positionR = test.find(n)
                            if positionR < 10 :
                                pattern = lastTest[positionR-10:]+test[:positionR]+"__"+n+"__"+test[positionR+len(n):positionR+len(n)+10]
                            elif positionR+len(n)+10 > bufferring :
                                if curseur == piSize : pattern = test[positionR-10:positionR]+"__"+n+"__"+test[positionR+len(n):]
                                else :
                                    myStream.seek(curseur+bufferring+2)
                                    nextTest = myStream.read(bufferring)
                                    pattern = test[positionR-10:positionR]+"__"+n+"__"+test[positionR+len(n):]+nextTest[(positionR+len(n)+10)%bufferring:]
                            else :
                                pattern = test[positionR-10:positionR]+"__"+n+"__"+test[positionR+len(n):positionR+len(n)+10]
                            break
                        oldEndMatch = ""
                        for i in range(len(n)) :
                            if test.endswith(n[:i]) : oldEndMatch = n[:i]
                        curseur += bufferring
                        lastTest = test

                    await client.delete_message(loader)
                    if positionA == -1 :
                        try : await client.send_message(message.channel, n+" n'a pas été trouvé dans les 1 000 000 000 premières décimales de pi.")
                        except discord.errors.HTTPException : await client.send_message(message.channel, "Je n'ai pas trouvé ton nombre mais je ne vais pas pouvoir l'afficher car il est un peu trop long...")
                    elif positionA == 0 : await client.send_message(message.channel, "C'est ainsi que commence le nombre pi ^^")
                    else :
                        try : await client.send_message(message.channel, n+" a été trouvé à la "+joliStr(positionA+1)+" ème décimale de pi ("+pattern+").")
                        except discord.errors.HTTPException : await client.send_message(message.channel, "Ton nombre a bien été trouvé à la "+joliStr(positionA+1)+" ème décimales de pi mais il est trop long pour que je l'affiche.")

            elif cmd == "pi2image" or cmd in alias["pi2image"] :
                try : 
                    if len(args) == 2 :
                        width = int(args[0])
                        height = int(args[1])
                        begining = 0
                    elif len(args) == 3 :
                        width = int(args[0])
                        height = int(args[1])
                        begining = int(args[2])
                    else :
                        raise ValueError
                except ValueError :
                    await client.send_message(message.channel, usage(p, cmd))
                    return
                if width*height > 2073600 :
                    await client.send_message(message.channel, "Pour éviter de me faire calculer pendant des heures, l'image est limitée à 2 073 600 pixels (la taille d'un écran d'ordinateur classique).")
                    return
                elif width*height <= 0 :
                    await client.send_message(message.channel, "Ouais alors la taille doit quand même être supéreure à zéro \N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT}")
                    return
                elif min(width, height) < 10 :
                    await client.send_message(message.channel, "La largeur et la hauteur doivent être supérieures à 10 pixels.")
                    return
                elif begining < 0 :
                    await client.send_message(message.channel, "Arrête d'essayer de me faire crasher t'es méchant \N{TIRED FACE}")
                    return

                await client.add_reaction(message, "\N{TIMER CLOCK}")
                myStream = io.open('pi-billion.txt', "r", encoding="utf-8")

                try : myStream.seek(begining+2)
                except OSError :
                    await client.send_message(message.channel, "Je ne connais *que* le premier miliard de décimales de pi.")
                    return                    

                decimals = myStream.read(width*height*3)

                pimg =  open ("pi.ppm", 'wb')
                pimg.write(bytes("P6\n"+str(width)+" "+str(height)+" 9\n", 'ascii'))
                for i in decimals :
                    pimg.write(bytes([int(i)*255//9]))
                if len(decimals) < width*height*3 :
                    await client.send_message(message.channel, "Je ne connais *que* le premier miliard de décimales de pi alors je complètes avec des pixels noirs.")
                    for _ in range(width*height*3 - len(decimals)) :
                        pimg.write(bytes([0]))
                del decimals
                pimg.close()

                im = Image.open("pi.ppm")
                im.save("pi.png")
                im.close()

                if begining == 0 : txt = "première"
                else : txt = joliStr(begining)+" ème"
                await client.send_file(message.channel, "pi.png", content="Voici une image de "+str(width)+"x"+str(height)+" avec les décimales de pi de la "+txt+" à la "+joliStr(begining + width*height*3)+" ème.")
                await client.remove_reaction(message, "\N{TIMER CLOCK}", client.user)






            # ^ nouvelles commandes ici ^

            elif len(msg) > 2 and msg[0] == p : await client.add_reaction(message, u"\N{UPSIDE-DOWN FACE}")
                
        except Exception :
            txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n')
            txt += "erreur sur le serv **" + message.server.name + "** suite à un message de **" + message.author.name + "** (`" + message.content.replace("```", "\`\`\`") + "`).\nVoici le détail :```Python\n"
            txt += format_exc() + "```\n\n"
            with open("log/erreurs.txt","a") as f : f.write(txt)
            while len(txt) > 2000 :
                await client.send_message(ribt, txt[:2000])
                txt = txt[2000:]
            if txt != "" : await client.send_message(ribt, txt)
            await client.send_message(message.channel, "Une erreur inatendue s'est produite, désolé de la gêne occasionnée \N{CONFUSED FACE}")

                

    #client.loop.create_task(actu())
    client.run(secret["discord-token"])
except Exception :
    txt = "\n\n##########[ERREUR FATALE]##########\n" + time.strftime('[%d/%m/%Y %H:%M:%S]') + format_exc() + "\n\n"
    with open("log/erreurs.txt","a") as f : f.write(txt)
    time.sleep(60*10)
    with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + " Tux va tenter de redémarrer\n")
popen("./restart-tux.sh")
