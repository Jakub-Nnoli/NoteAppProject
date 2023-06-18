FROM python:3
COPY database_modules.py necessary_dialogs.py start_window.py text_editor_window.py user_notes_window.py /app/
COPY __pycache__ /app/__pycache__
COPY NotepadDatabase.db /app/
COPY Icons /app/Icons
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx
CMD ["python", "start_window.py"]
