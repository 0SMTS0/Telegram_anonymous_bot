import telebot
from telebot import types
from telebot.types import ReactionTypeEmoji
from telebot.types import ReactionTypeEmoji
import hashlib





Allowed_Commands = ["/start","/list","/SstTAarRTtADMIN"]

Api_Token = '7407346257:AAHV5AtUqxWAWSZXMrheXTrJZgOLW7MOUNw'

bot = telebot.TeleBot(Api_Token)

Channel_Username = "@ScreamSilence0"

User_Links = {}

Active_Chats = {}

User_Id_Hash = {}

User_First_Name = {}


@bot.message_handler(commands=['start'])
def Check_Membership(M):

    Chat_Id = M.chat.id

    User_Id = M.from_user.id

    print(f"{User_Id} -----> {M.from_user.first_name} Started the Bot .")

    print("-----------------")


    if "start " in M.text:
        
        Recived_Hash = M.text.split('start ')[1]
        
        Target_User_Id = User_Id_Hash[Recived_Hash]


        if User_First_Name.get(Recived_Hash):

            
            Target_First_Name = User_First_Name[Recived_Hash]
        

            if Chat_Id == int(Target_User_Id):

                bot.send_message(chat_id=Chat_Id, text="You can't send a message to yourself!")

                bot.set_message_reaction(chat_id=Chat_Id, message_id=M.message_id, reaction=[ReactionTypeEmoji(emoji='😐')])

                return


            Active_Chats[Chat_Id] = int(Target_User_Id)

            Active_Chats[int(Target_User_Id)] = Chat_Id



            bot.send_message(chat_id=Chat_Id, text=f"You connected {Target_First_Name} to send message:")

        else:
            
            if Chat_Id == int(Target_User_Id):

                bot.send_message(chat_id=Chat_Id, text="You can't send a message to yourself!")

                bot.set_message_reaction(chat_id=Chat_Id, message_id=M.message_id, reaction=[ReactionTypeEmoji(emoji='😐')])             

                return


            Active_Chats[Chat_Id] = int(Target_User_Id)

            Active_Chats[int(Target_User_Id)] = Chat_Id



            bot.send_message(chat_id=Chat_Id, text=f"You connected to send message:")



    else:

        
        try:

            Check_Joined_User = bot.get_chat_member(Channel_Username, User_Id)


            if Check_Joined_User.status in ["member", "administrator", "creator"]:

                Markup = types.InlineKeyboardMarkup()

                Link_Button = types.InlineKeyboardButton("Get my link", callback_data="Get_Link")

                List_Button = types.InlineKeyboardButton("List Item",callback_data="List_Item")

                Markup.add(Link_Button, List_Button) 

                bot.send_message(chat_id=M.chat.id, text="""It seems you have already joined to our channel so you can use the bot just now!
Here we have to good and intresting option in our bot for you:
                                 
1.First you can get your own link that your friends use that to just send you message in hidden shape.
                                 
2.Second you can just make a list of your friends links to message them in hidden shape everytime that you want.""", reply_markup=Markup)
                print(M.message.chat.id)


            else:

                MArkup = types.InlineKeyboardMarkup()


                Channel_Link_Button = types.InlineKeyboardButton("Join ScreamSilence 🔗",url="https://t.me/ScreamSilence0")

                Joined_Channel_Button = types.InlineKeyboardButton("I joined", callback_data="Joined_Channel")


                MArkup.add(Channel_Link_Button,Joined_Channel_Button, row_width=1)


                bot.send_message(chat_id=M.message.chat.id,text="""Hi, we are so happy that seems you are using our bot,
before starting you should just join to our channel.
                """, reply_markup=MArkup)



        except Exception as e:

            print(f"Error : {e}")

            return False



@bot.message_handler(func=lambda message: True)
def Send_Message(message):

    User_Name = message.from_user.first_name
    User_Name1 = message.from_user.username

    Message = message.text.replace(".", "\\.").replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("~", "\\~").replace("`", "\\`").replace(">", "\\>").replace("<", "\\<").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace("!", "\\!")
    
    Chat_Id = message.chat.id
    
    Markup = types.InlineKeyboardMarkup()

    User_Id = message.from_user.id

    Hash_Object = hashlib.md5(str(User_Id).encode())

    Unique_Id = Hash_Object.hexdigest()

    User_Id_Hash[Unique_Id] = User_Id

    Reply_Message = types.InlineKeyboardButton("Reply", url=f"https://t.me/Hidden0_Chat0_bot?start={Unique_Id}")
    
    Markup.add(Reply_Message)


    if Chat_Id in Active_Chats and Active_Chats[Chat_Id]:
        Target_Chat_Id = Active_Chats[Chat_Id] 

        if Target_Chat_Id in [6370572874, 5148092201]:

            bot.send_message(chat_id= Target_Chat_Id, text= f"""{User_Name} in Username \\@{User_Name1} sent a message to you :
                         
||{Message}||""", parse_mode="MarkdownV2", reply_markup=Markup)
    

            del Active_Chats[Target_Chat_Id]

            del Active_Chats[Chat_Id]   

            bot.send_message(chat_id=Chat_Id, text="""Your message sent!
Please restart the bot to use intresting options.""")
            
        else:

            bot.send_message(chat_id= Target_Chat_Id, text= f"""Someone sent a message to you :
                         
||{Message}||""", parse_mode="MarkdownV2", reply_markup=Markup)
    
        
            Markup = types.InlineKeyboardMarkup()
            Yes_Button = types.InlineKeyboardButton("Yes", callback_data="Reaction_Yes")
            No_Button = types.InlineKeyboardButton("No", callback_data="Reaction_No")
            Markup.add(Yes_Button,No_Button)
            bot.send_message(chat_id= Target_Chat_Id, text=f"Do you want to reaction his\her message?",Markup=Markup)
            
           



            del Active_Chats[Target_Chat_Id]

            del Active_Chats[Chat_Id]   

            bot.send_message(chat_id=Chat_Id, text="""Your message sent!
Please restart the bot to use intresting options.""")



        




    elif message.text.startswith("/") and message.text not in Allowed_Commands:

        bot.send_message(chat_id=message.chat.id, text="Please write the commands(/start,/list) to use the bot or connect yourself to someone link to message him/her.")


    elif  not message.text.startswith("/"):

        bot.send_message(chat_id=Chat_Id, text="Please first connect yourself to someone link to send message!")





@bot.callback_query_handler(func=lambda M:M.data == "Reaction_Yes")
def Reaction_Yes(M):
    Chat_Id = M.chat.id


    Markup = types.InlineKeyboardMarkup()
    Like_Re = types.InlineKeyboardButton("👍",callback_data="Like")
    Dislike_Re = types.InlineKeyboardButton("👎",callback_data="Dislike")
    Kiss_Re = types.InlineKeyboardButton("💋",callback_data="Kiss")
    Love_Re = types.InlineKeyboardButton("❤️",callback_data="Love")
    Smile_Re = types.InlineKeyboardButton("😁",callback_data="Smile")
    Markup.add(Like_Re,Dislike_Re,Kiss_Re,Love_Re,Smile_Re)
    bot.send_message(chat_id= Chat_Id, text="Here you can reaction to your contact message !", Markup=Markup)



@bot.callback_query_handler(func=lambda M:M.data in ["Like","DisLike","Kiss","Love","Smile"])
def Send_Reaction(M):

    if M.data == "Like":
        
    elif M.data == "Disslike":
        
    elif M.data == "Kiss":
        
    elif M.data == "Love":
        
    elif M.data == "Smile":
        






@bot.callback_query_handler(func=lambda M:M.data == "Joined_Channel")
def Joined_Channel(M):
        
    
    User_Id = M.from_user.id

    try:
        Check_Joined_User = bot.get_chat_member(Channel_Username, User_Id)


        if Check_Joined_User.status in ["member", "administrator", "creator"]:

            Markup = types.InlineKeyboardMarkup()

            Link_Button = types.InlineKeyboardButton("Get my link", callback_data="Get_link")

            List_Button = types.InlineKeyboardButton("List Item",callback_data="List_Item")

            Markup.add(Link_Button, List_Button) 

            bot.send_message(chat_id=M.message.chat.id, text="""It seems you have joined to our channel so you can use the bot just now!
Here we have to good and intresting option in our bot for you:
                             
1.First you can get your own link that your friends use that to just send you message in hidden shape.
                             
2.Second you can just make a list of your friends links to message them in hidden shape everytime that you want.""", reply_markup=Markup)
            
            print(M.message.chat.id)


        else:

            MArkup = types.InlineKeyboardMarkup()


            Channel_Link_Button = types.InlineKeyboardButton("Join ScreamSilence 🔗",url="https://t.me/ScreamSilence0")

            Joined_Channel_Button = types.InlineKeyboardButton("I joined", callback_data="Joined_Channel")


            MArkup.add(Channel_Link_Button,Joined_Channel_Button, row_width=1)


            bot.send_message(chat_id=M.message.chat.id,text="""You are not a member of the channel yet
To use the bot, you must be a member of the channel.
            """, reply_markup=MArkup)



    except Exception as e:

        print(f"Error : {e}")

        return False





@bot.callback_query_handler(func=lambda M: M.data == "Get_Link")
def Get_Link(M):

    global First_Name
    First_Name = M.from_user.first_name

    User_Id = M.from_user.id

    Hash_Object = hashlib.md5(str(User_Id).encode())

    Unique_Id = Hash_Object.hexdigest()

    User_Id_Hash[Unique_Id] = User_Id

    User_First_Name[Unique_Id] = First_Name  # "ADFADfasdfadsfaadsfadfasdf" = "Ali"

    Unique_Link = f"https://t.me/Hidden0_Chat0_bot?start={Unique_Id}"

    

    bot.send_message(chat_id=User_Id, text=f"""So now, You can use your link.
Just give your link to your friends to message you in hidden Shape.
{Unique_Link}""", disable_web_page_preview=True)







bot.infinity_polling()