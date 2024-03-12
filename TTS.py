from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup 
from edge_tts import VoicesManager
import time, re , edge_tts


bot = Client("TTS Bot",api_id=21832338, 
              api_hash="3d11dad763458ea9b7ab106d6fc5e7ce",
              bot_token="7018791817:AAEmSO0Y9JmwFsFwjKXFUFZbBras4K0II0Y")


botusers = {}

class User:
    Inst = []
    def __init__(self,userid,username):
        self.userid = userid
        self.username = username
        self.wordsleft = 500
        self.premium_status = False
        self.selectedvoice = "en-US-SteffanNeural"
        User.Inst.append(self)

    def ChangeVoice(self,voice):
        self.selectedvoice = voice

    def is_premium(self):
        return self.premium_status

    def ChangePremium(self,value):
        self.premium_status = value 

    def get_user(obj):
        return obj


Language_menu = [   
                    ['English','Spanish','French'],
                    ['Mandarin', 'Russian', 'Arabic'],
                    ['Amharic','More languages']             
                ]
Amh_lang_menu = [ ['Ameha','Mekdes'] ]
Rus_lang_menu = [ ['Dmitry','Svetlana'] ]
Fre_lang_menu = [ ['Henri','Denise'] ]




# Functions 

async def TTS(bot,message):
    await message.reply("processing")
    voices = await VoicesManager.create()
    user = User.get_user(botusers.get(message.from_user.id))
    voice= user.selectedvoice
    communicate = edge_tts.Communicate(message.text, voice)
    await communicate.save('voice.mp3') 
    await bot.send_voice(message.chat.id,"voice.mp3",caption=f'{voice}') 
    user.wordsleft = user.wordsleft - len(message.text.split())


# Triggers

@bot.on_message(filters.private & (filters.command("start") or filters.command("Start")))
def Greetuser(bot,message):    
    id = message.from_user.id
    try:
         name = message.from_user.first_name + ' ' +message.from_user.last_name
    except:
         try:
              name = message.from_user.first_name
         except:
              name = 'User'+ str(id)    
    if id in botusers:        
        user = User.get_user(botusers.get(id))         
        match = re.findall(r'-(\w+)Neural', user.selectedvoice)
        message.reply(f"Dear {user.username} Welcome \n words left : {user.wordsleft} \n selected voice : {match[0]}")
    else :
        message.reply("Welcome")
        botusers[id] = User(id,name)
        print(botusers)

@bot.on_message(filters.private & (filters.command("lang") | filters.command("language")))
def ChangeLanguage(bot,message):
    text = "Select your prefered language."
    Lang_Menu = ReplyKeyboardMarkup(Language_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Language")
    message.reply(text=text, reply_markup = Lang_Menu )

# amharic

@bot.on_message(filters.private & filters.regex('Amharic'))
def AmharicMenu(bot,message):
    text = "Ok Now, select your prefered voice"
    Lang_Menu =ReplyKeyboardMarkup(Amh_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
    message.reply(text=text, reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.regex('Ameha'))
def setAmeha(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("am-ET-AmehaNeural")
    message.reply("Language Succesfully changed")
    
@bot.on_message(filters.private & filters.regex('Mekdes'))
def setMekdes(bot,message):    
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("am-ET-MekdesNeural")
    message.reply("Language Succesfully changed")

# russian

@bot.on_message(filters.private & filters.regex("Russian"))
def RussianMenu(bot,message):
    text = "Ok Now, select your prefered voice"
    Lang_Menu =ReplyKeyboardMarkup(Rus_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
    message.reply(text=text, reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.regex('Dmitry'))
def setDmitry(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("ru-RU-DmitryNeural")
    message.reply("Language Succesfully changed")

@bot.on_message(filters.private & filters.regex('Svetlana'))
def setSvetlana(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("ru-RU-SvetlanaNeural")
    message.reply("Language Succesfully changed")

# french 
    
@bot.on_message(filters.private & filters.regex('French'))
def FrenchMenu(bot,message):
    text = "Ok Now, select your prefered voice"
    Lang_Menu =ReplyKeyboardMarkup(Fre_lang_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Voice")
    message.reply(text=text, reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.regex('Henri'))
def setHenri(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("fr-FR-HenriNeural")
    message.reply("Language Succesfully changed")    

@bot.on_message(filters.private & filters.regex('Denise'))
def setDenise(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))         
    user.ChangeVoice("fr-FR-DeniseNeural")
    message.reply("Language Succesfully changed")



@bot.on_message(filters.private & filters.regex('More languages'))
def MoreLang(bot,message):
    message.reply("Coming Soon . . .")


@bot.on_message(filters.private & filters.text)
async def TextToSpeech(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))
    if user.wordsleft > len(message.text.split()): 
        await TTS(bot,message)
    else :
        await message.reply("I'm sorry you don't have enough words left for today , Try again tomorrow")




       






print("tts running")
bot.run()


