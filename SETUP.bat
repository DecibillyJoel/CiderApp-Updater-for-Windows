python -m pip install requests

set TARGET='%CD%\Cider Updater.py'
set ICON='%CD%\icon.ico';
set WORKINGDIRECTORY='%CD%'
set SHORTCUT='%CD%\Cider Updater.lnk'
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.TargetPath = %TARGET%; $S.IconLocation = %ICON%; $S.WorkingDirectory = %WORKINGDIRECTORY%; $S.Save()"

set STARTUP_FILE="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Cider Updater.lnk"
copy /v /y "Cider Updater.lnk" %STARTUP_FILE%

pause