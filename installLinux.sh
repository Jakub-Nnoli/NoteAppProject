#!/bin/bash
git clone https://github.com/Jakub-Nnoli/NoteAppProject.git
sudo chmod -R 777 NoteAppProject
cd NoteAppProject
rm installWindows.bat
rm NoteApp.bat
rm installLinux.sh
rm README.md
git remote remove origin
rm -rf .git
rm -rf __pycache__
pip install -r requirements.txt
python database_modules.py
./NoteApp.sh
