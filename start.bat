@echo off
call myvenv/Scripts/activate
@pause
pip install -r requirements.txt
streamlit run labs/lab3/Main.py