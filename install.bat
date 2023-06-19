git clone https://github.com/Jakub-Nnoli/NoteAppProject.git
cd NoteAppProject
del install.bat
del README.md
rmdir .git
rmdir __pycache__
pip install -r requirements.txt
call NoteApp.bat
