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
SERVICE_FILE="$PROJECT_DIR/backend/systemd/snownavi-flask.service"
ENV_FILE="$PROJECT_DIR/backend/.env"
SYSTEMD_DIR="/etc/systemd/system"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo -e "${YELLOW}Creating default .env file...${NC}"
  cat > "$ENV_FILE" << EOF
FLASK_SECRET_KEY=change-this-to-a-random-string
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
ALLOWED_EMAILS=okboy2008@gmail.com
EOF
  echo -e "${YELLOW}Please update $ENV_FILE with your actual configuration values.${NC}"
fi

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
  echo -e "${YELLOW}Installing python3-venv...${NC}"
  apt-get update
  apt-get install -y python3-venv
fi

# Remove existing virtual environment if it exists but is incomplete
if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/pip" ]; then
  echo -e "${YELLOW}Removing incomplete virtual environment...${NC}"
  rm -rf "$VENV_DIR"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo -e "${YELLOW}Creating virtual environment...${NC}"
  python3 -m venv "$VENV_DIR"

  # Verify virtual environment was created successfully
  if [ ! -f "$VENV_DIR/bin/pip" ]; then
    echo -e "${RED}Failed to create virtual environment. Please check your Python installation.${NC}"
    exit 1
  fi
fi

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
"$VENV_DIR/bin/python" -m pip install --upgrade pip

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/backend/requirements.txt"

# Check if server.py exists
SERVER_FILE="$PROJECT_DIR/backend/server.py"
if [ ! -f "$SERVER_FILE" ]; then
  echo -e "${RED}Error: server.py not found at $SERVER_FILE${NC}"
  exit 1
fi

# Fix permissions
echo -e "${YELLOW}Setting correct permissions...${NC}"
chown -R lighthouse:lighthouse "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"
chmod 644 "$ENV_FILE"
chmod 755 "$SERVER_FILE"

# Copy service file to systemd directory
echo -e "${YELLOW}Setting up systemd service...${NC}"
cp "$SERVICE_FILE" "$SYSTEMD_DIR/snownavi-flask.service"
systemctl daemon-reload

# Enable and start the service
echo -e "${YELLOW}Enabling and starting the service...${NC}"
systemctl enable snownavi-flask.service
systemctl restart snownavi-flask.service || {
  echo -e "${RED}Failed to start the service. Check the logs with: journalctl -u snownavi-flask.service${NC}"
  exit 1
}

# Check service status
echo -e "${YELLOW}Checking service status...${NC}"
systemctl status snownavi-flask.service

echo -e "${GREEN}=== Setup complete! ===${NC}"
echo -e "${GREEN}The SnowNavi Flask Server has been successfully set up and started.${NC}"
echo -e "${YELLOW}Configuration file: $ENV_FILE${NC}"
echo -e "${YELLOW}Service status: systemctl status snownavi-flask.service${NC}"
echo -e "${YELLOW}View logs: journalctl -u snownavi-flask.service${NC}"
echo -e "${YELLOW}Restart service: systemctl restart snownavi-flask.service${NC}"
echo -e "${YELLOW}Server URL: http://localhost:8899${NC}"
echo -e "${GREEN}Remember to configure Nginx to proxy requests to the Flask server.${NC}"
