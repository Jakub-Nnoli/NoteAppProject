#!/bin/bash
git clone https://github.com/Jakub-Nnoli/NoteAppProject.git
cd NoteAppProject
rm installWindows.bat
rm NoteApp.bat
rm installLinux.sh
rm README.md
git remote remove origin
rm -rf .git
rm -rf __pycache__
pip install -r requirements.txt
./NoteApp.sh
