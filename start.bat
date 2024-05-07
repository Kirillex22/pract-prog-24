@echo off
call myvenv/Scripts/activate
@pause
pip install -r requirements.txt
streamlit run labs/lab2/rb_tree/Main.py