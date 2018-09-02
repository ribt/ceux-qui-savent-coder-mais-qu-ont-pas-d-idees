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

def int_to_bytes(x):
    return list(x.to_bytes((x.bit_length() + 7) // 8, 'big'))