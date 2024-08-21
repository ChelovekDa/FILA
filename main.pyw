from os import path
import telebot
from Backend import util, file, folder, Path, disk

settings = util().getConfig()
token = settings["token"]
bot = telebot.TeleBot(token, parse_mode="HTML")

# static base
MAX_SIZE_FILE_SEND = 49

rcon = [settings["RCON"], "5038489915"]
directory = util().getBaseFolder()

def check(message: telebot.types.Message) -> bool:
    if (str(message.from_user.id) in rcon):
        return True
    else:
        return False

def updateConfig() -> None:
    global settings
    settings = util().getConfig()

def checkIsFiles(message: telebot.types.Message) -> None:
    global directory

    if (Path(f"{directory.toStr()}{util().getSep(directory.toStr())}{message.text}")).isDir() == False:
        print(Path(f"{directory.toStr()}{message.text}").toStr())
        bot.send_message(message.chat.id, settings["baseMessage"],
                         reply_markup=toMarkUp(file(message.text).getListButtons()))
        directory = Path(directory.toStr() + f"/{message.text}")
    else:
        dir = folder(message.text).openFolder(directory)
        directory = dir
        getDir(message)

def toMarkUp(list: list[str], backButton: bool = True) -> telebot.types.ReplyKeyboardMarkup:
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if (backButton == True):
        markup.add("...")
    for i in range(len(list)):
        markup.add(list[i])
    return markup

@bot.message_handler(commands=["get"])
def getDir(message) -> None:
    global directory
    if (check(message)):
        try:
            bot.send_message(message.chat.id, settings["baseMessage"], reply_markup=toMarkUp(directory.getMarkupListOfDir()))
        except:
            directory = util().getBaseFolder()
            bot.send_message(message.chat.id, "<b>В процессе выполнения команды возникла ошибка!</b>\n"
                                              "Для избежания дальнейших ошибок, Ваша директория была изменена на стандартную.\n"
                                              f"\n{settings['baseMessage']}", reply_markup=toMarkUp(directory.getMarkupListOfDir()))

@bot.message_handler(commands=["dir"])
def printDir(message) -> None:
    if (check(message)):
        bot.send_message(message.chat.id, directory.toStr())

@bot.message_handler(commands=["id"])
def getID(message) -> None:
    bot.send_message(message.chat.id, str(message.from_user.id))

@bot.message_handler(commands=["update"])
def update(message) -> None:
    updateConfig()

@bot.message_handler(content_types=["text"])
def textDec(message) -> None:
    global directory
    print(directory.toStr())

    if (check(message)):

        if (message.text == "..."):
            if (disk().isDisk(directory.toStr())):
                bot.send_message(message.chat.id, text=settings["baseMessage"],
                                 reply_markup=toMarkUp(disk().getListButtons(), False))
            else:
                directory = Path(directory.getPrevDir())
                if (directory.toStr() == "C:"):
                    bot.send_message(message.chat.id, text=settings["baseMessage"],
                                     reply_markup=toMarkUp(disk().getListButtons(), False))
                    return
                getDir(message)

        elif ("|" in message.text):
            if (message.text == "|Send-File|"):
                if (disk().byteToMB(path.getsize(directory.toStr())) >= int(settings["maxSizeFileSend"])):
                    bot.send_message(message.chat.id, f"<b>Вес данного файла превышает установленный максимум!</b>\n"
                                                      f"Отправка данного файла имеет слишком высокий риск возникновения ошибки, из-за его веса!\n"
                                                      f"\n{settings['baseMessage']}")
                    directory = Path(directory.getPrevDir())
                    getDir(message)
                    return
                else:
                    try:
                        file = open(directory.toStr(), "rb")
                        bot.send_document(message.chat.id, document=file)
                    except:
                        bot.send_message(message.chat.id, "<b>В процессе отправки файла возникла ошибка!</b>\n"
                                                          "В процессе отправки данного файла возникла непредвиденная ошибка, но системе удалось <b>временно</b> нейтрализовать ее.\n"
                                                          "Во избежание дальнейших ошибок и нарушений работы бота, рекомендуется отказаться от отправки данного файла и обратиться к создателю бота!\n"
                                                          f"{settings['baseMessage']}")
                    finally:
                        file.close()
                        directory = Path(directory.getPrevDir())
                        getDir(message)

            elif disk().isDisk(message.text.split(" | ")[0]):
                directory = Path(disk().getDisk(message.text.split(" | ")[0]))
                getDir(message)
                return
        else:
            try:
                checkIsFiles(message)
            except:
                getDir(message)

bot.polling(none_stop=True)
