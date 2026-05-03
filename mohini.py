#!/bin/bash
# ============================================
# 🎙️ HARI VOICE RECORDING TOOL
# Termux Tool - Auto Server + Chrome Open
# ============================================

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear

echo -e "${CYAN}"
echo "    ██╗  ██╗ █████╗ ██████╗ ██╗"
echo "    ██║  ██║██╔══██╗██╔══██╗██║"
echo "    ███████║███████║██████╔╝██║"
echo "    ██╔══██║██╔══██║██╔══██╗██║"
echo "    ██║  ██║██║  ██║██║  ██║██║"
echo "    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝"
echo -e "${NC}"
echo -e "${CYAN}    🎙️ VOICE RECORDING TOOL${NC}"
echo -e "${YELLOW}    ─────────────────────────${NC}"
echo ""

if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}📦 Python install ho raha hai...${NC}"
    pkg install python -y
fi

if ! python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}📦 Flask install ho raha hai...${NC}"
    pip install flask
fi

mkdir -p hari.txt

echo -e "${YELLOW}🧹 Purana server clean ho raha hai...${NC}"
pkill -f "python app.py" 2>/dev/null
sleep 1

echo -e "${GREEN}🚀 HARI Voice Server start ho raha hai...${NC}"
python app.py &
SERVER_PID=$!

sleep 3

IP=$(ifconfig 2>/dev/null | grep -oE 'inet [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | grep -v '127.0.0.1' | head -1 | awk '{print $2}')
if [ -z "$IP" ]; then
    IP="localhost"
fi

URL="http://${IP}:5000"

echo ""
echo -e "${GREEN}✅ SERVER READY!${NC}"
echo -e "${CYAN}────────────────────────────────────${NC}"
echo -e "${YELLOW}🌐 URL: ${GREEN}${URL}${NC}"
echo -e "${YELLOW}📊 Admin: ${GREEN}http://localhost:5000/admin${NC}"
echo -e "${CYAN}────────────────────────────────────${NC}"
echo ""

if command -v termux-open &> /dev/null; then
    echo -e "${YELLOW}🌐 Chrome open ho raha hai...${NC}"
    termux-open "$URL"
fi

echo -e "${CYAN}🎙️ Voice Recording Active!${NC}"
echo -e "${YELLOW}💡 Recordings 'hari.txt' folder mein save honge${NC}"
echo -e "${RED}⚠️  Ctrl+C dabayein to stop hoga${NC}"
echo ""

wait $SERVER_PID
