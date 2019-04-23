# -*- coding: utf-8 -*-
import os
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

    #채널 목록 얻어오기
    lt = list()
    for chain in app.get_all_channels():
            lt.append(chain)
    #돌림판 초기 설정
    default_list = ['알파','하틴','루인스','탐방','나캄','샤미','찰리','파이남','부캠','브라보','캄퐁','독스','라카위','몽나이','카오','하늘정원']
    tmp_list = default_list        
            
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
            mslt.append(str(ms.nick))
        tmp = list()
        num = 1
        while mslt:
            if len(mslt)<n:
                await app.send_message(message.channel,str(num)+"팀 "+str(mslt))
                await app.send_message(message.channel,"===========================================")
                break;
            else:        
                while len(tmp) != n:
                    lg = len(mslt)
                    tmp.append(mslt.pop(rd.randint(0,lg-1)))
                await app.send_message(message.channel,str(num)+"팀 "+str(tmp))
                await app.send_message(message.channel,"===========================================")
                tmp = []
            num +=1
    if message.content == ("!돌림판"):
        f = open("test.txt",'r')
        tmp_list = f.read().split()
        f.close()   
        await app.send_message(message.channel,tmp_list[rd.randint(0,len(tmp_list)-1)])

    else:
        if message.content.startswith("!돌림판"):
            command = message.content.split()[1]

            if command == '초기화':
                f = open("test.txt",'w')
                for word in default_list:
                    f.write(word)
                    f.write(" ")
                f.close()
                await app.send_message(message.channel,"초기화 완료")
            
            elif command == '목록':
                f = open("test.txt",'r')
                tmp_list = f.read().split()
                f.close()
                await app.send_message(message.channel,tmp_list)
            elif command == ('추가'):
                words = message.content.split()[2:]
                f = open("test.txt",'a')
                t = open("test.txt",'r')
                tm_list = t.read().split()
                t.close()
                for word in words:
                    if word in tm_list:
                        await app.send_message(message.channel,"목록에 존재합니다 " + word)
                        continue
                    f.write(word+" ")
                f.close()
            elif command == ('삭제'):
                words = message.content.split()[2:]
                t = open("test.txt",'r')
                read_list = t.read().split()
                t.close()
                for word in words:
                    if word in read_list:
                        read_list.remove((word))
                        continue
                    await app.send_message(message.channel,"존재하지 않습니다 " + word)
                    
                f = open("test.txt",'w')
                for word in read_list:
                    f.write(word)
                    f.write(" ")
                f.close()



'''
 if message.content.startswith("!돌림판"):
        command = message.content.split()[1]
        maplt = ['알파','하틴','루인스','탐방','나캄','샤미','찰리','파이남','부캠','브라보','캄퐁','독스','라카위','몽나이','카오','하늘정원']
        if command == ('골라줘'):
            await app.send_message(message.channel,maplt.pop(rd.randint(0,len(maplt)-1)))
            maplt = ['알파','하틴','루인스','탐방','나캄','샤미','찰리','파이남','부캠','브라보','캄퐁','독스','라카위','몽나이','카오','하늘정원']
        elif command == '목록':
            await app.send_message(message.channel,maplt)
'''

    
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



