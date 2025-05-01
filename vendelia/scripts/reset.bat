@echo off

REM Move to project root
cd /d %~dp0\..

REM Test for virtual environment
IF "%VIRTUAL_ENV%"=="" (
    echo Error: Virtual Environment not active.
    exit /b 1
)

REM Delete migration files and DB
echo Deleting migration files and DB
for /R marketplace\migrations %%f in (*.py) do (
    if not "%%~nxf"=="__init__.py" del "%%f"
)
for /R marketplace\migrations %%f in (*.pyc) do del "%%f"
del /f /q db.sqlite3 2>nul

REM Run migrations
echo Running migrations
call python manage.py makemigrations
call python manage.py migrate

REM Create debug superuser if -a flag is passed
IF "%1"=="-a" (
    echo Creating debug superuser: admin::admin
    echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.admin', 'admin') | python manage.py shell
)

echo Operation complete.
