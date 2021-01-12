@echo off
cls
echo This batch file keeps the python script running when there is an error!
title Bot Anticrash
:StartBot
start /wait python bot.py
echo (%time%) Bot closed/crashed... restarting!
goto StartBot