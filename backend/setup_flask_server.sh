#!/bin/bash

# Exit on error
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up SnowNavi Flask Server...${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root or with sudo${NC}"
  exit 1
fi

# Define paths
PROJECT_DIR="/home/lighthouse/git/snownavi_website"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_FILE="$PROJECT_DIR/backend/snownavi-flask.service"
SYSTEMD_DIR="/etc/systemd/system"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo -e "${YELLOW}Creating virtual environment...${NC}"
  python3 -m venv "$VENV_DIR"
fi

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/backend/requirements.txt"

# Copy service file to systemd directory
echo -e "${YELLOW}Setting up systemd service...${NC}"
cp "$SERVICE_FILE" "$SYSTEMD_DIR/snownavi-flask.service"
systemctl daemon-reload

# Enable and start the service
echo -e "${YELLOW}Enabling and starting the service...${NC}"
systemctl enable snownavi-flask.service
systemctl restart snownavi-flask.service

# Check service status
echo -e "${YELLOW}Checking service status...${NC}"
systemctl status snownavi-flask.service

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}You can check the logs with: journalctl -u snownavi-flask.service${NC}"
