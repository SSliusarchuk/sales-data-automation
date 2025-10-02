@echo off

REM --- запуск першого скрипта ---
"C:\Users\Admin\Desktop\auto\venv\Scripts\python.exe" "C:\Users\Admin\Desktop\auto\scripts\generate_data.py"

REM --- запуск другого скрипта ---
"C:\Users\Admin\Desktop\auto\venv\Scripts\python.exe" "C:\Users\Admin\Desktop\auto\scripts\load_to_db.py"

pause
