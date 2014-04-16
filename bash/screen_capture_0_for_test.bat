::@ECHO off
ECHO hello world!!
::PAUSE
::IF %ERRORLEVEL% NEQ 0 ECHO hello world
CutyCapt --url=http://www.adagetechnologies.com --out=adagetechnologies.com.png
IF %ERRORLEVEL% NEQ 0 ECHO failed.
echo %errorlevel%
Pause