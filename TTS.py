from pyrogram import Client, filters , enums
from pyrogram.types import ReplyKeyboardMarkup 
from edge_tts import VoicesManager
import time , re , edge_tts , mysql.connector


bot = Client("TTS Bot",api_id=21832338, 
              api_hash="3d11dad763458ea9b7ab106d6fc5e7ce",
              bot_token="7018791817:AAEmSO0Y9JmwFsFwjKXFUFZbBras4K0II0Y")


botusers = {}

Conn = mysql.connector.connect(
    host='localhost',
    user='root',
    port='3307',
    password='cityzens',
    database='TTSBotDB'
)
print(Conn)
Cur = Conn.cursor()

class User:
    Inst = []
    def __init__(self,userid,username):
        self.userid = userid
        self.username = username
        self.wordsleft = 500
        self.premium_status = False
        self.selectedvoice = "en-US-SteffanNeural"
        User.Inst.append(self)

    def is_premium(self):
        return self.premium_status

    def ChangePremium(self,value):
        self.premium_status = value 

    def get_user(obj):
        return obj



Language_menu = [   
                    ['English','Spanish','French'],
                    ['Mandarin', 'Russian', 'Arabic'],
                    ['German','Amharic','More languages']             
                ]

Amh_lang_menu = [ ['Ameha','Mekdes'], ['Back'] ]
Rus_lang_menu = [ ['Dmitry','Svetlana'], ['Back'] ]
Fre_lang_menu = [ ['Henri','Denise'], ['Back'] ]
Spa_lang_menu = [ ['Alvaro','Elvira'], ['Back'] ]
Eng_lang_menu = [ ['Steffan','Jenny'], ['Back'] ]
man_lang_menu = [ ['Yunjian','Xiaoxiao'], ['Back'] ]
Ara_lang_menu = [ ['Hamdan','Fatima'], ['Back'] ]
Ger_lang_menu = [ ['Conrad','Amala'], ['Back']]
ml_lang_menu = [ ['Ana(Eng Child)','Neerja(Eng Indian)'], ['Back'] ]



# Functions 

# async def TTS(bot,message):
#     await bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
#     time.sleep(2)
#     mes = await message.reply("Reading Text . . .")
#     voices = await VoicesManager.create()
#     user = Get_User(message.from_user.id)
#     time.sleep(3)    
#     await bot.edit_message_text(message.chat.id,mes.id," Checking the selected voice ") 
#     voice= user.selectedvoice
#     try:
#         await bot.send_chat_action(message.chat.id,enums.ChatAction.RECORD_AUDIO)    
#         communicate = edge_tts.Communicate(message.text, voice)
#         await communicate.save('voice.mp3') 
#         await bot.send_chat_action(message.chat.id,enums.ChatAction.UPLOAD_AUDIO)        
#         match = re.findall(r'-(\w+)Neural', user.selectedvoice)
#         await bot.delete_messages(message.chat.id,mes.id)
#         await bot.send_voice(message.chat.id,"voice.mp3",caption=f"{match[0]}'s voice") 
#         if user.premium_status == False:
#             user.wordsleft = user.wordsleft - len(message.text.split())
#     except:
#         await bot.delete_messages(message.chat.id,mes.id)
#         await message.reply("There is an error in the input please try again")

async def TTS(bot,message):
    await bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    time.sleep(2)
    mes = await message.reply("Reading Text . . .")
    voices = await VoicesManager.create()    
    user = Get_User(message.from_user.id)
    time.sleep(3)    
    if user :
        await bot.edit_message_text(message.chat.id,mes.id," Checking the selected voice ") 
        voice= user[4]
        try:
            await bot.send_chat_action(message.chat.id,enums.ChatAction.RECORD_AUDIO)    
            communicate = edge_tts.Communicate(message.text, voice)
            await communicate.save('voice.mp3') 
            await bot.send_chat_action(message.chat.id,enums.ChatAction.UPLOAD_AUDIO)        
            match = re.findall(r'-(\w+)Neural', user[4])
            await bot.delete_messages(message.chat.id,mes.id)
            await bot.send_voice(message.chat.id,"voice.mp3",caption=f"{match[0]}'s voice") 
            if user[3] == 0:
                wl = int(user[2]) - len(message.text.split())
                Cur.execute(f"update User set wordsleft = {wl} where id= {user[0]};")
                Conn.commit()
        except:
            await bot.delete_messages(message.chat.id,mes.id)
            await message.reply("There is an error in the input please try again")

def Get_User(id):
    Cur.execute(f'select * from User where id={id}')
    result = Cur.fetchall()
    if result:
        for res in result:
            time.sleep(1)
        return res
    else:
        return None

def Manage_User(message):

        Cur.execute(f'select * from User where id={message.from_user.id}')
        result = Cur.fetchall()        
        if result:
            for res in result:
                print(res)
                message.reply(f"Welcome Dear `{res[1]}`")
        else:
            uid = message.from_user.id
            name = f"User{uid}"
            sv = 'en-US-SteffanNeural'
            msg = f"Insert into User(id, username,wordsleft,premium_status,selected_voice) values({uid},'{name}',300 ,False,'{sv}');"
            Cur.execute(msg)
            Conn.commit() 
            message.reply(f"Welcome To Fine TTS Dear {name}")

def ChangeVoice(voice,uid):
    Cur.execute(f"update User set selected_voice = '{voice}' where id = {uid} ")
    Conn.commit()

    

# Triggers

@bot.on_message(filters.private & (filters.command("start") or filters.command("Start")))
def Greetuser(bot,message):    
    Manage_User(message)
    
@bot.on_message(filters.private & (filters.command("lang") | filters.command("language")))
def ChangeLanguage(bot,message):
    text = "Select your prefered language."
    Lang_Menu = ReplyKeyboardMarkup(Language_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Language")
    message.reply(text=text, reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.regex('Back'))
def GoBackMenu(bot,message):
    Lang_Menu = ReplyKeyboardMarkup(Language_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Language")
    message.reply(text=" Select language ", reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.command("stat"))
def Greetuser(bot,message):    
    id = message.from_user.id
    try:
        name = message.from_user.first_name
    except:
        name = f"User{id}"
    user = Get_User(message.from_user.id)
     
    if user:
        wl = str(user[2])        
        match = re.findall(r'-(\w+)Neural', user[4])
        if user[3] == 0:
            prem = "False"
        else:
            prem = "True"
            wl = "♾"
        message.reply(f"""\n ID:  `{user[1]}` \n\n Name :  `{name}`\n\n Words left :  `{wl}` \n\n selected voice :  `{match[0]}` \n\n premium :  `{prem}`   """)

# @bot.on_message(filters.private & filters.regex('chgprem'))
# def PromoteDemote (bot,message):
#     user = Get_User(message.from_user.id)
#     if user.premium_status == False:
#         user.ChangePremium(True)
#     else:
#         user.ChangePremium(False)
                    
# amharic

@bot.on_message(filters.private & filters.regex('Amharic'))
async def AmharicMenu(bot,message):
    if message.text == 'Amharic':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Amh_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message) 

@bot.on_message(filters.private & filters.regex('Ameha'))
async def setAmeha(bot,message):
    if message.text == 'Ameha':
        ChangeVoice("am-ET-AmehaNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Mekdes'))
async def setMekdes(bot,message):    
    if message.text == 'Mekdes':
        ChangeVoice("am-ET-MekdesNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

# russian

@bot.on_message(filters.private & filters.regex("Russian"))
async def RussianMenu(bot,message):
    if message.text == 'Russian':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Rus_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Dmitry'))
async def setDmitry(bot,message):
    if message.text == 'Dmitry':
        ChangeVoice("ru-RU-DmitryNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Svetlana'))
async def setSvetlana(bot,message):
    if message.text == 'Svetlana':
        ChangeVoice("ru-RU-SvetlanaNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

# french 
    
@bot.on_message(filters.private & filters.regex('French'))
async def FrenchMenu(bot,message):
    if message.text == 'French':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Fre_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Henri'))
async def setHenri(bot,message):
    if message.text == 'Henri':
        ChangeVoice("fr-FR-HenriNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Denise'))
async def setDenise(bot,message):
    if message.text == 'Denise':
        ChangeVoice("fr-FR-DeniseNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

# spanish
    
@bot.on_message(filters.private & filters.regex('Spanish'))
async def SpanishMenu(bot,message):
    if message.text == 'Spanish':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Spa_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Alvaro'))
async def setAlvaro(bot,message):
    if message.text == 'Alvaro':
        ChangeVoice("es-ES-AlvaroNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Elvira'))
async def setElvira(bot,message):
    if message.text == 'Elvira':
        ChangeVoice("es-ES-ElviraNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

# english
    
@bot.on_message(filters.private & filters.regex('English'))
async def EnglishMenu(bot,message):
    if message.text == 'English':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Eng_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Steffan'))
async def setSteffan(bot,message):
    if message.text == 'Steffan':
        ChangeVoice("en-US-SteffanNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Jenny'))
async def setJenny(bot,message):
    if message.text == 'Jenny':
        ChangeVoice("en-US-JennyNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

# mandarin
    
@bot.on_message(filters.private & filters.regex('Mandarin'))
async def MandarinMenu(bot,message):
    if message.text == 'Mandarin':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(man_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)
    
@bot.on_message(filters.private & filters.regex('Yunjian'))
async def setYunjian(bot,message):
    if message.text == 'Yunjian':
        ChangeVoice("zh-CN-YunjianNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Xiaoxiao'))
async def setXiaoxiao(bot,message):
    if message.text == 'Xiaoxiao':
        ChangeVoice("zh-CN-XiaoxiaoNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)
    
# arabic

@bot.on_message(filters.private & filters.regex('Arabic'))
async def ArabicMenu(bot,message):
    if message.text == 'Arabic':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Ara_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Hamdan'))
async def setHamdan(bot,message):
    if message.text == 'Hamdan':
        ChangeVoice("ar-Ae-HamdanNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Fatima'))
async def setFatima(bot,message):
    if message.text == 'Fatima':
        ChangeVoice("ar-Ae-FatimaNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

# german

@bot.on_message(filters.private & filters.regex('German'))
async def GermanMenu(bot,message):
    if message.text == 'German':
        text = "Ok Now, select your prefered voice"
        Lang_Menu =ReplyKeyboardMarkup(Ger_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
        await message.reply(text=text, reply_markup = Lang_Menu )
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Conrad'))
async def setConrad(bot,message):
    if message.text == 'Conrad':
        ChangeVoice("de-DE-ConradNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Amala'))
async def setAmala(bot,message):
    if message.text == 'Amala':
        ChangeVoice("de-DE-AmalaNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

# more language

@bot.on_message(filters.private & filters.regex('More languages'))
async def MoreLang(bot,message):
    if message.text == 'More languages':
        ml_Menu = ReplyKeyboardMarkup(ml_lang_menu,one_time_keyboard=True,resize_keyboard=True,placeholder="Explore other languages")
        await message.reply(text= "More languages Coming Soon . . .", reply_markup = ml_Menu)
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Ana'))
async def setAna(bot,message):
    if message.text == 'Ana(Eng Child)':
        ChangeVoice("en-US-AnaNeural",message.from_user.id)
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Neerja'))
async def setNeerja(bot,message):
    if message.text == 'Neerja(Eng Indian)':
        ChangeVoice("en-IN-NeerjaNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)


# the text
        
@bot.on_message(filters.private & filters.text)
async def TextToSpeech(bot,message):
    user = Get_User(message.from_user.id)
    if user:
        if user[2] > len(message.text.split()): 
            await TTS(bot,message)
        else :
            await message.reply("I'm sorry you don't have enough words left for today , Try again tomorrow")
    else:
        await message.reply()




       






print("tts running")
bot.run()


