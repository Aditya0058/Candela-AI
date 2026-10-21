#!/bin/bash
set -e

color='\033[0;33m' # yellow
NC='\033[0m' # no color

echo -e "${color}Starting Candela-Agent-MVP Initialization${NC}"

# check required tools
echo "Checking prerequisites"
if ! command -v git &> /dev/null; then echo "////// Bruhhh!, Git is not installed."; exit 1; fi
if ! command -v python3 &> /dev/null; then echo "////// Bruhhh!, Python3 is not installed."; exit 1; fi
if ! command -v npm &> /dev/null; then echo "////// Bruhhhh!, Node.js/NPM is not installed."; exit 1; fi

echo -e "${color}:) :) Huurayyyy! Prerequisites met!${NC}"

if [ ! -d "Candela-Agent-MVP" ]; then
    echo -e "${color}Wait bro Downloading Candela...${NC}"
    git clone https://github.com/Aditya0058/Candela-Agent-MVP.git
    cd Candela-Agent-MVP
else
    echo -e "${color}you r smart Candela directory already exists! Updating...${NC}"
    cd Candela-Agent-MVP
    git pull
fi

# backend
echo -e "${color}Cloning completed ${NC}"
echo " "
echo -e "${color}Setting up Backend._._._._._${NC}"
cd Backend
echo -e "${color}for ur security i am using virtual environments ${NC}"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# database initialization if not exists
if [ ! -f "candela.db" ]; then
    echo -e "${color}hehhehehehe - Initializing database...${NC}"
    python init_db.py
fi
cd ..

echo -e "${color}Backend done ${NC}"
echo " "

# frontend
echo -e "${color}now setting up frontend${NC}"
cd Frontend
npm install
cd ..

echo -e "${color}Installation completed${NC}"
echo " "
echo -e " ${color} Let me start it for you, Launching Candela (remember MVP) ${NC}"
# start.py running
python3 start.py

