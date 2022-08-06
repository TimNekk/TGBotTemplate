@echo off
title Database Migration
call venv\Scripts\activate.bat

SET /P name=Enter revision name: 

alembic revision -m "%name%" --autogenerate --head head
echo Revision "%name%" created!

set "reply=y"
set /p "reply=Update Database? y/n: "
if /i not "%reply%" == "y" goto :eof

alembic upgrade head
echo Database updated!

pause