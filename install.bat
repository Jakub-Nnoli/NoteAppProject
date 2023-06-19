git clone https://github.com/Jakub-Nnoli/NoteAppProject.git
cd NoteAppProject
del install.bat
del README.md
git remote remove origin
rmdir /s /q .git
rmdir /s /q __pycache__
pip install -r requirements.txt
call NoteApp.bat
