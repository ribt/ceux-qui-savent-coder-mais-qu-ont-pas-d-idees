import discord
import asyncio
import time
from calendar import timegm
from datetime import date
import random
from traceback import format_exc
from re import match
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
import json
from html import unescape
from os import popen
from sys import exit
import feedparser
import codecs
import speedtest
from unicodedata import name
from hashlib import sha256
import qrcode
from variables import fast, aide_fast, caracteres, feeds, pendu

commandes = {"blague": "`!blague` pour avoir une blague au hasard parmis celles que je connais et `!blague add <Votre blague.>` pour m'en apprendre une nouvelle (mettre un `|` pour que je fasse une pause au moment de raconter votre blague)",
             "citation": "`!citation` pour avoir une citation au hasard parmis celles que je connais et `!citation add <Votre citation.>` pour m'en apprendre une nouvelle",
             "chr": "`!chr <c>` où `<c>` est n'importe quel caractère pour avoir le nom et le code Unicode de ce caractère",
             "crypto": "`!crypto <nom>` pour avoir des infos sur l'état actuel de la crypto monnaie",
             "date": "la date d'aujourd'hui, tout simplement ^^",
             "defis": "cette commande va de paire avec https://ribt.fr/defis/ \n`!defis` pour avoir le leaderboard et `!defis @quelqu'un` pour avoir le détail pour une personne.",
             "devine": "un super jeu ! (je choisis un nombre entre 0 et 100 et tu dois le deviner)",
             "fast": aide_fast,
             "gif": "`!gif <recherche>` pour chercher un GIF (une recherche vide donne un GIF aléatoire)",
             "gps": "`!gps <latitude,longitude>` pour avoir les trois mots what3words et l'adresse correspondant aux coordonnées. Exemple : `!gps 49.192149,-0.306415`.",
             "help": "la liste des commandes (`!help <comande>` pour avoir toutes les infos sur une commande)",
             "heure": "l'heure, tout simplement ^^",
             "lmgtfy": "Let Me Google That For You, je fais une recherche sur Internet pour toi",
             "loc": "Lines Of Code : je te dis combien de lignes comporte actuellement mon programme Python",
             "mute": "**uniquement pour les modérateurs**\n`!mute <@utilisateur> <temps><s|m|h|j> <motif>` pour mute temporairement quelqu'un",
             "ping": "tester la vitesse connection avec le bot",
             "proverbe": "`!proverbe` pour avoir un proverbe au hasard parmis ceux que je connais et `!proverbe add <Votre proverbe.>` pour m'en apprendre un nouveau",
             "qr": "`!qr <du blabla>` pour faire un QR code avec les données",
             "r2d": "`!r2d <nombre en chiffres romains>` pour convertir un nombre en chiffres romains en un nombre en chiffres décimaux",
             "role": "`!role <list|add|remove> [rôle1] [rôle2] [rôle3] ...` pour vous ajouter, supprimer ou lister tous les rôles disponibles",
             "roll": "un nombre (pseudo-)aléatoire entre 0 et 100",
             "rot13": "`!rot13 <texte>` pour chiffrer/déchiffrer un message en rot13",
             "speedtest": "je me la pète un peu avec ma conexion de taré ^^",
             "vps": "quelques infos sur le VPS qui m'héberge",
             "rug": "Random User Generator, une identité aléatoire",
             "ud": "`!ud <mot>` pour chercher la définition d'un mot sur Urban Dictionnary (en anglais)",
             "unicode": "`!unicode <code>` je renvois le caractère correspondant au code Unicode donné (au format décimal)",
             "user": "`!user @mention` quelques infos sur la personne",
             "w3w": "`!w3w <mot1.mot2.mot3> [langue]` pour avoir les coordonnées GPS et l'adresse d'un lieu à partir des ses trois mots what3words. La langue est le code ISO 639-1 de deux lettres coorespondant. Ce paramètre est facultatif si les mots sont français. Plus d'infos sur https://what3words.com/fr/a-propos/",
             "weather": "`!weather <ville> <jours>` pour avoir les prévisions météo de la ville pendant un certain nombre de jour (un nombre entre 1 et 7)",
             "whois": "`!whois <nom de domaine>` pour avoir queqlues infos sur un nom de domaine",
             "wiki": "`!wiki <recherche>` pour effectuer une recherche sur Wikipédia et avoir la première phrase de l'article",
             "youtube": "`!youtube <nom de la chaîne>` pour avoir les statistiques de cette chaîne."}

with open("wordlist/courants.txt", "r") as f : mots = f.read().split("\n")
with open("secret.json", "r") as f : secret = json.loads(f.read())

chaine, nbr, coups, ancienmsg, PartieP, mot, aff, vies = {},{},{},{},{},{},{},{}
tmp = log = None

def getUrl(url) :
    req = Request(url, headers={'User-Agent': "Je n'suis pas un robot (enfin si mais un gentil ^^) !"})
    result = urlopen(req)
    result = unescape(result.read().decode("utf-8"))
    return json.loads(result)

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


try :
    """
    async def actu():
        await client.wait_until_ready()
        channel = discord.Object(id='420635603592413185')
        while not client.is_closed:
            dernier = time.time()
            await asyncio.sleep(10*60) # 10 minutes
            for feed in feeds :
                rss = feedparser.parse(feed)
                for i in rss['entries'] :
                    if timegm(i['published_parsed']) > dernier :
                        await client.send_message(channel, i['link'])
    """        
    client = discord.Client()
            
    @client.event
    async def on_ready():
        try :
            global log, ribt
            log = time.strftime("log/%Y%m%d", time.localtime())
            with open(log,"a") as f : f.write(time.strftime('\n\n***[%H:%M:%S]', time.localtime()) + ' Connecté en tant que ' + client.user.name + ' (id : ' + client.user.id + ')\n')
            await client.change_presence(game=discord.Game(name='jouer avec vous'))
            ribt = await client.get_user_info("321675705010225162")
            await client.start_private_message(ribt)
            await client.send_message(ribt, 'OK')
        except:
            txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n', time.localtime()) + format_exc() + "\n\n"
            with open("log/erreurs.txt","a") as f : f.write(txt)

    @client.event
    async def on_member_join(member):
      with open("config.json", "r") as f : config = json.loads(f.read())
      if member.server.id in config and "mp_accueil" in config[member.server.id] :
         await client.send_message(member, config[member.server.id]["mp_accueil"])

    @client.event
    async def on_member_remove(member):
      await client.send_message(discord.utils.get(member.server.channels, name='accueil'), "Au revoir **" + member.name + "** \N{WAVING HAND SIGN}")

    @client.event
    async def on_message(message):
        try:
            if message.author == client.user : return

            if message.content == "!reboot" and message.author == ribt :
                  with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + "Tux va tenter de redemarrer sur demande de ribt\n")
                  cmd = popen("python3 tux.py &")
                  exit()
            
            if message.server == None :
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

            global log, tmp, ancienmsg, loader, chaine, nbr, coups, vies, mot, aff
            #print (message.content)
            t = timegm(message.timestamp.timetuple())
            msg = message.content
            args = msg.split(" ")
            serv = message.server.id
            txt = time.strftime('\n[%H:%M:%S] #', time.localtime(t)) + str(message.channel) + ' ' + str(message.author) + ' : ' + msg
            if log != time.strftime("log/%Y%m%d", time.localtime()): log = time.strftime("log/%Y%m%d", time.localtime())
            with open(log,"a") as f : f.write(txt)
            with open("mute.json", "r") as f : mute = json.loads(f.read())

            if message.author.id in mute :
                if mute[message.author.id]['expires'] < time.time() :
                    del mute[message.author.id]
                    with open("mute.json", "w") as f : f.write(json.dumps(mute, indent=4))
                    await client.remove_roles(message.author, discord.utils.get(message.server.roles, name='VilainPasBeau'))
                elif not "modo" in [role.name for role in message.author.roles] :    
                    await client.delete_message(message)
                    await client.send_message(message.author, "Il te reste encore " + str(round(mute[message.author.id]['expires'] - time.time())) + " secondes pour réfléchir à ce que tu as fait.")
            else :
                if message.author.top_role.name == "VilainPasBeau" :
                    await client.remove_roles(message.author, discord.utils.get(message.server.roles, name='VilainPasBeau'))
                    
                if match(r"(?i)^ah?\W*$", msg) :
                    await client.send_message(message.channel, 'tchoum')

                if match(r"(?i)^[kq]u?oi?\W*$", msg) :
                    await client.send_message(message.channel, 'ffeur')

                elif match(r"(?i)^lol\W*$", msg) :
                    await client.send_message(message.channel, 'ita')

                elif match(r"(?i)^hein\W*$", msg):
                  await client.send_message(message.channel, 'deux')

                elif match(r"(?i)^trois\W*$", msg):
                  await client.send_message(message.channel, 'soleil')
                """
                elif match(r"^[0-9+/() *-]+$", msg):
                  result = str(eval(msg))
                  if result != msg : await client.send_message(message.channel, result)
                """

                
                if msg == "" : pass

                elif msg.startswith('!flag'):
                  await client.delete_message(message)
                  await client.send_message(message.author, "Envoie-moi le flag **PAR MP** sinon tout le monde reçoit une notif avec la réponse \N{TIRED FACE}")

                elif msg == '!ping':
                    tmp = time.time() * 1000 - t * 1000
                    await client.send_message(message.channel, 'Pong ! ('+str(round(tmp,1))+' ms)')

                elif (msg == "Recherche d'un GIF..." or msg == "Recherche du meilleur serveur...") and message.author.id == client.user.id :
                    loader = message

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
                        embed = discord.Embed(title="Description de la commande !" + commande + " :", description=commandes[commande], color=0x00ff00)
                        await client.send_message(message.channel, embed=embed)
                    else :
                        await client.send_message(message.channel, "Pas de description pour cette commande...")

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
                        time.sleep(2)               

                elif msg.startswith('!blague add '):
                    blague = msg.replace('!blague add ', '')
                    f = open("blagues.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    if blague in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà cette blague.')
                    else :
                        f = open("blagues.txt", "a")
                        f.write('\n' + blague)
                        f.close()
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

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
                    if proverbe in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà ce proverbe.')
                    else :
                        f = open("proverbes.txt", "a")
                        f.write('\n' + proverbe)
                        f.close()
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

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
                    if citation in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà cette citation.')
                    else :
                        f = open("citations.txt", "a")
                        f.write('\n' + citation)
                        f.close()
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                elif  msg.startswith('!wiki'):
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `!wiki <recherche>`.")
                    else :
                        req = quote_plus(" ".join(args[1:]))
                        resultat = getUrl("https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exsentences=2&explaintext&exintro&redirects=true&titles=" + req)["query"]["pages"]
                        id = list(resultat)[0]
                        titre = resultat[id]["title"]
                        if id == "-1" :
                            resultat = getUrl("https://fr.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&search=" + req)
                            if resultat[2] != [] and resultat[2][0] != "" :
                                e = discord.Embed(description=resultat[2][0], color=0x00ff00)
                                titre = quote_plus(resultat[1][0])
                                image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + titre)["query"]["pages"]
                                id = list(image)[0]
                                if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                                await client.send_message(message.channel, embed=e)
                            else : await client.send_message(message.channel, "Auncun résultat pour cette recherche...")
                        else :
                            e = discord.Embed(description=resultat[id]["extract"], color=0x00ff00)
                            image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + req)["query"]["pages"]
                            id = list(image)[0]
                            if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                            await client.send_message(message.channel, embed=e)                  
                            
                        
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
                    await client.send_message(message.channel, 'Gagné ' + message.author.mention + ' !!!')

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
                    fact = getUrl("https://www.chucknorrisfacts.fr/api/get?data=tri:alea;nb:1")[0]['fact']
                    await client.send_message(message.channel, fact)

                elif msg == "!ud" : await client.send_message(message.channel, "Usage : `!ud <mot>` (`!help ud` pour plus de détails)")

                elif msg.startswith("!ud ") :
                    url = msg.replace("!ud ", "http://api.urbandictionary.com/v0/define?term=")
                    definition = getUrl(url)
                    if definition['result_type'] == 'no_results' : await client.send_message(message.channel, 'Aucun résultat...')
                    else : await client.send_message(message.channel, definition['list'][0]['definition'])

                elif msg == "!rug" :
                    data = getUrl("https://randomuser.me/api/?nat=fr")['results'][0]
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

                elif msg == "!vps" :
                    txt = ""
                    txt += "freespace=" + popen("df -h /").read().split("\n")[1].split()[3] + "\n"
                    txt += "host=" + popen("hostname --fqdn").read()
                    await client.send_message(message.channel, txt)

                elif msg.startswith("!gif") :            
                    if len(msg) == 4 :
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
                        req = msg[5:]
                        url = "http://api.giphy.com/v1/gifs/search?api_key="+ secret["giphy-key"] + "&lang=fr&limit=1&q=" + req
                        gif = getUrl(url)['data'][0]
                        await client.edit_message(loader, "Téléchargement du GIF...")
                        with open("/home/ribt/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['images']['original']['url']).read())
                        await client.edit_message(loader, "Upload du GIF...")
                        await client.send_file(message.channel, "tmp.gif", filename=gif['title'].replace(" ", "_")+".gif")
                        await client.delete_message(loader)

                elif msg == "!devine" :
                    if message.channel.name != "spam-bot" :
                        await client.send_message(message.channel, "On va pas jouer ici alors qu'il y'a un salon qui s'appelle spam-bot !")
                    else :
                        if serv in nbr :
                            await client.send_message(message.channel, "Une partie est déja en cours...")
                        else :
                            coups[serv] = {}
                            nbr[serv] = random.randint(0, 100)
                            await client.send_message(message.channel, "C'est parti mon kiki ! (devine mon nombre)")
                elif serv in nbr and message.channel.name == "spam-bot" :
                    try : proposition = int(msg)
                    except ValueError : pass
                    else :
                        if message.author.id in coups[serv] : coups[serv][message.author.id] += 1
                        else : coups[serv][message.author.id] = 1
                        if proposition == nbr[serv] :
                            del(nbr[serv])
                            await client.send_message(message.channel, 'Gagné en ' + str(coups[serv][message.author.id]) + ' coups ' + message.author.mention + ' !')
                        elif nbr[serv] < proposition :
                            await client.send_message(message.channel, "C'est moins que " + str(proposition))
                        else :
                            await client.send_message(message.channel, "C'est plus que " + str(proposition))

                elif msg.startswith("!weather") :
                    try :
                        ville, jours = msg.replace("!weather ", "").split(" ")
                        jours = int(jours)
                    except ValueError :
                        await client.send_message(message.channel, "Usage : !weather <ville> <jours>")
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
                    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=" + secret["whois-key"] + "&outputFormat=JSON&domainName=" + dn
                    try : data = getUrl(url)['WhoisRecord']['registryData']['administrativeContact']['rawText'].split("\n")
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
                
                elif msg.startswith("!role") :
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `!role <list|add|remove> [rôle]` (`!help role` pour plus de détails)")
                    elif args[1] == "list" :
                        txt = "__Liste des rôles disponibles :__\n\n"
                        for i in message.server.roles :
                            if str(i.colour) == "#ffffff" : txt += "- **" + i.name + "**\n"
                        txt += "\n(Vous pouvez proposer de nouveaux rôles proposer dans " + discord.utils.get(message.server.channels, name='suggestions').mention + " \N{WINKING FACE})"
                        await client.send_message(message.channel, txt)
                    elif len(args) < 3 : await client.send_message(message.channel, "Usage : `!role <list|add|remove> [rôle]` (`!help role` pour plus de détails)")
   
                    elif args[1] == "add" :
                        for arg in args[2:] :
                            role = None
                            for i in message.server.roles :
                                if i.name.lower() == arg.lower() : role = i
                            if role == None : await client.send_message(message.channel, "Le rôle *" + arg + "* n'existe pas encore mais vous pouvez le proposer dans " + discord.utils.get(message.server.channels, name='suggestions').mention + " \N{WINKING FACE}")
                            elif str(role.colour) != "#ffffff" : await client.send_message(message.channel, "Le rôle *" + arg + "*, t'as pas le droit de le prendre \N{WINKING FACE}")
                            else :
                                await client.add_roles(message.author, role)
                                await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                    elif args[1] == "remove" :
                        for arg in args[2:] :
                            role = None
                            for i in message.author.roles :
                                if i.name.lower() == arg.lower() : role = i
                            if role == None : await client.send_message(message.channel, "Tu n'as pas le rôle *" + arg + "*...")
                            else :
                                await client.remove_roles(message.author, role)
                                await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                    else : await client.send_message(message.channel, "Usage : `!role <list|add|remove> [rôle]` (`!help role` pour plus de détails)")

                elif msg.startswith("!w3w"):
                    if len(args) < 2 or len(args) > 3 : await client.send_message(message.channel, "Usage : `!w3w <mot1.mot2.mot3> [langue]` (`!help w3w` pour plus de détails)")
                    else :
                        url = "https://api.what3words.com/v2/forward?addr=" + quote_plus(args[1]) + "&key=" + secret["w3w-key"] + "&format=json&display=minimal"
                        if len(args) == 3 and args[2].lower() != "fr" : url += "&lang=" + quote_plus(args[2].lower())
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

                elif msg.startswith("!gps"):
                    if len(args) != 2 : await client.send_message(message.channel, "Usage : `!gps <latitude,longitude>` (`!help gps` pour plus de détails)")
                    lat, lng = args[1].split(",")
                    url = "https://api.what3words.com/v2/reverse?coords=" + lat + "," + lng + "&key=" + secret["w3w-key"] + "&lang=fr&format=json&display=minimal"
                    w3w = getUrl(url)['words']
                    if w3w == None : await client.send_message(message.channel, "Les coordonnées semblent être incorrectes... Respectez la syntaxe : `!gps <latitude,longitude>`.")
                    else :
                        await client.send_message(message.channel, "w3w : " + w3w)              
                        url = "https://services.gisgraphy.com/reversegeocoding/search?format=json&lat=" + lat + "&lng=" + lng
                        adresse = getUrl(url)['result'][0]
                        await client.send_message(message.channel, "adresse complète : " + adresse['formatedFull'])

                elif msg == "!speedtest":
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
                    await client.send_message(message.channel, url)


                elif msg.startswith("!lmgtfy") or msg.startswith("!lmqtfy") or msg.startswith("!qwant"):
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `" + args[0] + " <recherche>` (`!help " + args[0][1:] + "` pour plus de détails)")
                    else :
                        recherche = " ".join(args[1:])
                        url = "https://api.qwant.com/egp/search/web?count=10&q=" + quote_plus(recherche)
                        resultats = getUrl(url)
                        if resultats['status'] == "error" : await client.send_message(message.channel, "Une erreur s'est produite, j'espère que c'est pas parce que t'as écrit n'importe quoi \N{WINKING FACE}")
                        else :
                            txt = "Voici les 10 premiers liens de ta recherche sur Qwant :\n"
                            if args[0][3] == "g" : txt +=  "(t'as quand même pas cru que j'allais utiliser Google \N{SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES})\n"
                            for i in resultats['data']['result']['items'] : txt += i['url'] + "\n"
                            txt += "Voilà, voilà..."
                            await client.send_message(message.channel, txt)

                elif msg.startswith("!chr") :
                    if len(args) != 2 : await client.send_message(message.channel, "Usage : `!chr <c>` (`!help chr` pour plus de détails)")
                    else :
                        c = args[1]
                        await client.send_message(message.channel, "Le caractère `" + c + "` répond au doux nom de **" + name(c) + "** et son code Unicode est **" + str(ord(c)) + "**.")

                elif msg.startswith("!unicode") :
                    if len(args) != 2 : await client.send_message(message.channel, "Usage : `!unicode <code>` (`!help unicode` pour plus de détails)")
                    else :
                        try :
                            c = chr(int(args[1]))
                            await client.send_message(message.channel, "Le caractère correspondant au code " + args[1] + " est le suivant : `" + c + "` (" + name(c) + ").")
                        except (ValueError, OverflowError) : await client.send_message(message.channel, "Aucun caractère ne correspond à ce numéro...")

                elif msg == "!loc" :
                    l = popen("wc -l tux.py").read().split(" ")[0]
                    s = popen("ls -lh tux.py").read().split(" ")[4] + "o"
                    await client.send_message(message.channel, "Mon code source (écrit en Python) comporte actuellement " + joliStr(l) + " lignes (" + s + ").")

                elif msg.startswith("!crypto") :
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `!crypto <nom de la monnaie>`")
                    else :
                        req = " ".join(args[1:]).lower()
                        crypto = getUrl("https://api.coinmarketcap.com/v1/ticker/?limit=0")
                        cid = None
                        for i in crypto :
                            if i["id"].lower() == req or i["name"].lower() == req or i["symbol"].lower() == req :
                                cid = i["id"]
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

                elif msg.startswith("!user") :
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
                    else : await client.send_message(message.channel, "Usage : `!user @quelqu'un`")

                elif msg == "!life": await client.send_file(message.channel, "life.gif")
                
                elif msg == "!gratuit": await client.send_file(message.channel, "gratuit.png")

                elif msg == '!haddock':
                    with open("haddock.txt","r") as f : c = f.read().split('\n')
                    await client.send_message(message.channel, random.choice(c))

                elif "modo" in [role.name for role in message.author.roles] and msg.startswith("!mute") :
                    try :
                        user = message.mentions[0]
                        if args[2][-1] == "s" : temps = int(args[2][:-1])
                        elif args[2][-1] == "m" : temps = int(args[2][:-1])*60
                        elif args[2][-1] == "h" : temps = int(args[2][:-1])*3600
                        elif args[2][-1] == "j" : temps = int(args[2][:-1])*3600*24
                        motif = " ".join(args[3:])
                        with open("mute.json", "r") as f : mute = json.loads(f.read())
                        mute[user.id] = {}
                        mute[user.id]['time'] = args[2]
                        mute[user.id]['by'] = message.author.name
                        mute[user.id]['expires'] = time.time() + temps
                        mute[user.id]['motif'] = motif
                        with open("mute.json", "w") as f : f.write(json.dumps(mute, indent=4))
                        await client.add_roles(user, discord.utils.get(message.server.roles, name='VilainPasBeau'))
                    except Exception : await client.send_message(message.channel, "Usage : `!mute <@utilisateur> <temps><s|m|h|j> <motif>`")
                    await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                    await client.send_message(user, "Tu a été mute pendant " + args[2] + " par **" + message.author.name + "** pour le motif suivant : *" + motif + "*.")

                elif msg.startswith("!youtube") :
                  if len(args) == 1 : await client.send_message(message.channel, "`!youtube <nom de la chaîne>` pour avoir les statistiques de cette chaîne.")
                  chaine = " ".join(args[1:])
                  recherche = getUrl("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&type=channel&q=" + quote_plus(chaine) + "&key=" + secret["google-key"])["items"]
                  if recherche == [] : await client.send_message(message.channel, "Aucun résultat...")
                  else :
                    channelId = recherche[0]["id"]["channelId"]
                    data = getUrl("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=" + channelId + "&key=" + secret["google-key"])["items"]
                    data = data[0]
                    em = discord.Embed(title=data["snippet"]["title"], colour=0x00ff00)
                    em.set_image(url=data["snippet"]["thumbnails"]["high"]["url"])
                    em.add_field(name="id :", value=data["id"], inline=True)
                    em.add_field(name="description :", value=data["snippet"]["description"], inline=True)
                    em.add_field(name="date de création de la chaîne :", value=data["snippet"]["publishedAt"].replace("T", " à ")[:-5], inline=True)
                    if "country" in data["snippet"] : em.add_field(name="pays :", value=data["snippet"]["country"], inline=True)
                    if not data["statistics"]["hiddenSubscriberCount"] :
                      em.add_field(name="nombre total de vues :", value=joliStr(data["statistics"]["viewCount"]), inline=True)
                      em.add_field(name="nombre d'abonnés :", value=joliStr(data["statistics"]["subscriberCount"]), inline=True)
                      em.add_field(name="nombre de vidéos :", value=joliStr(data["statistics"]["videoCount"]), inline=True)
                      em.add_field(name="nombre de commentaires postés :", value=joliStr(data["statistics"]["commentCount"]), inline=True)
                    await client.send_message(message.channel, embed=em)
                elif msg.startswith("!code") :
                  await client.send_message(message.channel, " Mon code source (en Python) : https://github.com/ribt/ceux-qui-savent-coder-mais-qu-ont-pas-d-idees/blob/master/bots/tux.py")

                elif msg == "!ecris" :
                  await client.delete_message(message)
                  await client.send_typing(message.channel)

                elif msg.startswith("!defis"):
                  with open("score.json", "r") as f : score = json.loads(f.read())
                  with open("flags.json", "r") as f : l = len(json.loads(f.read()))
                  if len(args) == 1 :
                    leaders = []
                    for i in range(10):
                      best = 0
                      tmp = None
                      for userId in score :
                        if score[userId]["points"] >= best and not userId in leaders:
                          best = score[userId]["points"]
                          tmp = userId
                      if tmp != None : leaders.append(tmp)
                    txt = "classement de https://ribt.fr/defis/ :\n\n"
                    for leader in leaders:
                      txt += str(leaders.index(leader)+1) + ". "
                      txt += "**" + discord.utils.get(message.server.members, id=leader).name + "** "
                      txt += str(score[leader]["points"]) + " pts ("
                      txt += str(round(len(score[leader]["reussis"])/l*100)) + " %) \n"
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
                  else : await client.send_message(message.channel, "Usage : `!defis` pour avoir le leaderboard et `!defis @quelqu'un` pour avoir le détail pour une personne.")

                elif msg.startswith("!qr"):
                  if len(args) == 1 : await client.send_message(message.channel, "Usage : `!qr <du texte>`.")
                  else :
                    data = " ".join(args[1:])
                    qrcode.make(data).save("qr.png")
                    await client.send_file(message.channel, "qr.png")



                  
                    
                    
                    
                    




                # ^ nouvelles commandes ici ^

                elif len(msg) > 2 and msg[0] == '!' :
                   await client.send_message(message.channel, 'A tes souhaits ' + message.author.mention + ' !')

                ancienmsg[serv] = msg
                
        except Exception :
            txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n') + format_exc() + "\n\n"
            with open("log/erreurs.txt","a") as f : f.write(txt)
                

    #client.loop.create_task(actu())
    client.run(secret["discord-token"])
except Exception :
    txt = "\n\n##########[ERREUR FATALE]##########\n" + time.strftime('[%d/%m/%Y %H:%M:%S]') + format_exc() + "\n\n"
    with open("log/erreurs.txt","a") as f : f.write(txt)
    time.sleep(60*10)
    with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + "Tux va tenter de redemarrer\n")
popen("python3 tux.py &")
        

with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + "Tux va tenter de redemarrer\n")
popen("python3 tux.py &")
        

