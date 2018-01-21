import discord
import asyncio
import time
from calendar import timegm
import random
from traceback import format_exc
from re import search
import wikipedia
from urllib.request import urlopen
import json
from html import unescape
from os import popen
import feedparser
import codecs

fast = """```  ______        _   
 |  ____|      | |  
 | |__ __ _ ___| |_ 
 |  __/ _` / __| __|
 | | | (_| \__ \ |_ 
 |_|  \__,_|___/\__|```
 """

aide_fast = fast +  u"""**Fast** est un jeu où vous devez retaper la chaîne de caractères choisie par le bot le plus rapidement possible. Faites `!fast <niveau>` pour déclancher le début du jeu.
__Niveau **1**__ : 10 à 20 caractères minuscules
__Niveau **2**__ : 10 à 20 caractères minuscules ou majuscules
__Niveau **3**__ : 10 à 20 caractères minuscules (avec ou sans accent), majuscules ou numériques
__Niveau **4**__ : 10 à 20 caractères minuscules (avec ou sans accent), majuscules, numériques ou spéciaux
__Niveau **5**__ : 20 à 30 caractères minuscules (avec ou sans accent), majuscules, numériques ou spéciaux
Bon courage \N{SMILING FACE WITH HORNS}"""

commandes = {"blague": "`!blague` pour avoir une blague au hasard parmis celles que je connais et `!blague add <Votre blague.>` pour m'en apprendre une nouvelle (mettre un `|` pour que je fasse une pause au moment de raconter votre blague)",
             "citation": "`!citation` pour avoir une citation au hasard parmis celles que je connais et `!citation add <Votre citation.>` pour m'en apprendre une nouvelle",
             "date": "la date d'aujourd'hui, tout simplement ^^",
             "devine": "un super jeu ! (je choisis un nombre entre 0 et 100 et tu dois le deviner)",
             "fast": aide_fast,
             "gif": "`!gif <recherche>` pour chercher un GIF (une recherche vide donne un GIF aléatoire)",
             "help": "la liste des commandes (`!help <comande>` pour avoir toutes les infos sur une commande)",
             "heure": "l'heure, tout simplement ^^",
             "langage": "`!langage <list|add|remove> [langage]` pour vous ajouter, supprimer ou lister tous les langages disponibles comme rôle",
             "meteo": "`!meteo <ville> <jours>` pour avoir les prévisions météo de la ville pendant un certain nombre de jour (un nombre entre 1 et 7)",
             "ping": "tester la vitesse connection avec le bot",
             "proverbe": "`!proverbe` pour avoir un proverbe au hasard parmis ceux que je connais et `!proverbe add <Votre proverbe.>` pour m'en apprendre un nouveau",
             "r2d": "`!r2d <nombre en chiffres romains>` pour convertir un nombre en chiffres romains en un nombre en chiffres décimaux",
             "roll": "un nombre (pseudo-)aléatoire entre 0 et 100",
             "rot13": "`!rot13 <texte>` pour chiffrer/déchiffrer un message en rot13",
             "rpi": "quelques infos sur la Raspberry Pi qui m'héberge",
             "rug": "Random User Generator, une identité aléatoire",
             "ud": "`!ud <mot>` pour chercher la définition d'un mot sur Urban Dictionnary (en anglais)",
             "whois": "`!whois <nom de domaine>` pour avoir queqlues infos sur un nom de domaine",
             "wiki": "`!wiki <recherche>` pour effectuer une recherche sur Wikipédia et avoir la première phrase de l'article"}

caracteres = ['abcdefghijklmnopqrstuvwxyz',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZaàbcçdeêëéèfghijklmnopqrstuùvwxyz0123456789',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZaàbcçdeêëéèfghijklmnopqrstuùvwxyz0123456789&"#\'{([-|_\\)]°+=}$*?,.;/:!']

feeds = ["https://news.google.com/news/rss/headlines/section/topic/SCITECH.fr_fr/Science%2FHigh-Tech?ned=fr&hl=fr",
         "http://www.commitstrip.com/fr/feed/",
         "https://korben.info/feed",
         "https://www.begeek.fr/feed",
         "http://blogmotion.fr/feed",
         "http://www.framboise314.fr/feed/", "http://www.journaldugeek.com/feed/",
         "https://thehackernews.com/feeds/posts/default",
         "https://usbeketrica.com/rss",
         "https://www.lemondeinformatique.fr/flux-rss/"]

with open("wordlist/courants.txt", "r") as f : mots = f.read().split("\n")
with open("secret.json", "r") as f : secret = json.loads(f.read())

pendu = ["""```
                       
                        
                        
                         
                          
                          
                         
                        
         
        ============```""", """```
            
           ||          
           ||          
           ||          
           ||         
           ||         
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||        
           ||        
           ||       
           ||       
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      
           || /       
           ||/       
           ||       
           ||       
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        
           ||        
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        O
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        O/
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||          \
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||        / \
           ||
           ||
           ||
        ============```"""]


          

chaine, nbr, coups, ancienmsg, loader, PartieP, mot, aff, vies = {},{},{},{},{},{},{},{},{}
tmp = log = None

client = discord.Client()
        
@client.event
async def on_ready():
    try :
        global log
        log = time.strftime("log/%Y%m%d", time.localtime())
        with open(log,"a") as f : f.write(time.strftime('\n\n***[%H:%M:%S]', time.localtime()) + ' Connecté en tant que ' + client.user.name + ' (id : ' + client.user.id + ')\n')
        await client.change_status(game=discord.Game(name='jouer avec vous'))
    except:
        txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n', time.localtime()) + format_exc() + "\n\n"
        with open("log/erreurs.txt","a") as f : f.write(txt)

@client.event
async def on_message(message):
    try:
        global log, tmp, ancienmsg, loader, chaine, nbr, coups, vies, mot, aff
        
        t = timegm(message.timestamp.timetuple())
        msg = message.content
        serv = message.server.id
        txt = time.strftime('\n[%H:%M:%S] #', time.localtime(t)) + str(message.channel) + ' ' + str(message.author) + ' : ' + msg
        if log != time.strftime("log/%Y%m%d", time.localtime()): log = time.strftime("log/%Y%m%d", time.localtime())
        with open(log,"a") as f : f.write(txt)
        #print (message.author.name)

        if search(r"(?i)^ah?\W*$", msg) :
            await client.send_message(message.channel, 'tchoum')

        if search(r"(?i)^[kq]u?oi?\W*$", msg) :
            await client.send_message(message.channel, 'ffeur')

        elif search(r"(?i)^lol\W*$", msg) :
            await client.send_message(message.channel, 'ita')

        if msg == "!debug" :
            print ("===[VARIABLES]===")
            for i in globals().keys():
                if i != "mots" and i != "pendu" and i != "fast" and i != "aide_fast" and i != "commandes" and i != "caracteres" and i != "feeds" :
                    try : print (i + " : " + str(globals()[i]) + "\n")
                    except UnicodeEncodeError : print ('### erreur encodage avec ' + str(i))
            print ("=================")
        
        if msg == "" : pass

        elif msg == '!ping':
            tmp = time.time() * 1000 - t * 1000
            await client.send_message(message.channel, 'Pong ! ('+str(round(tmp,1))+' ms)')

        elif msg == "Recherche d'un GIF..." and message.author.id == client.user.id :
            loader[serv] = message

        elif msg == '!help':
            txt = "__Liste des commandes disponibles :__\n\n(faire `!help <commande>` pour avoir toutes les infos sur une comande)\n\n"
            for commande in commandes.keys() : txt += "- `!" + commande + "`\n"
            txt += "\n**Cette liste est en constante évoluton : n'hésitez pas à revenir la consulter régulièrement !**"
            if message.channel.name == "spam-bot" : await client.send_message(message.channel, txt)
            else :
                await client.send_message(message.author, txt)
                await client.send_message(message.channel, "Check tes MP " + "<@" + message.author.id + "> \N{WINKING FACE}")

        elif msg.startswith("!help ") :
            commande = msg[6:]
            if commande in commandes :
                await client.send_message(message.channel, "__Description de la commande `!" + commande + "` :__\n" + commandes[commande])
            else :
                await client.send_message(message.channel, "Elle existe pas cette commande là ^^")

        elif msg == '!roll' :
            await client.send_message(message.channel, str(random.randint(0, 100)))

        elif msg == '!heure' :
            await client.send_message(message.channel, time.strftime('Il est %H:%M passé de %S secondes.', time.localtime()))

        elif msg == '!date':
            await client.send_message(message.channel, time.strftime('Nous sommes le %d/%m/%Y.', time.localtime()))

        elif msg == '!blague':
            f = open("blagues.txt", "r")
            c = f.read().split('\n')
            f.close()
            blague = random.choice(c).split('|')
            while blague == [""] or blague == tmp : blague = random.choice(c).split('|')
            tmp = blague
            for txt in blague :
                await client.send_message(message.channel, txt)
                time.sleep(3)               

        elif msg.startswith('!blague add '):
            blague = msg.replace('!blague add ', '')
            f = open("blagues.txt", "r")
            c = f.read().split('\n')
            f.close()
            if blague in c : await client.send_message(message.channel, '<@' + message.author.id + '> Je connais déjà cette blague.')
            else :
                f = open("blagues.txt", "a")
                f.write('\n' + blague)
                f.close()
                await client.send_message(message.channel, 'OK <@' + message.author.id + '>')

        elif msg == '!proverbe':
            f = open("proverbes.txt", "r")
            c = f.read().split('\n')
            f.close()
            proverbe = random.choice(c)
            while proverbe == "" or proverbe == tmp : proverbe = random.choice(c)
            tmp = proverbe
            await client.send_message(message.channel, proverbe)

        elif msg.startswith('!proverbe add '):
            proverbe = msg.replace('!proverbe add ', '')
            f = open("proverbes.txt", "r")
            c = f.read().split('\n')
            f.close()
            if proverbe in c : await client.send_message(message.channel, '<@' + message.author.id + '> Je connais déjà ce proverbe.')
            else :
                f = open("proverbes.txt", "a")
                f.write('\n' + proverbe)
                f.close()
                await client.send_message(message.channel, 'OK <@' + message.author.id + '>')

        elif msg == '!citation':
            f = open("citations.txt", "r")
            c = f.read().split('\n')
            f.close()
            citation = random.choice(c)
            while citation == "" or citation == tmp : citation = random.choice(c)
            tmp = citation
            await client.send_message(message.channel, citation)

        elif msg.startswith('!citation add '):
            citation = msg.replace('!citation add ', '')
            f = open("citations.txt", "r")
            c = f.read().split('\n')
            f.close()
            if citation in c : await client.send_message(message.channel, '<@' + message.author.id + '> Je connais déjà cette citation.')
            else :
                f = open("citations.txt", "a")
                f.write('\n' + citation)
                f.close()
                await client.send_message(message.channel, 'OK <@' + message.author.id + '>')

        elif  msg.startswith('!wiki'):
            if len(msg) < 7 :
                await client.send_message(message.channel, "Usage : `!wiki <recherche>`.")
            else :
                req = msg[6:len(msg)]
                wikipedia.set_lang("fr")
                try : await client.send_message(message.channel, wikipedia.summary(req, sentences=1))
                except wikipedia.exceptions.DisambiguationError as e:
                    i = 0
                    txt = "J'hésite entre "
                    while i < len(e.options)-2 :
                        txt += e.options[i] + ", "
                        i += 1
                    txt += e.options[-2] + " et " + e.options[-1] + "..."
                    await client.send_message(message.channel, txt)
                except wikipedia.exceptions.PageError : await client.send_message(message.channel, "Impossible de trouver quoi que ce soit avec cette recherche...")
      
        elif msg.startswith('!fast'):
            if serv in chaine :
                tmp = ""
                for i in chaine[serv] : tmp += i + " "
                await client.send_message(message.channel, "Une partie est déja en cours avec la chaîne `" + tmp[:-1] + "`...")
            elif len(msg) != 7 :
                await client.send_message(message.channel, "Usage : `!fast <niveau>`. Faire `!help fast`pour plus de détails.")
            else :
                try : niveau = int(msg[6])
                except ValueError: await client.send_message(message.channel, "Usage : `!fast <niveau>`. Faire `!help fast`pour plus de détails.")
                else :
                    if not(1 <= niveau <= 5) : await client.send_message(message.channel, "Usage : `!fast <niveau>`. Faire `!help fast`pour plus de détails.")
                    else :             
                        chaine[serv] = ''
                        if niveau == 5:
                            choix = caracteres[3]
                            l = random.randint(20, 30)
                        else :
                            choix = caracteres[niveau - 1]
                            l = random.randint(10, 20)
                        i = 0
                        while i < l:
                            chaine[serv] += random.choice(choix)
                            i += 1
                        tmp = ""
                        for i in chaine[serv] : tmp += i + " "
                        await client.send_message(message.channel, fast + "Chaine à recopier : " + tmp[:-1] + "\n\n Les espaces c'est juste pour éviter le copier-coller ;-)")
        elif serv in chaine and msg == chaine[serv] :
            del(chaine[serv])
            await client.send_message(message.channel, 'Gagné <@' + message.author.id + '> !!!')

        elif msg.startswith('!r2d') :
            if len(msg) < 6: await client.send_message(message.channel, "Usage : `!r2d <nombre en chiffres romains>`.")
            else :
                r = msg.replace('!r2d ', '')
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


        elif msg == "!cnf" :
            fact = urlopen("https://www.chucknorrisfacts.fr/api/get?data=tri:alea;nb:1")
            fact = unescape(fact.read().decode("utf-8"))
            fact = json.loads(fact)[0]['fact']
            await client.send_message(message.channel, fact)

        elif msg == "!ud" : await client.send_message(message.channel, "Usage : `!ud <mot>` (`!help ud` pour plus de détails)")

        elif msg.startswith("!ud ") :
            url = msg.replace("!ud ", "http://api.urbandictionary.com/v0/define?term=")
            definition = urlopen(url)
            definition = unescape(definition.read().decode("utf-8"))
            definition = json.loads(definition)
            if definition['result_type'] == 'no_results' : await client.send_message(message.channel, 'Aucun résultat...')
            else : await client.send_message(message.channel, definition['list'][0]['definition'])

        elif msg == "!rug" :
            data = urlopen("https://randomuser.me/api/?nat=fr")
            data = unescape(data.read().decode("utf-8"))
            data = json.loads(data)['results'][0]
            txt = ""
            txt += "Tu t'appelles " + data['name']['first'].capitalize() + " " + data['name']['last'].capitalize() + ". "
            txt += "Ton adresse mail est " + data['email'].replace("example.com", random.choice(["gmail.com","yahoo.com","neuf.fr","laposte.net","orange.fr","ovh.net",])) + ". "
            jour, heure = data['dob'].split(" ")
            jour = jour.split("-")
            jour = jour[2] + "/" + jour[1] + "/" + jour[0]
            txt += "Tu es né le " + jour + " à " + heure + ". "
            txt += "Ton numéro de téléphone est le " + data['phone'].replace("-", " ") + ". "
            loc = data['location']
            txt += "Tu habites au " + loc['street'] + " à " + loc['city'].title() + ". "
            txt += "Ton pseudo est " + data['login']['username'] + " et ton mot de passe est `" + data['login']['password'] + "`."
            await client.send_message(message.channel, txt)

        elif msg == "!rpi" :
            txt = ""
            txt += popen("vcgencmd measure_temp").read()
            txt += popen("vcgencmd get_mem arm").read()
            txt += popen("vcgencmd get_mem gpu").read()
            txt += popen("vcgencmd measure_volts").read()
            txt += "freespace=" + popen("df -h /").read().split("\n")[1].split()[3] + "\n"
            txt += "localip=" + popen("ifconfig | grep -Eo 'inet adr:([0-9]*\.){3}[0-9]*'").read().split("\n")[0].replace("inet adr:", "") + "\n"
            txt += "host=" + popen("hostname").read()
            await client.send_message(message.channel, txt)

        elif msg.startswith("!gif") :            
            if len(msg) == 4 :
                await client.send_message(message.channel, "Recherche d'un GIF...")
                url = "http://api.giphy.com/v1/gifs/random?api_key=" + secret["giphy-key"]
                gif = urlopen(url)
                gif = unescape(gif.read().decode("utf-8"))
                gif = json.loads(gif)['data']
                if serv in loader : await client.edit_message(loader[serv], "Téléchargement du GIF...")
                with open("/home/pi/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['image_url']).read())
                #name = search(r"^http://giphy.com/gifs/(.+)-\w+$", gif['data']['url']).groups(1)
                if serv in loader : await client.edit_message(loader[serv], "Upload du GIF...")
                await client.send_file(message.channel, "tmp.gif", filename="random.gif")
                if serv in loader :
                    await client.delete_message(loader[serv])
                    del(loader[serv])
            
            else :
                await client.send_message(message.channel, "Recherche d'un GIF...")
                req = msg[5:]
                url = "http://api.giphy.com/v1/gifs/search?api_key="+ secret["giphy-key"] + "&lang=fr&limit=1&q=" + req
                gif = urlopen(url)
                gif = unescape(gif.read().decode("utf-8"))
                gif = json.loads(gif)['data'][0]
                if serv in loader : await client.edit_message(loader[serv], "Téléchargement du GIF...")
                with open("/home/pi/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['images']['original']['url']).read())
                if serv in loader : await client.edit_message(loader[serv], "Upload du GIF...")
                await client.send_file(message.channel, "tmp.gif", filename=gif['title'].replace(" ", "_")+".gif")
                if serv in loader :
                    await client.delete_message(loader[serv])
                    del(loader[serv])

        elif msg == "!devine" :
            if message.channel.name != "spam-bot" :
                await client.send_message(message.channel, "On va pas jouer ici alors qu'il y'a un salon qui s'appelle spam-bot !")
            else :
                if serv in nbr :
                    await client.send_message(message.channel, "Une partie est déja en cours...")
                else :
                    coups[serv] = {}
                    nbr[serv] = random.randint(0, 100)
                    debug()
                    await client.send_message(message.channel, "C'est parti mon kiki !")
        elif serv in nbr and message.channel.name == "spam-bot" :
            try : proposition = int(msg)
            except ValueError : pass
            else :
                if message.author.id in coups[serv] : coups[serv][message.author.id] += 1
                else : coups[serv][message.author.id] = 1
                if proposition == nbr[serv] :
                    del(nbr[serv])
                    await client.send_message(message.channel, 'Gagné en ' + str(coups[serv][message.author.id]) + ' coups <@' + message.author.id + '> !')
                elif nbr[serv] < proposition :
                    await client.send_message(message.channel, "C'est moins que " + str(proposition))
                else :
                    await client.send_message(message.channel, "C'est plus que " + str(proposition))

        elif msg.startswith("!meteo") :
            try :
                ville, jours = msg.replace("!meteo ", "").split(" ")
                jours = int(jours)
            except ValueError :
                await client.send_message(message.channel, "Usage : !meteo <ville> <jours>")
            else :
                if not(1 <= jours <= 7) : await client.send_message(message.channel, "<jours> doit être un nombre entre 1 et 7")
                else :
                    try : data = feedparser.parse("http://api.meteorologic.net/forecarss?p=" + ville)['entries'][0]['summary']
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

        elif msg.startswith("!rot13 ") :
            await client.send_message(message.channel, codecs.encode(msg[7:], 'rot_13'))

        elif msg == "!whois" : await client.send_message(message.channel, "Usage : `!whois <nom de domaine>` (`!help whois` pour plus de détails)")

        elif msg.startswith("!whois ") :
            dn = msg[7:]
            data = urlopen("https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=" + secret["whois-key"] + "&outputFormat=JSON&domainName=" + dn)
            data = unescape(data.read().decode("utf-8"))
            try : data = json.loads(data)['WhoisRecord']['registryData']['administrativeContact']['rawText'].split("\n")
            except KeyError : await client.send_message(message.channel, 'nom de domaine inconnu...')
            else :
                txt = tmp = ""
                i = 0
                while len(tmp) <= 400 and i < len(data):
                    txt = tmp
                    tmp += data[i] + "\n"
                    i += 1
                await client.send_message(message.channel, txt)

        elif msg == "!pi" : await client.send_message(message.channel, "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160")

        elif msg == "!pendu" :
            if message.channel.name != "spam-bot" :
                await client.send_message(message.channel, "On va quand même pas jouer ici alors qu'il y'a un salon qui s'appelle spam-bot !")
            else :
                if serv in mot : await client.send_message(message.channel, "Une partie est déjà en cours (" + aff[serv] + ")...")
                else :
                    vies[serv] = len(pendu)
                    mot[serv] = random.choice(mots)
                    aff[serv] = ["_"]*len(mot[serv])
                    await client.send_message(message.channel, "C'est parti ! (N'oubliez pas que je compte les accents et les cédilles ^_^)")
                    await client.send_message(message.channel, " ".join(aff[serv]).replace("_", r"\_"))
                    
        elif message.channel.name == "spam-bot" and serv in mot and len(msg) == 1:
            lettre = msg.lower()
            if lettre in mot[serv] :
                i = 0
                while i < len(mot[serv]) :
                    if mot[serv][i] == lettre : aff[serv][i] = lettre
                    i += 1
                if not "_" in aff[serv] :
                    del(mot[serv])
                    await client.send_message(message.channel, "Gagné ^^")
            else :
                await client.send_message(message.channel, pendu[-vies[serv]])
                vies[serv] -= 1
                if vies[serv] == 0 :
                    await client.send_message(message.channel, "PERDU !!! (le mot était... " + mot[serv] + " !)")
                    del(mot[serv])
            
            if serv in mot : await client.send_message(message.channel, " ".join(aff[serv]).replace("_", r"\_"))
        
        elif msg.startswith("!langage") :
            args = msg.split(" ")[1:]
            if len(args) < 1 or len(args) > 2 : await client.send_message(message.channel, "Usage : `!langage <list|add|remove> [langage]` (`!help langage` pour plus de détails)")
            elif args[0] == "list" :
                txt = "__Liste des rôles disponibles :__\n\n"
                for i in message.server.roles :
                    if str(i.colour) == "#ffffff" : txt += "- **" + i.name + "**\n"
                txt += "\n(si vous parlez un langage qui n'est pas mentionné ici vous pouvez le proposer dans <#" + discord.utils.get(message.server.channels, name='suggestions').id + "> \N{WINKING FACE})"
                await client.send_message(message.channel, txt)
                    
            elif args[0] == "add" :
                role = discord.utils.get(message.server.roles, name=args[1])
                if role == None : await client.send_message(message.channel, "Ce rôle n'existe pas encore mais vous pouvez le proposer dans <#" + discord.utils.get(message.server.channels, name='suggestions').id + "> \N{WINKING FACE}")
                elif str(role.colour) != "#ffffff" : await client.send_message(message.channel, u"Ce rôle là, t'as pas le droit de le prendre \N{WINKING FACE}")
                else :
                    await client.add_roles(message.author, role)
                    await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

            elif args[0] == "remove" :
                requete = msg[7:]
                role = discord.utils.get(message.server.roles, name=args[1])
                if role == None : await client.send_message(message.channel, "Ce rôle n'existe pas...")
                elif not role in message.author.roles : await client.send_message(message.channel, "Tu n'as pas ce rôle...")
                else :
                    await client.remove_roles(message.author, role)
                    await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

            else : await client.send_message(message.channel, "Usage : `!langage <list|add|remove> [langage]` (`!help langage` pour plus de détails)")






        elif len(msg) > 2 and msg[0] == '!' :
           await client.send_message(message.channel, 'A tes souhaits <@' + message.author.id + '> !')

        #ancienmsg[serv] = msg       
           
    except:
        txt = time.strftime('[%d/%m/%Y %H:%M:%S]', time.localtime()) + ' sur ' + message.server.name + '\n' + format_exc() + "\n\n"
        with open("log/erreurs.txt","a") as f : f.write(txt)

                                      
while True:
    try : client.run(secret["discord-token"])
    except :
        txt = "\n\n##########[ERREUR FATALE]##########\n" + time.strftime('[%d/%m/%Y %H:%M:%S]', time.localtime()) + format_exc() + "\n\n"
        with open("log/erreurs.txt","a") as f : f.write(txt)
