from os import path
import telebot
from Backend import Util, file, folder, Path, disk

settings = Util().get_config()
token = settings["token"]
bot = telebot.TeleBot(token, parse_mode="HTML")

# static base
MAX_SIZE_FILE_SEND = 49

rcon = [settings["RCON"]]
directory = Util().getBaseFolder()

def check(message: telebot.types.Message) -> bool:
    if (str(message.from_user.id) in rcon):
        return True
    else:
        return False

def updateConfig() -> None:
    global settings
    settings = Util().get_config()

def checkIsFiles(message: telebot.types.Message) -> None:
    global directory

    if (Path(f"{directory.toStr()}{Util().getSep(directory.toStr())}{message.text}")).is_dir() == False:
        print(Path(f"{directory.toStr()}{message.text}").toStr())
        bot.send_message(message.chat.id, settings["baseMessage"],
                         reply_markup=to_markup(file(message.text).getListButtons()))
        directory = Path(directory.toStr() + f"/{message.text}")
    else:
        dir = folder(message.text).openFolder(directory)
        directory = dir
        get_dir(message)

def to_markup(list: list[str], backButton: bool = True) -> telebot.types.ReplyKeyboardMarkup:
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if (backButton == True):
        markup.add("...")
    for i in range(len(list)):
        markup.add(list[i])
    return markup

@bot.message_handler(commands=["get"])
def get_dir(message) -> None:
    global directory
    if check(message):
        try:
            bot.send_message(message.chat.id, settings["baseMessage"], reply_markup=to_markup(
                directory.get_markup_list_dir()))
        except:
            directory = Util().getBaseFolder()
            bot.send_message(message.chat.id, "<b>В процессе выполнения команды возникла ошибка!</b>\n"
                                              "Для избежания дальнейших ошибок, Ваша директория была изменена на стандартную.\n"
                                              f"\n{settings['baseMessage']}", reply_markup=to_markup(
                directory.get_markup_list_dir()))

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
                                 reply_markup=to_markup(disk().getListButtons(), False))
            else:
                directory = Path(directory.get_prev_dir())
                if (directory.toStr() == "C:"):
                    bot.send_message(message.chat.id, text=settings["baseMessage"],
                                     reply_markup=to_markup(disk().getListButtons(), False))
                    return
                get_dir(message)

        elif "|" in message.text:
            if message.text == "|Send-File|":
                if disk().byteToMB(path.getsize(directory.toStr())) >= int(settings["maxSizeFileSend"]):
                    bot.send_message(message.chat.id, f"<b>Вес данного файла превышает установленный максимум!</b>\n"
                                                      f"Отправка данного файла имеет слишком высокий риск возникновения ошибки, из-за его веса!\n"
                                                      f"\n{settings['baseMessage']}")
                    directory = Path(directory.get_prev_dir())
                    get_dir(message)
                    return
                else:
                    file = None
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
                        directory = Path(directory.get_prev_dir())
                        get_dir(message)

            elif disk().isDisk(message.text.split(" | ")[0]):
                directory = Path(disk().getDisk(message.text.split(" | ")[0]))
                get_dir(message)
                return
        else:
            try:
                checkIsFiles(message)
            except:
                get_dir(message)

bot.polling(none_stop=True)
