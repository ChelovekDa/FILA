For this script starting to work, you must be create special file "config" in directory with other .py script.
See as must be look you config file:

    baseDir$
    token$
    RCON$
    baseMessage$
    maxSizeFileSend$

1) **baseDir$** - This must be used for you base directory for work with bot. *This VERY important argument.*
2) **token$** - This's bot token. You can get his from [@BotFather](https://t.me/BotFather) in Telegram. *This VERY important argument.*
3) **RCON$** - Functions:
     *1)* If in process of working bot was appered a error, that all messages of error was be sending to this user.
     *2)* If you don't append to this argument, you can't use this bot. But on this argument you cant write only one user. If you want to append more, you must write them in code. _(main.pyw, line 12)_
     *This VERY important argument.*
4) **baseMessage$** - Message which bot will be send on every bot message. *Can be empty*
5) **maxSizeFileSend$** - Amount of MB weight which bot can send to you. ***WARNING! You can edit this argument, but I can't advise this to you. Bots in Telegram cant send more then 50 MB file weight and edit this argument can be call a error!*** *Can be empty, but in code stay static limit of 49 MB file weight*

*INFO:* One bot - one computer.
The end.
