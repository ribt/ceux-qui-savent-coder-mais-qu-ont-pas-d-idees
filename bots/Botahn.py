#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import discord
import asyncio
import time
from calendar import timegm
from datetime import date
import random
from traceback import format_exc
from re import search
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
import json
from html import unescape
from os import popen
from sys import exit
import codecs
import speedtest
from unicodedata import name
import qrcode


###################################
#                                 #
#Programme principal du bot Botahn#
#                                 #
###################################

#http://fr.python-requests.org/en/latest/user/quickstart.html#creer-une-requete
#https://docs.python.org/fr/3/library/urllib.request.html#module-urllib.request#
###http://apprendre-python.com/page-expressions-regulieres-regular-python#### lien utile aussi
###https://github.com/ribt/ceux-qui-savent-coder-mais-qu-ont-pas-d-idees/blob/master/bots/tux.py###
description = """```Bonjour,je suis Botahn,le bot de ce serveur.Voici une liste des commandes que je comprends et que vous pouvez utiliser :
/help pour voir ce dont je suis capable
/shifumi pour me défier à ce jeu ancestral
/user <mention> pour tout savoir d'un utilisateur
/dilemme si vous ne savez pas si c'est oui ou non qu'il faut choisir
/+ou- pour tenter de deviner le nombre auquel je pense
/randmsg pour recevoir une phrase aléatoire mais vraie !
/randinsult pour insulter cordialement avec une insulte aléatoire
/pi le nombre pi
/qrcode <information> pour que votre information soit 'transformée' en QRcode,ça peut être un lien,un mot,un nombre etc ...
/coinflip pour lancer une pièce
/wiki <recherche> pour apprendre des choses !
/dé pour lancer un dé !
/role pour interagir avec tes rôles.
/speedtest pour voir le connexion actuellle de Botahn
/cnf pour que je te raconte un Chuck Norris Fact sélectionné au hasard sur https://chucknorrisfacts.fr/
/savoir pour que je vous inonde de mon savoir
/savoir add <blague,anectodes,connaissances,citations...> Pour m'apprendre plus de choses mais attention ! Pas de retour à la ligne dans vos messages,une seule information par `/savoir add` et appliquez vous pour l'ortographe !"
```
"""

motban = ['Syrus','syrus','SYRUS','chocolatine','Chocolatine','roid','Roid','inspecteur']

rolesbannis = """``` Participant de l'île des duellistes Les gentils sympa Vainqueur VISC 1 Trolleur en chef modo nep Visc Participant RPG Participants T.T Vainqueur Troll Tournament 1 Vainqueur Troll Tournament 2 Botahn King of Games Troll PokiCouple TRANCHE ! ```"""

def getUrl(url) :
    req = Request(url, headers={'User-Agent': "Je n'suis pas un robot (enfin si mais un gentil ^^) !"})
    result = urlopen(req)
    result = unescape(result.read().decode("utf-8"))
    return json.loads(result)

botahn=discord.Client()
global fact,shifumi
shifumi=0

#@botahn.event
#async def on_typing(channel, user, when):
    #await botahn.send_message(discord.utils.get(user.server.channels,name ='spam-bot'),'**'+user.name+"** est en train d'écrire un super message dans "+channel.name+'.')

@botahn.event
async def on_channel_create(channel):
    try:
        if channel.server.name != 'Smart People':
            try:
                await botahn.send_message(discord.utils.get(channel.server.channels, name ='annonce'),'Le channel **'+channel.name+'** a été créé !')
            except:
                await botahn.send_message(discord.utils.get(channel.server.channels, name ='general'),'Le channel **'+channel.name+'** a été créé !')
    except:
        pass
    
@botahn.event
async def on_channel_delete(channel):
    try:
        if channel.server.name != 'Smart People':
            try:
                await botahn.send_message(discord.utils.get(channel.server.channels, name ='annonce'),'Le channel **'+channel.name+'** a été détruit !')
            except:
                await botahn.send_message(discord.utils.get(channel.server.channels, name ='general'),'Le channel **'+channel.name+'** a été détruit !')
    except:
        pass
    
@botahn.event
async def on_member_ban(member):
    if member.server.name != 'Smart People':
        await botahn.send_message(discord.utils.get(member.server.channels, name='general'),'***'+member.name+'*** a été banni du serveur.')
        return

@botahn.event
async def on_member_remove(member):
    if member.server.name != 'Smart People':
        await botahn.send_message(discord.utils.get(member.server.channels, name='general'), "***" + member.name + "*** est parti,il était bien trop pathétique pour rester de toute manière.")

@botahn.event
async def on_member_join(member):
    if member.server.name != 'Smart People':
        await botahn.send_message(discord.utils.get(member.server.channels, name='general'),"Bienvenue à <@" +member.id+"> ! Je t'invite à lire les règles dans le salon approprié et à dire bonjour au passage !")
                              
@botahn.event ###CE QU'IL FAIT QUAND IL SE CONNECTE###
async def on_ready():
    await botahn.change_presence(game=discord.Game(name='/help'))
    print("Logged in as:",botahn.user.name)
    print("ID:",botahn.user.id)
    
@botahn.event
async def on_message(message):
    try:
        if message.server.name == 'Smart People':
            if "Frenchies" in [role.name for role in message.author.roles]:
                pass
            else:
                return
    except:
        pass
    if message.author==botahn.user or message.server.name=='TestBot': ###Ignorer le message si c'est Botahn qui l'a écrit"""
        return
    elif message.server == None:
        await botahn.send_message(message.author,'Je ne réponds pas au MP ,désolé !')

    if ('Botahn' in message.content or '436096950211706881' in message.content) and 'café' in message.content:
        await botahn.send_message(message.channel,':coffee:')
        
    elif "Mute" in [role.name for role in message.author.roles]:
        print(message.content)
        await botahn.delete_message(message)###Fonction Mute###
        
    ###LES MOTS BANNIS DU SERVEUR STUPID TOURNAMENTS###
    banmot = False
    for i in motban:
        if i in message.content:
            banmot = True
    if message.server.name=='Stupid Tournaments' and banmot ==True :
        try:
            await botahn.delete_message(message)
            await botahn.send_message(message.author,"Tu as utilisé un mot interdit dans le serveur.")
        except:
            pass

    ###CLEAR###
    if ("modo" in [role.name for role in message.author.roles] or "mod" in [role.name for role in message.author.roles] or message.author.name=='Micmicro')and message.content.startswith('/clear'):
        try:
            msg = message.content.replace('/clear ','')
            nb_messages = int(msg)
            await botahn.purge_from(message.channel,limit=nb_messages, check=None, before=None, after=None, around=None)
        except:
            await botahn.send_message(message.channel,"Erreur,je ne peux pas supprimer les messages vieux de plus de 14 jours.Essayer de demander de supprimer moins de messages d'un coup ")

    ###QR CODE###
    elif message.content.startswith('/qrcode '):
        msg = message.content.replace('/qrcode ','')
        qrcode.make(msg).save("qr.png")
        await botahn.send_file(message.channel, "qr.png")

    ###Alcool###
    elif message.content == '/alcool':
        await botahn.send_file(message.channel,"alcool.png")
        
    ###Phrase random###
    elif message.content == '/randmsg':
        sess = requests.session()
        r = sess.get('https://generateur.vuzi.fr/')
        cook = r.cookies.get_dict()
        dat = str(r.text)
        dat = dat.split('''span id="quotemarkContent">
        ''')
        dat = str(dat[1])
        dat = dat.split('''</span>''')
        dat = str(dat[0])
        dat = dat.replace('  ','')
        await botahn.send_message(message.channel,str(dat))

    ###Insulte random###
    elif message.content == '/randinsult':
        sess = requests.session()
        r = sess.get('http://insultron.fr')
        cook = r.cookies.get_dict()
        dat = str(r.text)
        dat = dat.split('''<!-- --------------TEST-------------- -->
	<link rel="publisher" href="https://plus.google.com/u/2/103855380029124418175"/>
	
	

	
	<meta property="og:local" content="fr_FR" />
	<meta property="og:type" content="website" />
	<meta property="og:title" content="Insultron | Le générateur d'insultes ultime!"/>
	<meta property="og:description" content="''')
        dat = str(dat[1])
        dat = dat.split('''"/>''')
        dat = str(dat[0])
        await botahn.send_message(message.channel,str(dat))

        
    ###NEP NEP NEP###
    elif message.content.startswith("nep") and "nep" in [role.name for role in message.author.roles]: 
            args = message.content.split(" ")
            x= 0
            nep =""
            while x<len(args):
                nep = str(nep) + " nep"
                x+=1
            await botahn.send_message(message.channel,str(nep))

    ###MUTE POUR LES MODO####
    elif "modo" in [role.name for role in message.author.roles] and message.content.startswith('/mute'):
        try:
            user = message.mentions[0]
            await botahn.add_roles(user,discord.utils.get(message.server.roles, name='Mute'))
            await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
            await botahn.send_message(user,"Tu as été mute par <@"+str(message.author.id)+">,Si tu veux pouvoir de nouveau parler dans "+str(message.server.name)+",il faudra attendre qu'un modérateur te libère.")
        except:
           await botahn.send_message(message.channel,"Tu as sans doute mal utilisé la commande,il faut être dans un serveur,avoir le grade de modo, et la rédiger sous cette forme : ```/mute <@Mentionexemple#0000>```")
    elif "modo" in [role.name for role in message.author.roles] and message.content.startswith('/unmute'):
        try:
            user = message.mentions[0]
            await botahn.remove_roles(user,discord.utils.get(message.server.roles,name="Mute"))
            await botahn.add_reaction(message,u"\N{WHITE HEAVY CHECK MARK}")
            await botahn.send_message(user,"Tu peux de nouveau parler dans "+str(message.server.name)+"! Essaye d'être plus respectueux des règles")
        except:
            await botahn.send_message(message.channel,"Tu as sans doute mal utilisé la commande, il faut être dans un serveur,avoir le grade de modo,vouloir unmute une personne mute et rédiger ta demande sous cette forme : ```/unmute <@MentionTest#0000>```")

    #ROLE#
    elif message.content.startswith('/role') :
        if 'inspecteur' in message.content:
            await botahn.delete_message(message)
            if message.content =='/role add inspecteur':
                await botahn.add_roles(message.author,discord.utils.get(message.server.roles,name ='inspecteur'))
            return
        args = message.content.split(" ")
        if message.channel.name !="spam-bot" and message.channel.name != "commande-teste":
            await botahn.send_message(message.channel,"Cette commande doit être utilisé dans le salon #spam-bot !")
            return
        elif message.server.name !="Stupid Tournaments":
            await botahn.send_message(message.channel,"Cette commande n'est pas disponible pour ce serveur.")
            return
        elif len(args) == 2:
            if str(args[1])== 'banlist':
                await botahn.send_message(message.channel,rolesbannis)
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
            else:
                await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove/banlist> <rôle désiré>```")
        elif len(args) > 3 or len(args) <3:
            await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove/banlist> <rôle désiré>```")
        elif str(args[2]) in rolesbannis:
            await botahn.send_message(message.channel,"C'est interdit ça mon petit gars.")
        elif str(args[1]) != "remove" and str(args[1]) != "add" and str(args[1]) !='banlist':
            await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove/banlist> <rôle désiré>``` Ne mettez pas de rôles si vous mettez `banlist`")
        elif str(args[1]) =="banlist":
            await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove/banlist> <rôle désiré>``` Ne mettez pas de rôles si vous mettez `banlist`")
        elif str(args[1]) == "add" :
            try :
                if message.author.name !='vrinth':
                    await botahn.add_roles(message.author,discord.utils.get(message.server.roles,name =str(args[2])))
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
            except :
                await botahn.send_message(message.channel,"Tu as sans doute mal utilisé la commande, mal écrit le nom du rôle ou essayé de te donner un rôle que tu n'as pas le droit de recevoir ou que tu possèdes déjà.")
        elif str(args[1])  == "remove":
            try :
                await botahn.remove_roles(message.author,discord.utils.get(message.server.roles,name =str(args[2])))
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
            except :
                await botahn.send_message(message.channel,"Tu as sans doute mal utilisé la commande, mal écrit le nom du rôle ou essayé de te retirer un rôle que tu n'as pas le droit de te retirer ou que tu ne possèdes pas.")
                        
    #SAVOIR#
    elif message.content =='/savoir':
        data = open("savoir.txt","r")
        liste = data.read().split('\n')
        data.close()
        savoir = random.choice(liste)
        while savoir == "": savoir = random.choice(liste)
        await botahn.send_message(message.channel,savoir)
    elif message.content.startswith('/savoir add'):
        try:
            savoir = message.content.replace('/savoir add ','')
            data = open("savoir.txt","r")
            liste = data.read().split('\n')
            data.close
            if savoir in liste : await botahn.send_message(message.channel,'Je connais déjà ceci ^^')
            else:
                data = open("savoir.txt","a")
                data.write('\n' + savoir)
                data.close()
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
        except:
            await botahn.send_message(message.channel,"Une erreur s'est produite")


    ###FONCTION WIKI###
    elif message.content=="/wiki Botahn" or message.content=="/wiki botahn":
        await botahn.send_message(message.channel,"C'est moi ça.Si tu veux savoir des choses sur moi,utilise la commande`/help`")
    elif message.content.startswith('/wiki'):
        args = message.content.split(" ")
        if len(args) < 2 : return
        else :
            req = quote_plus(" ".join(args[1:]))
            resultat = getUrl("https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exsentences=2&explaintext&exintro&redirects=true&titles=" + req)["query"]["pages"]
            print(resultat)
            id = list(resultat)[0]
            titre = resultat[id]["title"]
            if id == "-1" :
                resultat = getUrl("https://fr.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&search=" + req)
                if resultat[2] != [] and resultat[2][0] != "" :
                    e = discord.Embed(description=resultat[2][0], color=0xff00fa)
                    titre = quote_plus(resultat[1][0])
                    image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + titre)["query"]["pages"]
                    id = list(image)[0]
                    if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                    await botahn.send_message(message.channel, embed=e)
                else : await botahn.send_message(message.channel, "Alors ça je ne connais pas du tout")
            else :
                e = discord.Embed(description=resultat[id]["extract"], color=0x00ff00)
                image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + req)["query"]["pages"]
                id = list(image)[0]
                if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                await botahn.send_message(message.channel, embed=e)

    ###FONCTION DILEMME###
    elif message.content=="/dilemme": 
        if random.randint(1,2)==1:
            await botahn.send_message(message.channel,"Et bien **Oui** !")
        else:
            await botahn.send_message(message.channel,"Et bien **Non** !")

    ###FONCTION PILE OU FACE###
    elif message.content=="/coinflip":
        #await botahn.send_file(message.channel,'index.jpg')
        popopo = random.randint(0,2001)
        if popopo >1000:
            await botahn.send_message(message.channel,"```FACE !```")
        elif popopo <1000:
            await botahn.send_message(message.channel,"```PILE !```")
        elif popopo ==1000:
            await botahn.send_message(message.channel,"```Sur la tranche o.O!```")
            await botahn.add_roles(user,discord.utils.get(message.server.roles, name='TRANCHE !'))

    ###Le nombre pi###
    elif message.content == "/pi" :
        await botahn.send_message(message.channel, "```3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527```")

    elif message.content =="/dé":
        nombre = random.randint(1,6)
        if nombre==1:
            msg ="""```+-------+
|       |
|   ♦   |
|       |
+-------+```"""
        elif nombre ==2:
            msg = """```+-------+
|♦      |
|       |
|      ♦|
+-------+```"""
        elif nombre ==3:
            msg = """```+-------+
|♦      |
|   ♦   |
|      ♦|
+-------+```"""
        elif nombre ==4:
            msg = """```+-------+
|♦     ♦|
|       |
|♦     ♦|
+-------+```"""
        elif nombre ==5:
            msg = """```+-------+
|♦     ♦|
|   ♦   |
|♦     ♦|
+-------+```"""
        elif nombre==6:
            msg ="""```+-------+
|♦     ♦|
|♦     ♦|
|♦     ♦|
+-------+```"""
        await botahn.send_message(message.channel,msg)
        
                
    ###Le bot dit ce qu'il sait faire###
    elif message.content=="/help":
        await botahn.send_message(message.author,description)
    
    ###BLAGUES NULLES###
    elif message.content =="Who's Gay ?":
        mssg=await botahn.wait_for_message(author = message.author)
        if mssg != None:
            await botahn.delete_message(mssg)
            await botahn.send_message(message.channel,"***"+str(mssg.content)+"***"+ " is Gay.")
    ###BLAGUES NULLES###

    ###CNF###
    elif message.content =="/cnf":
        if True:
            try:
                page = random.randint(1,345)
                sess = requests.session()
                r = sess.get('https://chucknorrisfacts.fr/facts?p='+str(page))
                #cook = r.cookies.get_dict()
                dat = str(r.text)
                #print(dat)

                fact = dat.split('''</div>    <div class="factbody">''')
                a = random.randint(1,30)
                act =str(fact[a])
                fact = act.split('<div')
                act = str(fact[0])
                act = act.replace('&acirc;','â')
                act = act.replace('<br />','')
                act =act.replace('&eacute;','é')
                act = act.replace("&#039;","'")
                act = act.replace('&agrave;','à')
                act = act.replace('&egrave;','è')
                act = act.replace('&ecirc;','ê')
                act = act.replace('&ccedil;','ç')
                act = act.replace('&icirc;','î')
                act = act.replace('&ugrave;','ù')
                act = act.replace('&quot;','"')
                act = act.replace('&ocirc;','ô')
                act = act.replace('&iuml;','ï')
                await botahn.send_message(message.channel,act)
            except:
                await botahn.send_message(message.channel,'Une erreur est survenue lors de votre demande')
    ###CNF###
        
    ###JEU SHIFUMI###
    elif message.content=="/shifumi":
            name_1 = message.author
            await botahn.send_message(message.channel,"Jouons ! Ecris `/pierre`,`/feuille` ou `/ciseaux` .")
            coup_bot = random.randint(1,3)
            shifumi = 0
            while shifumi == 0:
                msg = await botahn.wait_for_message(author=name_1)
                if msg.content=="/pierre" or msg.content=="/feuille" or msg.content=="/ciseaux":
                    if msg.content=="/pierre":
                        if coup_bot==1:
                            await botahn.send_message(message.channel,"`Pierre`")
                        elif coup_bot==2:
                            await botahn.send_message(message.channel,"`Feuille`")
                        elif coup_bot==3:
                            await botahn.send_message(message.channel,"`Ciseaux`")
                    elif msg.content=="/feuille":
                        if coup_bot==1:
                            await botahn.send_message(message.channel,"`Feuille`")
                        elif coup_bot==2:
                            await botahn.send_message(message.channel,"`Ciseaux`")
                        elif coup_bot==3:
                            await botahn.send_message(message.channel,"`Pierre`")
                    elif msg.content=="/ciseaux":
                        if coup_bot==1:
                            await botahn.send_message(message.channel,"`Ciseaux`")
                        elif coup_bot==2:
                            await botahn.send_message(message.channel,"`Pierre`")
                        elif coup_bot==3:
                            await botahn.send_message(message.channel,"`Feuille`")
                    if coup_bot==1:
                        await botahn.send_message(message.channel,"Egalité !")
                    elif coup_bot==2:
                        await botahn.send_message(message.channel,"J'ai gagné !")
                    elif coup_bot==3:
                        await botahn.send_message(message.channel,"Oh j'ai perdu ...")
                    shifumi=1
                else:
                    await botahn.send_message(message.channel,"Tu n'as pas entré une commande correcte...Les bonnes commandes sont `/pierre`,`/feuille`et `/ciseaux`")                        

    ##JEU + OU -###
    elif message.content=="/+ou-":
            nbrrr = 0
            verif = 0
            nombre_deviner =random.randint(0,100) 
            name_2 = message.author
            await botahn.send_message(message.channel,"Essaye de trouver mon nombre !")
            print(nombre_deviner)
            while verif ==0:
                msg2 = await botahn.wait_for_message(author = name_2)
                try:
                    nbr = int(msg2.content)
                    bug = 0
                except:
                    await botahn.send_message(message.channel,"Il faut rentrer un nombre entier compris entre 0 et 100(inclus)")
                    bug = 1
                if nbr >=0 and nbr <=100 and bug==0:
                    nbrrr = nbrrr+1
                    if nbr==nombre_deviner:
                        await botahn.send_message(message.channel,"Bien joué ! Je pensais bien à `" + str(nbr) + "`")
                        await botahn.send_message(message.channel,"Nombre de coups : `" +str(nbrrr) + "`")
                        verif=1
                    elif nbr < nombre_deviner:
                        await botahn.send_message(message.channel,"Et non,mon nombre est plus grand !")
                    elif nbr> nombre_deviner:
                        await botahn.send_message(message.channel,"Non ! Mon nombre est plus petit !")
                else:
                    await botahn.send_message(message.channel,"Le nombre doit être compris entre 0 et 100(inclus)")

    #SPEEDTEST#
    elif message.content == "/speedtest":
        try:
            loader = await botahn.send_message(message.channel, "Veuillez patienter...")
            s = speedtest.Speedtest()
            s.get_best_server()
            #await botahn.edit_message(loader, "Mesure du débit descendant...")
            s.download()
            #await botahn.edit_message(loader, "Mesure du débit montant...")
            s.upload()
            #await botahn.edit_message(loader, "Encore un instant...")
            url = s.results.share()
            await botahn.delete_message(loader)
            await botahn.send_message(message.channel, url)
        except:
            pass

    ###USER###
    elif message.content.startswith("/user") :
        if len(message.mentions) == 1 :
            member = message.mentions[0]
            user = await botahn.get_user_info(member.id)
            em = discord.Embed(title=user.name, colour=0xff00fa)
            em.set_image(url=user.avatar_url)
            em.add_field(name="A créé son compte le :", value=time.strftime("%d/%m/%Y", date.timetuple(user.created_at)), inline=True)
            if user.bot :
                em.add_field(name="Bot :", value="Oui", inline=True)
            else :
                em.add_field(name="Bot :", value="Non", inline=True)
            em.add_field(name="A rejoint le serveur le :", value=time.strftime("%d/%m/%Y", date.timetuple(member.joined_at)), inline=True)
            em.add_field(name="ID :", value=user.id, inline=True)
            if member.game :
                em.add_field(name="Jeu :", value=str(member.game), inline=True)
            em.add_field(name="Statut :", value=str(member.status), inline=True)
            if member.top_role :
                em.add_field(name="Plus haut rôle :", value=str(member.top_role), inline=True)
            if member.nick :
                em.add_field(name="Surnom :", value=member.nick, inline=True)
            await botahn.send_message(message.channel, embed=em)
        else :
            await botahn.send_message(message.channel, "Essaye d'utiliser la commande ainsi : ```/user <@mention>```")

    ###Botahn le barman de l'impossible###
    elif message.content.startswith('/bar'):
        if message.channel.name !='spam-bot' and message.channel.name !='bar' and message.channel.name !='commande-teste':
            await botahn.send_message(message.channel,'Je ne sers les clients que dans #spam-bot ou dans #bar !')
        else:
            args = message.content.split(' ')
            if len(args) == 1 or len(args) > 3 or message.content =='/bar help':
                await botahn.send_message(message.channel,'''Si tu ne sais pas utiliser la commande,je te recommande de faire `/bar drink|help|foood|randfood|randdrink|buy <ID_de_l'objet>`''')
            else:
                await botahn.send_message(message.channel,'Travail en cours,vous pourrez bientôt utiliser cette commande')
                
botahn.run("TOKEN")  ###COMMANDE DE LANCEMENT DU BOT###
            
        
        
        




