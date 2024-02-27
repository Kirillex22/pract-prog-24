@echo off
call myvenv/Scripts/activate
@pause
pip install -r requirements.txt
jupyter notebook