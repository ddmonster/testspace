@REM @echo off

@REM set /p message="Enter message: "
./.venv/scripts/activate
cd src
alembic revision --autogenerate -m "setup"
alembic upgrade head
