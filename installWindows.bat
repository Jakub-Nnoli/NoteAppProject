git clone https://github.com/Jakub-Nnoli/NoteAppProject.git
cd NoteAppProject
del installWindows.bat
del installLinux.sh
del NoteApp.sh
del README.md
git remote remove origin
rmdir /s /q .git
rmdir /s /q __pycache__
pip install -r requirements.txt
python .\database_modules.py
.\NoteApp.bat
