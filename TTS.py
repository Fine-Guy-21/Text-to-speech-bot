from pyrogram import Client, filters , enums
from pyrogram.types import ReplyKeyboardMarkup 
from edge_tts import VoicesManager
import time , re , edge_tts


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

async def TTS(bot,message):
    await bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    time.sleep(2)
    mes = await message.reply("Reading Text . . .")
    voices = await VoicesManager.create()
    user = User.get_user(botusers.get(message.from_user.id))
    time.sleep(3)    
    await bot.edit_message_text(message.chat.id,mes.id," Checking the selected voice ") 
    voice= user.selectedvoice
    try:
        await bot.send_chat_action(message.chat.id,enums.ChatAction.RECORD_AUDIO)    
        communicate = edge_tts.Communicate(message.text, voice)
        await communicate.save('voice.mp3') 
        await bot.send_chat_action(message.chat.id,enums.ChatAction.UPLOAD_AUDIO)        
        match = re.findall(r'-(\w+)Neural', user.selectedvoice)
        await bot.delete_messages(message.chat.id,mes.id)
        await bot.send_voice(message.chat.id,"voice.mp3",caption=f"{match[0]}'s voice") 
        if user.premium_status == False:
            user.wordsleft = user.wordsleft - len(message.text.split())
    except:
        await bot.delete_messages(message.chat.id,mes.id)
        await message.reply("There is an error in the input please try again")
        


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

@bot.on_message(filters.private & filters.regex('Back'))
def GoBackMenu(bot,message):
    Lang_Menu = ReplyKeyboardMarkup(Language_menu,one_time_keyboard=True, resize_keyboard=True,placeholder="Choose Language")
    message.reply(text=" Select language ", reply_markup = Lang_Menu )

@bot.on_message(filters.private & filters.command("stat"))
def Greetuser(bot,message):    
    id = message.from_user.id
    if id in botusers:        
        user = User.get_user(botusers.get(id))         
        match = re.findall(r'-(\w+)Neural', user.selectedvoice)
        message.reply(f""" User : {user.username}\n words left : {user.wordsleft} \n selected voice : {match[0]} \n premium : {user.premium_status}""")

@bot.on_message(filters.private & filters.regex('chgprem'))
def PromoteDemote (bot,message):
    user = User.get_user(botusers.get(message.from_user.id))
    if user.premium_status == False:
        user.ChangePremium(True)
    else:
        user.ChangePremium(False)
                    
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("am-ET-AmehaNeural")
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Mekdes'))
async def setMekdes(bot,message):    
    if message.text == 'Mekdes':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("am-ET-MekdesNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("ru-RU-DmitryNeural")
        await message.reply("Language Succesfully changed")
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Svetlana'))
async def setSvetlana(bot,message):
    if message.text == 'Svetlana':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("ru-RU-SvetlanaNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("fr-FR-HenriNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Denise'))
async def setDenise(bot,message):
    if message.text == 'Denise':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("fr-FR-DeniseNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("es-ES-AlvaroNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Elvira'))
async def setElvira(bot,message):
    if message.text == 'Elvira':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("es-ES-ElviraNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("en-US-SteffanNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Jenny'))
async def setJenny(bot,message):
    if message.text == 'Jenny':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("en-US-JennyNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("zh-CN-YunjianNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Xiaoxiao'))
async def setXiaoxiao(bot,message):
    if message.text == 'Xiaoxiao':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("zh-CN-XiaoxiaoNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("ar-Ae-HamdanNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Fatima'))
async def setFatima(bot,message):
    if message.text == 'Fatima':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("ar-Ae-FatimaNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("de-DE-ConradNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Amala'))
async def setAmala(bot,message):
    if message.text == 'Amala':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("de-DE-AmalaNeural")
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
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("en-US-AnaNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)

@bot.on_message(filters.private & filters.regex('Neerja'))
async def setNeerja(bot,message):
    if message.text == 'Neerja(Eng Indian)':
        user = User.get_user(botusers.get(message.from_user.id))         
        user.ChangeVoice("en-IN-NeerjaNeural")
        await message.reply("Language Succesfully changed")    
    else:
        await TTS(bot,message)


# the text
        
@bot.on_message(filters.private & filters.text)
async def TextToSpeech(bot,message):
    user = User.get_user(botusers.get(message.from_user.id))
    if user.wordsleft > len(message.text.split()): 
        await TTS(bot,message)
    else :
        await message.reply("I'm sorry you don't have enough words left for today , Try again tomorrow")




       






print("tts running")
bot.run()


