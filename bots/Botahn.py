#!/usr/bin/env python
#-*- coding: utf-8 -*-

import traceback
import os
import math
import requests
import discord
import asyncio
import time
from calendar import timegm
from datetime import date
import random
from traceback import format_exc
from re import match, search
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
import json
from glob import glob
from html import unescape
from os import popen
from sys import exit
import codecs
import speedtest
import unicodedata
import qrcode
from discord.ext import commands
if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')
###################################
#                                 #
#Programme principal du bot Botahn#
#                                 #
###################################

description = """Bonjour,je suis Botahn,le bot de ce serveur.Voici une liste des commandes que je comprends et que vous pouvez utiliser :
/shifumi
/dilemme ou /dilemme <choix1> <choix2> <choix3> etc... 
/+ou-
/randmsg
/randinsult
/pi
/cookie <@mention>
/ice <@mention>
/qrcode <information>
/flip <mise_facultative> <face|pile facultatif>
/wiki <recherche>
/dé
/daily
/create
/profil <mention facultative>
/money
/pokemon
/reset
/roll <nombre de faces>
/avatar <@mention>
/youtube <recherche>
/role disponible uniquement sur le serveur d'origine de Botahn
/bar
/cnf pour un Chuck Norris Fact
/music_help
/savoir
/code
/teaser
/savoir add <blague,anectodes,connaissances,citations...>
/vipinfo <@mention>
/vipbuy"""

description_2="""/vip <mention> pour nommer quelqu'un VIP
/user <mention> pour tout savoir d'un utilisateur
/love <@mention1> <@mentions2> pour un test d'amour classique
/rappel <temps en seconde> <description facultative> pour ne pas oublier des trucs cons.Quand je suis relancé,je perds tout les rappels en cours et 'joue' à être relancé pendant 10 minutes pour que vous le voyiez.
"""
ema = discord.Embed(title=None, colour=0x000000)
ema.add_field(name="Liste de commandes", value=description, inline=True)
ema_2 = discord.Embed(title=None, colour=0x000000)
ema_2.add_field(name="Liste de commandes VIP", value=description_2, inline=True)
ema_3 = discord.Embed(title = 'En cas de question,de bug, de problème ou de suggestions : contactez Micmicro#9452',description = "Contactez le en MP si vous avez un serveur en commun ou utilisez `/support <message à faire passer>`. Vous pouvez inclure une invitation au serveur sur lequel vous êtes. Il est possible que je ne réponde pas instantanément, je ne suis pas une machine. N'envoyez pas n'importe quoi sinon vous serez simplement ignoré par Botahn pour toutes ses commandes.",colour = 0x000000)
ema_4=discord.Embed(title='Inviter le Bot',description="Voici 2 liens pour inviter Botahn : le premier avec le minimum de permissions si vous n'avez pas confiance en ce bot, le deuxième avec toutes les permissions.Les deux ont le même code source.\n Premier lien :https://discordapp.com/oauth2/authorize?client_id=436096950211706881&scope=bot&permissions=104201280 \nDeuxième lien :https://discordapp.com/oauth2/authorize?client_id=436096950211706881&scope=bot&permissions=2146958591\n Botahn a besoin d'un salon nommé exactement `spam-bot` pour bien fonctionner.\nInviter le bot vous permet de devenir VIP et de nommer d'autres personnes VIP,contactez moi par /support pour avoir accès à ces droits!\nN'étant encore qu'en développement et relativement inutile, je ne suis pas connecté 24h/24.N'hésitez toutefois pas à tapez `/help` régulièrement pour voir mes nouvelles fonctions.",colour=0x000000)
drink = """-vodka    00
-bière    01
-whiskey    02
-mojito    03
-limonade    04
-Ice tea    05
-café    06
-pina colada    07
-jus de tomate    08
-jus de pamplemousse    09
-sang de phoque    10
-vin    11
-diabolo    12
**proposez vos boissons !**"""

food = """-cookie    50
-banane    51
-choucroute    52
-raclette    53
-pizza    54
-burger    55
-sanglier    56
-kebab    57
-tacos    58
-hot dog    59
-mousse au chocolat    60
**-proposez vos plats !**
"""
emdrink = discord.Embed(title=None, colour=0xffff00)
emdrink.add_field(name="***Liste des boissons disponibles et leurs ID :***", value=drink, inline=True)
emfood = discord.Embed(title=None, colour=0xffff00)
emfood.add_field(name="***Liste des plats disponibles et leurs ID :***", value=food, inline=True)
motban = ['Syrus','syrus','SYRUS','chocolatine','Chocolatine','roid','Roid']

rolesbannis = """``` pierres Finalistes de l'île des Duellistes Participant de l'île des duellistes Les gentils sympa Vainqueur VISC 1 Trolleur en chef modo nep Visc Participant RPG Participants T.T Vainqueur Troll Tournament 1 Vainqueur Troll Tournament 2 Botahn King of Games Troll PokiCouple TRANCHE ! ```"""

vipvip = open("vipvip.txt","r")
listevip = vipvip.read().split('\n')
vipvip.close

def getUrl(url) :
    req = Request(url, headers={'User-Agent': "Je n'suis pas un robot (enfin si mais un gentil ^^) !"})
    result = urlopen(req)
    result = unescape(result.read().decode("utf-8"))
    return json.loads(result)

botahn=discord.Client()
global fact,shifumi, log
shifumi=0

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
    await botahn.change_presence(game=discord.Game(name='être relancé'))
    print("Logged in as:",botahn.user.name)
    print("ID:",botahn.user.id)
    await asyncio.sleep(600)
    await botahn.change_presence(game=discord.Game(name='/help'))
    
@botahn.event
async def on_message(message):
    msg=message.content
    args = msg.split(' ')
    try:
        if message.server.name == 'Smart People':
            if "Frenchies" in [role.name for role in message.author.roles]:
                pass
            else:
                return
    except:
        pass
    if message.author.id=='436096950211706881' and message.content.startswith('```\nMusic'):
        await botahn.delete_message(message)
        return
    if message.author==botahn.user:###Ignorer le message si c'est Botahn qui l'a écrit"""
        return
    if message.server == None:
        if 'easteregg' in message.content:
            await botahn.delete_message(message)
            await botahn.send_message(message.author,"Tu as trouvé l'easter egg, tu deviens un VIP si tu n'en es pas déjà un et n'en parle à personne ^^")
            user = message.author
            data = open("vip.txt","r")
            liste = data.read().split('\n')
            data.close
            if user.id in liste : pass
            else:
                data = open("vip.txt","a")
                data.write('\n' + user.id)
                data.close()
        print(message.author)
        print(message.content)
        try:
            await botahn.send_message(message.author,'Je ne réponds pas au MP ,désolé !')
        except:
            pass
        return
    
    t = timegm(message.timestamp.timetuple())
    msg = message.content
    args = msg.split(" ")
    serv = message.server.id
    txt = time.strftime('\n[%H:%M:%S] #', time.localtime(t)) + str(message.channel) + ' ' + str(message.author) + ' : ' + msg
    
    if ('Botahn' in message.content or '436096950211706881' in message.content) and 'café' in message.content:
        await botahn.send_message(message.channel,':coffee:')
        
    elif "Mute" in [role.name for role in message.author.roles]:
        print(message.content)
        await botahn.delete_message(message)
        return###Fonction Mute###
        
    ###LES MOTS BANNIS DU SERVEUR STUPID TOURNAMENTS###
    #banmot = False
    #for i in motban:
        #if i in message.content:
           # banmot = True
    #try:
     #   if message.server.name=='Stupid Tournaments' and banmot ==True :
      #      try:
     #           await botahn.delete_message(message)
      #          await botahn.send_message(message.author,"Tu as utilisé un mot interdit dans le serveur.")
       #     except:
         #       pass
   # except:
       # pass


    ###CLEAR###
    if ("modo" in [role.name for role in message.author.roles] or "mod" in [role.name for role in message.author.roles] or message.author.id=='205009003653103626')and message.content.startswith('/clear'):
        try:
            msg = message.content.replace('/clear ','')
            nb_messages = int(msg)
            await botahn.delete_message(message)
            await botahn.purge_from(message.channel,limit=nb_messages, check=None, before=None, after=None, around=None)
        except:
            await botahn.send_message(message.channel,"Erreur,je ne peux pas supprimer les messages vieux de plus de 14 jours.Essayer de demander de supprimer moins de messages d'un coup ")

    ###changement de jeu###
    elif message.author.id=='205009003653103626' and message.content.startswith('/change '):
        msg = message.content.replace('/change ','')
        await botahn.change_presence(game=discord.Game(name=str(msg)))
    
    ###easteregg###
    elif message.content=='/easteregg':
        try:
            await botahn.delete_message(message)
        except:
            pass
        await botahn.send_message(message.author,"Tu as trouvé l'easter egg, tu deviens un VIP si tu n'en es pas déjà un et n'en parle à personne ^^ Voici en plus une 'clé' que tu enverras en MP à Micmicro ou en utilisant /support pour gagner 50.000€ sur la Botahn Bank")
        user = message.author
        data = open("vip.txt","r")
        liste = data.read().split('\n')
        data.close
        if user.id in liste : pass
        else:
            data = open("vip.txt","a")
            data.write('\n' + user.id)
            data.close()
    
    
    ###SUPPORT###
    elif message.content.startswith('/support '):
        try:
            msg = message.content.replace('/support ','')
            micmicro = await botahn.get_user_info('205009003653103626')
            await botahn.send_message(micmicro,"Demande d'aide de la part de :"+message.author.name+" qui a pour ID :"+message.author.id+"\n"+msg+"\nNom du serveur :"+message.server.name)
            await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
        except:
            await botahn.send_message(message.channel,"Erreur, la commande s'utilise ainsi : `/support <message à faire passer>`")
            
    ###delete message###
    elif message.content.startswith('/del ') and message.author.id=='205009003653103626':
        msgg = message.content.replace('/del ','')
        msg = await botahn.get_message(message.channel,msgg)
        await botahn.delete_message(msg)
        await botahn.delete_message(message)
    
    ###QR CODE###
    elif message.content.startswith('/qrcode '):
        msg = message.content.replace('/qrcode ','')
        qrcode.make(msg).save("qr.png")
        await botahn.send_file(message.channel, "qr.png")
        
    ###Rappel###
    elif message.content.startswith('/rappel '):
        user = message.author
        data = open("vip.txt","r")
        liste = data.read().split('\n')
        data.close
        if user.id in liste : pass
        else:
            await botahn.send_message(message.channel,"Commande réservée aux VIP.")
            return
        msg = message.content.split(' ')
        try:
            nbr = int(msg[1])
            if len(msg) >=3:
                msgg = message.content.replace('/rappel ','')
                msgg = msgg.replace(str(nbr),'')
                msg = True
            if nbr >24*3600 or nbr==0 or nbr<0:
                await botahn.send_message(message.channel,'Je ne peux pas faire de rappels qui dépassent les 24h ou qui sont négatifs ou nuls')
            else:
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                await asyncio.sleep(nbr)
                if msg==True: await botahn.send_message(message.channel,'<@'+message.author.id+'> a demandé à voir un rappel il y a '+str(nbr)+' secondes à propos de **'+str(msgg)+'**')
                else:await botahn.send_message(message.channel,'<@'+message.author.id+'> a demandé à voir un rappel il y a '+str(nbr)+' secondes.')
        except:
            await botahn.send_message(message.channel,'''Une erreur est survenue, la commande s'utilise ainsi : `/rappel <durée en secondes> <description facultative>`''')
    
    ###VIP###
    elif message.content.startswith('/vip '):
        if message.author.id=='205009003653103626' or message.author.id in listevip:
            pass
        else:
            await botahn.send_message(message.channel,"Vous n'avez pas le droit de nommer quelqu'un VIP")
            return
        try:
            user = message.mentions[0]
            data = open("vip.txt","r")
            liste = data.read().split('\n')
            data.close
            if user.id in liste : await botahn.send_message(message.channel,'Je connais déjà ce vip ^^')
            else:
                data = open("vip.txt","a")
                data.write('\n' + user.id)
                data.close()
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
        except:
            await botahn.send_message(message.channel,"Une erreur s'est produite")
    elif message.content.startswith('/vip '):
        await botahn.send_message(message.channel,"Tu n'as pas le droit de nommer quelqu'un VIP.")
    elif message.content.startswith('/vipinfo'):
        try:
            user = message.mentions[0]
            data = open("vip.txt","r")
            liste = data.read().split('\n')
            data.close
            if user.id in liste: await botahn.send_message(message.channel,user.name +" est un VIP")
            else: await botahn.send_message(message.channel,user.name +" n'est pas un VIP")
        except:
            await botahn.send_message(message.channel,"Une erreur s'est produite")
            
    ###Alcool###
    elif message.content == '/alcool':
        await botahn.send_file(message.channel,"alcool.png")

    ###cookie###
    elif message.content.startswith('/cookie'):
        try:
            user = message.mentions[0]
            await botahn.send_message(message.channel,":cookie:<@"+message.author.id+"> vous offre un cookie <@"+user.id+"> !:cookie:")
        except:
            await botahn.send_message(message.channel,"La commande s'utilise ainsi : `/cookie <@mention>`")

    ###ice cream###
    elif message.content.startswith('/ice'):
        try:
            user = message.mentions[0]
            await botahn.send_message(message.channel,":ice_cream:<@"+message.author.id+"> vous offre une glace <@"+user.id+"> !:ice_cream:")
        except:
            await botahn.send_message(message.channel,"La commande s'utilise ainsi : `/ice <@mention>`")
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
    elif ("modo" in [role.name for role in message.author.roles] or message.author.id=="205009003653103626") and message.content.startswith('/mute'):
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
                await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove> <rôle désiré>```")
        elif len(args) > 3 or len(args) <3:
            await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove> <rôle désiré>```")
        elif str(args[2]) in rolesbannis:
            await botahn.send_message(message.channel,"C'est interdit ça mon petit gars.")
        elif str(args[1]) != "remove" and str(args[1]) != "add":
            await botahn.send_message(message.channel,"Pour utiliser cette commande : ```/role <add/remove> <rôle désiré>``` Ne mettez pas de rôles si vous mettez `banlist`")
        elif str(args[1]) == "add" :
            try :
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
        await botahn.send_message(message.channel,"C'est moi ça.Si tu veux savoir des choses sur moi,utilise la commande`/help` ou `/user <@mentionne_moi>`")
    elif message.content.startswith('/wiki'):
        args = message.content.split(" ")
        if len(args) < 2 : return
        else :
            r = quote_plus(" ".join(args[1:]))
            result = getUrl("https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exsentences=2&explaintext&exintro&redirects=true&titles=" + r)["query"]["pages"]
            print(result)
            id = list(result)[0]
            title = result[id]["title"]
            if id == "-1" :
                resultat = getUrl("https://fr.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&search=" + r)
                if result[2] != [] and result[2][0] != "" :
                    e = discord.Embed(description=result[2][0], color=0xff00fa)
                    title = quote_plus(result[1][0])
                    image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + title)["query"]["pages"]
                    id = list(image)[0]
                    if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                    await botahn.send_message(message.channel, embed=e)
                else : await botahn.send_message(message.channel, "Alors ça je ne connais pas du tout")
            else :
                e = discord.Embed(description=result[id]["extract"], color=0x00ff00)
                image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + r)["query"]["pages"]
                id = list(image)[0]
                if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                await botahn.send_message(message.channel, embed=e)

    ###FONCTION DILEMME###
    elif message.content=="/dilemme": 
        if random.randint(1,2)==1:
            await botahn.send_message(message.channel,"Et bien **Oui** !")
        else:
            await botahn.send_message(message.channel,"Et bien **Non** !")
    elif message.content.startswith('/dilemme '):
        try:
            liste = message.content.split(' ')
            if len(liste) <=2:
                if random.randint(1,2)==1:
                    await botahn.send_message(message.channel,"Et bien **Oui** !")
                else:
                    await botahn.send_message(message.channel,"Et bien **Non** !")
            else:
                await botahn.send_message(message.channel,"Je dirais **"+str(liste[random.randint(1,len(liste)-1)])+"**")
        except:
            await botahn.send_message(message.channel,'Une erreur est survenue.')

    ###code###
    elif message.content=="/code":
        await botahn.send_message(message.channel,"Mon code source en Python qui fait actuellement 1300 lignes: https://github.com/ribt/ceux-qui-savent-coder-mais-qu-ont-pas-d-idees/blob/master/bots/Botahn.py \n*Il n'est pas forcément à jour*")

    ###FONCTION PILE OU FACE AVEC MISE(codé avec le cul bien sûr)###
    elif message.content.startswith("/flip"):
        banane = message.content.split(' ')
        if len(banane)==1:
            mise = 0
            choix = 'rien'
            pass
        else:
            try:
                mise = int(banane[1])
                choix = str(banane[2])
                 
                if mise !=0:
                    test= 0
                    nomfichier = "z"+message.author.id+".txt"
                    data = open(nomfichier,"r")
                    liste = data.read().split('\n')
                    data.close 
                    if mise <0 or mise> int(liste[1]):
                        mise = mise +"je sais pas générer une erreur j'ai oublié donc je fais cette merde"
                else:
                    test = 1
                if choix !='face' and choix!='pile':
                    choix = choix + 16516519841621
            except:
                await botahn.send_message(message.channel,"Un argument est incorrect ou vous essayez de miser trop ou vous n'avez pas de compte : `/flip <mise> <face|pile>`")
                return
        popopo = random.randint(0,2000)
        if choix =='face' or choix=='pile' or choix =='rien':
            if popopo > 1000 or choix=='rien':
                if choix=='rien':
                    if random.randint(1,2)==2:
                        choix_2 = 'face'
                    else:
                        choix_2 = 'pile'
                else:
                    choix_2=choix
                if test !=1:
                    data = open(nomfichier,"w")
                    data.write(str(liste[0]) +"\n"+str(int(liste[1])+mise))
                    data.close
                em = discord.Embed(title = "Pile ou face",description =message.author.mention+" a misé **"+str(mise)+"€** sur "+choix+". La pièce est tombé sur "+choix_2+"! Il gagne **"+str(mise)+"€**!",colour = 0xffff00)
            elif popopo <1000:
                if test !=1:
                    data = open(nomfichier,"w")
                    data.write(str(liste[0]) +"\n"+str(int(liste[1])-mise))
                    data.close
                if choix =="face":
                    em = discord.Embed(title = "Pile ou face",description =message.author.mention+" a misé **"+str(mise)+"€** sur "+choix+". La pièce est tombé sur pile! Il perd **"+str(mise)+"€**!",colour = 0xffff00)
                elif choix=='pile':
                    em = discord.Embed(title = "Pile ou face",description =message.author.mention+" a misé **"+str(mise)+"€** sur "+choix+". La pièce est tombé sur face! Il perd **"+str(mise)+"€**!",colour = 0xffff00)
        await botahn.send_message(message.channel,embed=em)
        
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

    elif message.content.startswith('/roll'):
        try:
            nbr = int(message.content.replace('/roll ',''))
            if nbr <2:
                print(ppp)
        except:
            await botahn.send_message(message.channel,"La commande s'utilise ainsi : `/roll <nombre>` puis renvoit un nombre entre 1 et ce nombre.")
            return
        em = discord.Embed(title=None, colour=0x0f00ff)
        em.add_field(name="Lancement d'un dé à "+str(nbr)+" faces.",value = "Le résultat est "+str(random.randint(1,nbr)),inline=True)
        await botahn.send_message(message.channel,embed = em)
        
                
    ###Le bot dit ce qu'il sait faire###
    elif message.content=="/help":
        await botahn.send_message(message.author,embed=ema)
        await botahn.send_message(message.author,embed=ema_2)
        await botahn.send_message(message.author,embed=ema_3)
        await botahn.send_message(message.author,embed=ema_4)
        
    ###Calculateur de love (codé avec le cul)###
    elif message.content.startswith('/love '):
        user = message.author
        data = open("vip.txt","r")
        liste = data.read().split('\n')
        data.close
        if user.id in liste : pass
        else:
            await botahn.send_message(message.channel,"Commande réservée aux VIP.")
            return
        try:
            user= message.mentions[0]
            user_2 = message.mentions[1]
            nbr = int(user.id)
            nbrr = int(user_2.id)
            #on trafique certains résultats
            if (nbr == 334319315828473856 and nbrr==119940459312185347) or (nbrr == 334319315828473856 and nbr==119940459312185347)  or (nbr==436096950211706881 and nbrr==205009003653103626) or (nbrr==436096950211706881 and nbr==205009003653103626):
                nbr=0
                nbrr = 0
            if nbr<nbrr: nbr = nbrr - nbr
            else: nbr = nbr - nbrr
            print(nbr)
            while nbr>1000000000000:
                nbr = nbr- 1000000000000
            while nbr>100000000000:
                nbr = nbr- 100000000000
            while nbr>10000000000:
                nbr = nbr- 10000000000
            while nbr>1000000000:
                nbr = nbr- 1000000000
            print(nbr)
            while nbr>100000000:
                nbr = nbr- 100000000
            print(nbr)
            while nbr>10000000:
                nbr = nbr- 10000000
            print(nbr)
            while nbr>1000000:
                nbr = nbr- 1000000
            print(nbr)
            while nbr>100000:
                nbr = nbr- 100000
            print(nbr)
            while nbr>10000:
                nbr = nbr- 10000
            print(nbr)
            while nbr>1000:
                nbr = nbr- 1000
            print(nbr)
            while nbr>0:
                nbr = nbr -100
            print(nbr)
            nbr = nbr+100
            em = discord.Embed(title=None, colour=0xff0000)
            em.add_field(name="Calcul d'amour", value="<@"+str(user.id)+"> et <@"+str(user_2.id)+"> s'aiment à "+str(nbr)+"% :heart:", inline=True)
            await botahn.send_message(message.channel, embed=em)
        except:
            await botahn.send_message(message.channel,"La commande s'utilise ainsi :```/love <@mention1> <@mention2>```")

    ###YOUTUBE (analyse du code de ribt pour comprendre et amélorier la fonction musique)###
    elif msg.startswith("/youtube") or msg.startswith("/yt") or msg.startswith("/ytb") :
        secret = "clé secrète filou"
        if len(args) == 1 : await client.send_message(message.channel, "Usage : `!youtube <nom de la vidéo ou de la chaîne à chercher>`.")
        else :
            txt = " ".join(args[1:])
            recherche = getUrl("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=" + quote_plus(txt) + "&key=" + secret)["items"][0]["id"]
            if recherche == [] : await botahn.send_message(message.channel, "Aucun résultat...")
            else :
                if recherche["kind"] == "youtube#channel" :
                    channelId = recherche["channelId"]
                    data = getUrl("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=" + channelId + "&key=" + secret)["items"][0]
                    em = discord.Embed(title="CHAINE YOUTUBE : "+data["snippet"]["title"], colour=0x00ff00)
                    em.set_image(url=data["snippet"]["thumbnails"]["high"]["url"])
                    em.add_field(name="ID :", value=data["id"], inline=True)
                    desc = data["snippet"]["description"]
                    if len(desc) < 1000 : em.add_field(name="Description :", value=desc, inline=True)
                    else : em.add_field(name="Description :", value=desc[:1000]+"\n\n[...]", inline=True)
                    em.add_field(name="Date de création de la chaîne :", value=data["snippet"]["publishedAt"].replace("T", " à ")[:-5], inline=True)
                    if "country" in data["snippet"] : em.add_field(name="pays :", value=data["snippet"]["country"], inline=True)
                    if not data["statistics"]["hiddenSubscriberCount"] :
                        #em.add_field(name="nombre total de vues :", value=data["statistics"]["viewCount"], inline=True)
                        #em.add_field(name="nombre d'abonnés :", value=data["statistics"]["subscriberCount"], inline=True)
                        #em.add_field(name="nombre de vidéos :", value=data["statistics"]["videoCount"], inline=True)
                        em.add_field(name="lien :", value="https://www.youtube.com/channel/"+channelId, inline=True)
                        await botahn.send_message(message.channel, embed=em)
                elif recherche["kind"] == "youtube#video" :
                    videoId = recherche["videoId"]
                    data = getUrl("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=" + videoId + "&key=" + secret)["items"][0]
                    em = discord.Embed(title="VIDEO : " + data["snippet"]["title"], colour=0x00ff00)
                    em.set_image(url=data["snippet"]["thumbnails"]["high"]["url"])
                    em.add_field(name="id :", value=data["id"], inline=True)
                    #desc = data["snippet"]["description"]
                    #if len(desc) < 1000 : em.add_field(name="description :", value=desc, inline=True)
                    #else : em.add_field(name="description :", value=desc[:1000]+"\n\n[...]", inline=True)
                    #em.add_field(name="tags :", value=", ".join(data["snippet"]["tags"]), inline=True)
                    #em.add_field(name="date de publication :", value=data["snippet"]["publishedAt"].replace("T", " à ")[:-5], inline=True)
                    #em.add_field(name="nom de la chaîne :", value=data["snippet"]["channelTitle"], inline=True)
                    #if "country" in data["snippet"] : em.add_field(name="pays :", value=data["snippet"]["country"], inline=True)
                    em.add_field(name="Nombre de vues :", value=data["statistics"]["viewCount"], inline=True)
                    if data["contentDetails"]["licensedContent"] : em.add_field(name="Contenu sous licence :", value="oui", inline=True)
                    else : em.add_field(name="contenu sous licence :", value="non", inline=True)
                    em.add_field(name="Lien :", value="https://www.youtube.com/watch?v="+videoId, inline=True)
                    await botahn.send_message(message.channel, embed=em)
                else : await botahn.send_message(message.channel, "Aucun résultat...")

    ###CNF###
    elif message.content =="/cnf":
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
                em = discord.Embed(title=None, colour=0x00ff00)
                em.add_field(name="Chuck Norris Fact :muscle:", value=act, inline=True)
                await botahn.send_message(message.channel, embed=em)
            except:
                await botahn.send_message(message.channel,'Une erreur est survenue lors de votre demande')

    ###POKEMON EN TEST ET EN TRAVAIL###
    elif msg.startswith("/pokemon"):
        pokemons = glob("pokemon/*.gif")
        file = random.choice(pokemons)
        nom = (((((str(file).replace("pokemon",'')).replace(".gif",'')).replace('\\',''))).replace('-f',' ').replace('-',' '))
        try:
            nomfichier = "z"+message.author.id+".txt"
            data = open(nomfichier,"r")
            liste = data.read().split('\n')
            data.close
            if int(liste[1])>=500:
                achat = "Si vous voulez faire de ce pokémon le vôtre pour la faible somme de 500€, réagissez avec :thumbsup:, sinon avec :thumbsdown: "+message.author.name+"."
            else:
                achat = "Avec 500€, vous auriez pu acquérir ce pokémon."
        except:
            achat = ""
        msgpokemon = await botahn.send_file(message.channel, file, content="Un **" +nom + "** sauvage apparaît ! "+achat)
        if achat !="" and achat!= "Avec 500€, vous auriez pu acquérir ce pokémon.":
            await botahn.add_reaction(msgpokemon, u'\N{THUMBS UP SIGN}')
            await botahn.add_reaction(msgpokemon, u'\N{THUMBS DOWN SIGN}')
            res = await botahn.wait_for_reaction([u'\N{THUMBS UP SIGN}',u'\N{THUMBS DOWN SIGN}'],user = message.author,message = msgpokemon)
            if res.reaction.emoji==u'\N{THUMBS DOWN SIGN}':
                await botahn.edit_message(msgpokemon,"Vous n'avez pas choisi **"+nom+"** comme pokémon "+message.author.name)
            else:
                liste[1] = str(int(liste[1])-500)
                profil = str(liste[2])
                profil = profil.split('_')
                profil[6]= nom
                data = open(nomfichier,"w")
                profiltxt = ""
                for i in range(0,len(profil)-1):
                    profiltxt =profiltxt + profil[i]+"_"
                try:
                    data.write(str(liste[0]) +'\n'+str(liste[1])+"\n"+str(profiltxt))
                except:
                    try:
                        data.write(str(liste[0]) +'\n'+str(liste[1])+"\n"+" _ _ _ _ _ _"+nom+"_")
                    except:
                        await botahn.send_message(message.channel,"Tapez /money et réessayez ensuite")
                await botahn.edit_message(msgpokemon,nom+" est maintenant votre pokémon !")
            try:
                await botahn.clear_reactions(msgpokemon)
            except:
                pass
        else:
            pass

    ###JEU SHIFUMI###
    elif message.content=="/shifumi":
            em = discord.Embed(title=None, colour=0x0f00ff)
            em.add_field(name="Shifumi",value = "Jouons "+message.author.name+"! Fais ton choix avec les réactions !",inline=True)
            msgembed = await botahn.send_message(message.channel, embed=em)
            await botahn.add_reaction(msgembed,u'\N{RAISED FIST}')
            await botahn.add_reaction(msgembed,u'\N{RAISED HAND}')
            await botahn.add_reaction(msgembed,u'\N{BLACK SCISSORS}')
            coup_bot = random.randint(1,3)
            res = await botahn.wait_for_reaction([u'\N{RAISED FIST}',u'\N{BLACK SCISSORS}',u'\N{RAISED HAND}'],user = message.author,message = msgembed)
            if res.reaction.emoji==u'\N{RAISED FIST}':
                coupp = 'Pierre :fist:'
                if coup_bot==1:
                    coup = 'Pierre :fist:'
                elif coup_bot==2:
                    coup = "Feuille :raised_hand:"
                elif coup_bot==3:
                    coup = "Ciseaux :scissors:"
            elif res.reaction.emoji==u'\N{RAISED HAND}':
                coupp = "Feuille :raised_hand:"
                if coup_bot==1:
                    coup = "Feuille :raised_hand:"
                elif coup_bot==2:
                    coup = "Ciseaux :scissors:"
                elif coup_bot==3:
                    coup = "Pierre :fist:"
            elif res.reaction.emoji==u'\N{BLACK SCISSORS}':
                coupp = "Ciseaux :scissors:"
                if coup_bot==1:
                    coup = "Ciseaux :scissors:"
                elif coup_bot==2:
                     coup = "Pierre :fist:"
                elif coup_bot==3:
                     coup = "Feuille :raised_hand:"
            if coup_bot==1:
                    resultat = "Egalité"
            elif coup_bot==2:
                resultat = "J'ai gagné !"
            elif coup_bot==3:
                resultat = "J'ai perdu ..."
            em = discord.Embed(title="Shifumi de "+message.author.name, colour=0x0f00ff)
            em.add_field(name="Vous avez joué :", value=coupp, inline=None)
            em.add_field(name="J'ai joué :", value=str(coup), inline=None)
            em.add_field(name='Résultat :',value = str(resultat), inline=None)
            await botahn.edit_message(msgembed, embed=em)
            try:
                await botahn.clear_reactions(msgembed)
            except:
                pass
        
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
                    if nbr >=0 and nbr <=100:
                        nbrrr = nbrrr+1
                        if nbr==nombre_deviner:
                            em = discord.Embed(title=None, colour=0x0f005f)
                            em.add_field(name="Jeu du plus ou moins", value="Bien joué ! Je pensais bien à `" + str(nbr) + "`\nNombre de coups : `" +str(nbrrr) + "`", inline=True)
                            await botahn.send_message(message.channel, embed=em)
                            verif=1
                        elif nbr < nombre_deviner:
                            await botahn.send_message(message.channel,"Et non,mon nombre est plus grand !")
                        elif nbr> nombre_deviner:
                            await botahn.send_message(message.channel,"Non ! Mon nombre est plus petit !")
                    else:await botahn.send_message(message.channel,"Le nombre doit être compris entre 0 et 100(inclus)")
                except: await botahn.send_message(message.channel,"Le nombre doit être compris entre 0 et 100(inclus)")

    ###AVATAR###
    elif message.content.startswith('/avatar'):
        try:
            member = message.mentions[0]
            em = discord.Embed(title=member.name, colour=0xff00af)
            em.set_image(url=member.avatar_url)
            em.add_field(name='Lien:',value=str(member.avatar_url),inline=True)
            await botahn.send_message(message.channel,embed =em)
        except:
            await botahn.send_message(message.channel,'''Une erreur est survenue''')

    ###ROULETTE RUSSE###
    elif message.content=='/roulette':
        return
        barillet = 6
        while True:
            if barillet == 6:
                lancement = str(input("Lance et continue la partie en appuyant sur Entrée "))
            if lancement == "":
                roulette = random.randint(1,barillet)
                tir = random.randint(1,barillet)
                if tir == roulette:
                    print ("BANG! Tu es mort!")
                    barillet = 6
                    continue
                else:
                    if barillet > 2:
                        barillet -= 1
                        lancement = str(input("Continue, tu es toujours en vie"))
                    else:
                        print ("Bien joué, cowboy!")
                        barillet = 6
                        continue
            else:
                print ("Commande invalide")
                continue
    ###USER###
    elif message.content.startswith("/user") :
        user = message.author
        data = open("vip.txt","r")
        liste = data.read().split('\n')
        data.close
        if user.id in liste : pass
        else:
            await botahn.send_message(message.channel,"Commande réservée aux VIP.")
            return
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
        if message.channel.name !='spam-bot' and message.channel.name !='bar' and message.channel.name !='commande-teste' and message.server.id!='442368373184266241' and message.server.id!='348759926442688513':
            await botahn.send_message(message.channel,'Je ne sers les clients que dans #spam-bot!')
        else:
            args = message.content.split(' ')
            if len(args) == 1 or len(args) > 4 or message.content =='/bar help':
                await botahn.send_message(message.channel,'''Si tu ne sais pas utiliser la commande,je te recommande de faire ```/bar drinklist|foodlist|randfood|randdrink|buy|offer <ID_de_l'objet pour buy et offer> <@Mention si offer>```''')
            elif len(args) ==2:
                if args[1]=='drinklist':
                    await botahn.send_message(message.channel,embed = emdrink)
                elif args[1] == 'foodlist':
                    await botahn.send_message(message.channel,embed = emfood)
                elif args[1]=='randfood':
                    data = open("food.txt","r")
                    liste = data.read().split('\n')
                    data.close
                    liste = liste[random.randint(0,len(liste)-1)]
                    await botahn.send_message(message.channel,"La sélection du chef pour <@"+message.author.id+">! Je te sers **"+liste+"**!")
                elif args[1]=='randdrink':
                    data = open("drink.txt","r")
                    liste = data.read().split('\n')
                    data.close
                    liste = liste[random.randint(0,len(liste)-2)]
                    await botahn.send_message(message.channel,"La sélection du barman pour <@"+message.author.id+">! Je te sers **"+liste+"**!")
                else:
                    await botahn.send_message(message.channel,'''Si tu ne sais pas utiliser la commande,je te recommande de faire ```/bar drinklist|foodlist|randfood|randdrink|buy|offer <ID_de_l'objet pour buy et offer> <@Mention si offer>```''')
            elif len(args)==3 and (args[1]== 'drinklist' or args[1]== 'foodlist' or args[1]== 'randfood' or args[1]== 'randdrink'):
                await botahn.send_message(message.channel,'''Si tu utilises `/bar drinklist|foodlist|randfood|randdrink`, tu ne dois pas mettre de 3ème argument''')
                return
            elif len(args)>=3:
                if args[1]=='buy' or args[1]=='offer':
                    try:
                        cho = int(args[2])
                        if cho>=50:
                            data = open("food.txt","r")
                            liste = data.read().split('\n')
                            data.close
                            liste = liste[cho-50]
                            if cho-50>len(liste)-1:
                                cho = int(args[1]) #création d'une erreur
                        elif cho<50 and cho>=0:
                            data = open("drink.txt","r")
                            liste = data.read().split('\n')
                            data.close
                            test = 2
                            if message.author.id =='205009003653103626': test = 1
                            if cho >len(liste)-test:
                                cho = int(args[1]) #création d'une erreur
                            liste = liste[cho]
                        else:
                            cho = int(args[1]) #création d'une erreur
                    except:
                        await botahn.send_message(message.channel,'ID incorrect')
                        return
                    if args[1]=='buy':
                        await botahn.send_message(message.channel,"Très bien <@"+str(message.author.id)+">! Je te sers **"+str(liste)+"**!")
                    else:
                        try:
                            user = message.mentions[0]
                            await botahn.send_message(message.channel,"<@"+str(message.author.id)+"> vous offre **"+str(liste)+"** <@"+str(user.id)+"> !")
                        except:
                            await botahn.send_message(message.channel,"Mention non valide")
                else:
                    await botahn.send_message(message.channel,'''Si tu ne sais pas utiliser la commande,je te recommande de faire ```/bar drinklist|foodlist|randfood|randdrink|buy|offer <ID_de_l'objet pour buy et offer> <@Mention si offer>```''')

    ###contrôle Botahn WIP###
    elif message.content.startswith('/msgsend ') and message.author.id =='205009003653103626':
        msg = message.content.replace('/msgsend ','')
        await botahn.send_message(message.channel,msg)

    ###TEASER###
    elif message.content=="/teaser":
        texte = await botahn.send_message(message.channel,"La fonction /profil qui était teasé a été terminée et implantée")
        em= discord.Embed(title="Roulette Russe de "+message.author.name,description = "Il reste encore **4** places dans le barillet. :grin: pour continuer ou :rage: pour poser le pistolet",colour = 0x008f00)
        em.set_footer(text="Ce message est un teaser, le résultat peut différer. Il sera supprimé dans 60 secondes")
        texte_2 = await botahn.send_message(message.channel,embed = em)
        await asyncio.sleep(60)
        await botahn.delete_message(texte)
        await botahn.delete_message(texte_2)


    ###profil de quelqu'un###
    elif message.content.startswith("/profil"):
        try:
            user = message.mentions[0]
            test=0
        except:
            user = message.author
            test=1
        try:
            nomfichier = "z"+user.id+".txt"
            data = open(nomfichier,"r")
            liste = data.read().split('\n')
            data.close
            profiltxt = liste[2]
            profil = profiltxt.split('_')
            for i in range(0,len(profil)-1):
                if profil[i]==' ':
                    profil[i]='aucun'
            em = discord.Embed(title="Le personnage de "+user.name,colour = 0x9f0000)
            em.add_field(name="Chapeau :",value=profil[0],inline=True)
            em.add_field(name="Collier :",value=profil[1],inline=True)
            em.add_field(name="Haut :",value=profil[2],inline=True)
            em.add_field(name="Bas :",value=profil[3],inline=True)
            em.add_field(name="Chaussures :",value=profil[4],inline=True)
            em.add_field(name="Accessoire :",value=profil[5],inline=True)
            em.add_field(name="Pokemon :", value = profil[6], inline=True)
            em.add_field(name="Argent :",value=liste[1]+"€",inline = False)
            em.set_footer(text="Vous ne pouvez personnaliser votre profil pour l'instant, fonction en travail")
            await botahn.send_message(message.channel,content = None,tts = None,embed = em)
        except:
            try:
                data = open(nomfichier,"r")
                liste = data.read().split('\n')
                data.close
                data = open(nomfichier,"w")
                try:
                    data.write(str(liste[0]) +'\n'+str(liste[1])+"\n"+str(liste[2]))
                except:
                    try:
                        data.write(str(liste[0]) +'\n'+str(liste[1])+"\n"+" _ _ _ _ _ _ _")
                    except:
                        await botahn.send_message(message.channel,"Tapez /money et réessayez ensuite")
                data.close
                await botahn.send_message(message.channel,"Retapez la commande s'il vous plaît")
            except:
                await botahn.send_message(message.channel,"La personne concernée n'a pas de compte.")
            
    ###Système d'argent###
    elif message.content.startswith('/admingive ') and message.author.id =='205009003653103626':
        give = int(message.content.split(' ')[1])
        user = message.mentions[0]
        nomfichier = "z"+user.id+".txt"
        data = open(nomfichier,"r")
        liste = data.read().split('\n')
        data.close
        data = open(nomfichier,"w")
        try:
            data.write(str(liste[0]) +'\n'+str(int(liste[1])+give)+"\n"+str(liste[2]))
        except:
            data.write(str(liste[0]) +'\n'+str(int(liste[1])+give)+"\n"+" _ _ _ _ _ _ _")
        data.close
        await botahn.send_message(message.channel,user.mention +" a reçu "+str(give)+"€ de la part de "+message.author.name)
        
    elif message.content=='/vipbuy':
        user = message.author
        data = open("vip.txt","r")
        liste = data.read().split('\n')
        data.close
        if user.id in liste :
            await botahn.send_message(message.channel,"Vous êtes déjà un VIP "+message.author.mention)
            return
        else:
            pass
        try:
            nomfichier = "z"+message.author.id+".txt"
            data = open(nomfichier,"r")
            liste = data.read().split('\n')
            data.close
            money = int(liste[1])
            if 3000>money:
                await botahn.send_message(message.channel,"Vous n'avez pas assez d'argent pour devenir VIP "+message.author.mention +". Cela coûte 3000€")
                return
            else:
                money = money-3000
                data = open("vip.txt","a")
                data.write('\n' + message.author.id)
                data.close()
                await botahn.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")
                em = discord.Embed(title="Botahn Bank",description = "Bravo ! Vous êtes désormais VIP et il vous reste encore **"+str(money)+"€** sur votre compte.",colour = 0xffff00)
                await botahn.send_message(message.channel,embed = em)
                data = open(nomfichier,"w")
                try:
                    data.write(str(liste[0]) +str(money)+str(liste[2]))
                except:
                    data.write(str(liste[0]) +"\n"+str(money)+"\n"+" _ _ _ _ _ _ _")

                data.close
        except:
            await botahn.send_message(message.channel,"Vous n'avez pas de compte, tapez `/create` pour en créer un !")
            
    elif message.content.startswith("/money"):
        try:
            user = message.mentions[0]
            test=0
        except:
            user = message.author
            test=1
        try:
            nomfichier = "z"+user.id+".txt"
            data = open(nomfichier,"r")
            liste = data.read().split('\n')
            data.close
            em = discord.Embed(title = "Botahn Bank",description = "Votre compte contient actuellement "+liste[1]+"€ <@"+user.id+">.",colour = 0xffff00)
            await botahn.send_message(message.channel,embed = em)
        except:
            if test == 1:pass
            else:
                await botahn.send_message(message.channel,"Cet utilisateur n'a pas de compte.")
                return
            await botahn.send_message(message.channel,"Vous n'avez pas de compte, tapez `/create` pour en créer un !")

    elif message.content =='/reset':
        try:
            nomfichier = "z"+message.author.id+".txt"
            data = open(nomfichier,"r")
            data.close
            em = discord.Embed(title=":warning: ATTENTION "+message.author.name+" :warning:", description = "Êtes vous sûr de vouloir réinitialiser votre compte ? En cas de bug ou de problème sur votre profil, ils seront résolus mais vous perdrez toute votre progression.",colour = 0xff0000)
            msgreset = await botahn.send_message(message.channel,embed = em)
            await botahn.add_reaction(msgreset, u"\N{THUMBS UP SIGN}")
            await botahn.add_reaction(msgreset, u"\N{THUMBS DOWN SIGN}")
            res = await botahn.wait_for_reaction([u'\N{THUMBS UP SIGN}',u'\N{THUMBS DOWN SIGN}'],user = message.author,message = msgreset)
            if res.reaction.emoji ==u'\N{THUMBS UP SIGN}':
                data = open(nomfichier,"w")
                data.write("0\n200\n" +" _ _ _ _ _ _ _")
                data.close
                await botahn.edit_message(msgreset, embed = discord.Embed(title="Votre compte a bien été réinitialisé "+message.author.name,colour = 0xff0000))
            else:
                await botahn.edit_message(msgreset,embed = discord.Embed(title = "Votre compte n'a pas été réinitialisé "+message.author.name,colour = 0xff0000))
            try:
                await botahn.clear_reactions(msgreset)
            except:
                pass
        except:
            await botahn.send_message(message.channel,"Vous n'avez pas de compte, tapez `/create` pour en créer un !")
            
    elif message.content== '/create':
        try:
            nomfichier = "z"+message.author.id+".txt"
            data = open(nomfichier,"r")
            data.close
            await botahn.send_message(message.channel, 'Tu as déjà un compte à la Botahn Bank')
        except:
            nomfichier = "z"+message.author.id+".txt"
            data = open(nomfichier,"w")
            data.write("0\n200\n" +" _ _ _ _ _ _ _")
            data.close
            em = discord.Embed(title="Botahn Bank",description = "Votre compte à la Botahn Bank a bien été ouvert et a été crédité de 200€ <@"+message.author.id+">.",colour = 0xffff00)
            await botahn.send_message(message.channel,embed = em)
            
    elif message.content=='/daily':
        try:
            nomfichier = "z"+message.author.id+".txt"
            data = open(nomfichier,"r")
            liste = data.read().split('\n')
            data.close
            if time.time()-float(liste[0])>86400:
                em = discord.Embed(title="Botahn Bank",description = "Votre compte à été crédité de **100€** . Vous possédez désormais **"+str(int(liste[1])+100)+"**€ <@"+message.author.id+">.",colour = 0xffff00)
                data = open(nomfichier,"w")
                try:
                    data.write(str(time.time()) +"\n"+str(int(liste[1])+100)+"\n"+liste[2])
                except:
                    data.write(str(time.time()) +"\n"+str(int(liste[1])+100)+"\n"+" _ _ _ _ _ _ _ _")
                data.close
                await botahn.send_message(message.channel,embed=em)
            else:
                attente = int(86400-(math.floor(time.time()-float(liste[0]))))
                heure = 0
                minute = 0
                while attente >=3600:
                    attente = attente -3600
                    heure = heure+1
                while attente >=60:
                    attente = attente -60
                    minute = minute +1
                heure = str(heure)+"h " 
                minute = str(minute)+"m "
                attente = str(attente)+"s"
                attente = heure + minute + attente
                await botahn.send_message(message.channel,"Vous ne pouvez gagner vos intérêts qu'une fois par jour, veuillez réessayer dans "+attente+" "+message.author.mention)
        except:
            await botahn.send_message(message.channel,"Vous n'avez pas de compte, tapez `/create` pour en créer un !")

###ERREUR###
@botahn.event
async def on_error(event, *args, **kwargs):
    try:
        micmicro = await botahn.get_user_info('205009003653103626')
        message= args[0]
        liste = [0x9f0000,0x00ff00]
        embed = discord.Embed(title="Erreur", description="```PYTHON\n{0}```".format(traceback.format_exc()), color=liste[random.randint(0,1)])
        embed.set_footer(text="Ce message sera supprimé dans 30 secondes", icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTicNxqDxGeWo0URJ1PjEISifmY0-YyWTg5udTqkrgyAbqMFyGMpQ')
        embed.set_image(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR0Frh2G8z3mMXJkNm3RCEiH2yY8gEHbhFsITuyz8CIFW-aQcT')
        trace=await botahn.send_message(message.channel, embed=embed)
        await botahn.send_message(micmicro,embed = embed)
        await botahn.send_message(micmicro,message.content)
        await asyncio.sleep(30)
        try:
            await botahn.delete_message(trace)
        except:
            pass
    except:
        pass

botahn.run("TOKEN")
###COMMANDE DE LANCEMENT DU BOT###



