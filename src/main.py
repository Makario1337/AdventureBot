import sqlite3
import discord
import json
import os
from datetime import datetime, timedelta
import random

# VERSION 1.0.2

config = json.load(open('config.json'))

con = sqlite3.connect("sqlite.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS USERS
    (
    userid INTEGER PRIMARY KEY,
    username VARCHAR,
    last_message DATETIME,
    xp INTEGER
    );""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS LEVELS
    (
    level INTEGER PRIMARY KEY,
    xp_needed INTEGER
    );""")

for level in range(250):
    cur.execute(f'''
        INSERT OR REPLACE INTO LEVELS 
        ("level", "xp_needed")
        VALUES
        ('{int(level)+1}','{(int(level)+1)*1000}')
        ;''')

con.commit()
con.close()

def DatabaseConnection(lSQL):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    query = cur.execute(lSQL).fetchall()
    con.commit()
    con.close()
    return query

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        await self.change_presence(activity=discord.Game(name=f"{config['prefix']}help"))
    
    async def on_message(self, message):
        lSQL =f'''SELECT * FROM USERS WHERE USERID = '{message.author.id}';'''
        user = DatabaseConnection(lSQL)
        if (message.author.bot == True): return

        if not user: 
            lSQL= f'''
                INSERT INTO USERS
                ("userid", "username", "last_message", "xp")
                VALUES 
                (
                    '{message.author.id}','{message.author.name}','{datetime.now()}','{random.randrange(1, 100)}'
                );'''
            DatabaseConnection(lSQL)
        else:
            if (datetime.strptime(user[0][2], f'%Y-%m-%d %H:%M:%S.%f') < datetime.now() - timedelta(minutes=1)):
                lSQL=f'''
                    UPDATE USERS SET XP = XP + {random.randrange(1, 100)}, last_message = '{datetime.now()}'  WHERE USERID = '{user[0][0]}';
                '''
                DatabaseConnection(lSQL)
        
        if(message.content.lower() == f"{config['prefix']}xp"):
            lSQL =f'''SELECT * FROM USERS WHERE USERID = '{message.author.id}';'''
            user = DatabaseConnection(lSQL)
            xp = user[0][3]
            lvl = f'''SELECT * FROM LEVELS WHERE xp_needed >= {xp} ORDER BY level ASC LIMIT 1'''
            current_level = DatabaseConnection(lvl)
            aktuelles_level = current_level[0][0]
            xp_needed_for_next_level = current_level[0][1]
            await message.channel.send(f"""Dein aktuelles Level ist: {aktuelles_level} mit {xp} XP.\nDu brauchst noch {xp_needed_for_next_level - xp} XP für das nächste Level!\nFrohes Chatten!""")
        
        if(message.content.lower() == f"{config['prefix']}top"):
            lSQL =f'''SELECT * FROM USERS ORDER BY XP DESC LIMIT 5;'''
            top5 = DatabaseConnection(lSQL)
            top5list = ""
            i = 1
            for entry in top5:  
                top5list = top5list + f"{i}. {entry[1]} - {entry[3]}xp.\n"
                i += 1
            await message.channel.send(top5list)

        if(message.content.lower() == f"{config['prefix']}help"):
            await message.channel.send("Folgende Befehle sind verfügbar: \n!xp - Zeigt dein aktuelles Level/Xp und wie viel du noch brauchst um aufzusteigen.\n!top - Zeigt die Top 5 Benutzer.")


intents = discord.Intents.default()
intents.message_content = True


client = MyClient(intents=intents)
client.run(config['token'])