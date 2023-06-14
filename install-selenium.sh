#!/bin/bash

#https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2#step-2-install-latest-chrome-for-linux

#echo "Changing to home directory..."
#pushd "$HOME"

echo "Update the repository and any packages..."
sudo apt update && sudo apt upgrade -y

echo "Install prerequisite packages..."
sudo apt install wget curl unzip -y

echo "Download the latest Chrome .deb file..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

echo "Install Google Chrome..."
sudo dpkg -i google-chrome-stable_current_amd64.deb

echo "Fix dependencies..."
sudo apt --fix-broken install -y

chrome_version=($(google-chrome-stable --version))
echo "Chrome version: ${chrome_version[2]}"

chromedriver_version=$(curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
echo "Chromedriver version: ${chromedriver_version}"
if [ "${chrome_version[2]}" == "$chromedriver_version" ]; then
    echo "Compatible Chromedriver is available..."
    echo "Proceeding with installation..."
else
    echo "Compabible Chromedriver not available...exiting"
    echo "Run: (see comment in code"
    # sometimes you have to add -1 after version: ex. ...-stable_114.0.5735.90-1_amd64.deb insted of -stable_114.0.5735.90_amd64.deb

    #  Check available versions here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable

#wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
 # && apt install -y /tmp/chrome.deb --allow-downgrades \
 # && rm /tmp/chrome.deb
    exit 1
fi

echo "Downloading latest Chromedriver..."
curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/${chromedriver_version}/chromedriver_linux64.zip"

echo "Unzip the binary file and make it executable..."
mkdir -p "chromedriver/stable"
unzip -q "chromedriver_linux64.zip" -d "chromedriver/stable"
chmod +x "chromedriver/stable/chromedriver"

echo "Install Selenium..."
python3 -m pip install selenium

#popd
