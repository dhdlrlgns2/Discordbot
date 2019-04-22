# -*- coding: utf-8 -*-

import asyncio
import discord
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random as rd


app = discord.Client() # 디코 대신 app으로 바로 되도록 설정

token = "NTY1ODE2ODE5MzExNzA2MTIy.XK79ew.iGcERrpDXjKJgQPWE6Vwy8Cf23E"

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("===========")
    #봇이 플레이중인 게임
    await app.change_presence(game=discord.Game(name="엉덩이춤 추기",type=1))

#봇 작동 구역
@app.event
async def on_message(message):
    lt = list()
    for chain in app.get_all_channels():
            lt.append(chain)
            
            
    if message.author.bot:
        return None #봇 메세지 무시
    if message.content.startswith("!춤춰"):
        await app.send_message(message.channel,"부리부리")
    if message.content.startswith("!전적"):
        
        if(not(str(message.channel)==str(lt[9])) ): 
            await app.send_message(message.channel,"전적 검색 방을 이용해주세요.")
        else:
            await app.send_message(message.channel,"이번 시즌 스쿼드 기준입니다")
            junjuk = message.content.split()
            
            html = urlopen("https://dak.gg/profile/" + junjuk[1]+"/pc-2018-03/kakao/squad")
            bsObject = BeautifulSoup(html,"html.parser")
            
            lt = list()
            for link in bsObject.find_all('dd'):
                lt.append(link.text.strip())
            try:
                embed = discord.Embed(title=junjuk[1]+"의 스쿼드 전적",description=lt[0]+"\n"+"K/D = "+lt[33]+"\n"+ "승률 = "+lt[19] + "\n" + "평균 딜량 = "+str(int(lt[51].replace(",",""))//int(lt[0].split(" ")[0])),color=0x00ff00)
                await app.send_message(message.channel, embed=embed)
            except:
                await app.send_message(message.channel,"아이디를 다시 확인해주세요.")
    if message.content == "!집합":
        if((message.author.roles[-1].position)>10):
            rlt = list()
            for chain in lt:
                if((chain.type)== (message.author.voice_channel.type)):
                    rlt.append(chain)
            moving = list()
            for i in range(len(rlt)):
                for mem in rlt[i].voice_members:
                    moving.append(mem)
            for tar in moving:
                await app.move_member(tar,message.author.voice_channel)
        else:
            await app.send_message(message.channel,"권한이 없습니다.")
    if message.content.startswith("!팀짜기"):
        n = int(message.content.split()[1])
        mslt = list()
        for ms in message.author.voice_channel.voice_members:
            mslt.append(ms.mention)
        tmp = list()
        while mslt:
            if len(mslt)<n:
                await app.send_message(message.channel,mslt)
                break;
            else:        
                while len(tmp) != n:
                    lg = len(mslt)
                    tmp.append(mslt.pop(rd.randint(0,lg-1)))
                await app.send_message(message.channel,tmp)
                tmp = []
    if message.content.startswith("!테스트"):
        
        await app.send_message(message.channel,(message.author.voice_channel))
        
    
@app.event
async def on_member_join(member):
    lt = list()
    for chain in app.get_all_channels():
            lt.append(chain)
    await app.send_message(lt[2], member.mention+ "님 알로항!")


@app.event
async def on_member_remove(member):
    lt = list()
    for chain in app.get_all_channels():
            lt.append(chain)
    await app.send_message(lt[2], member.mention+ "님 빠빠이!")
    
app.run(token)



