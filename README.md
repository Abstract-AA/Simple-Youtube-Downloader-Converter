# YTGrab


This is a GTK based youtube video downloader. I created this yt-dlp frontend because I wanted a simple tool to download videos and songs. Playlist download is also supported. 

Due to the mimalistic design, the interface can blend well with multiple desktop enviroments. The main inspiration for the design is Rhythmbox. 


![Alt Text](https://github.com/Abstract-AA/YTGrab/blob/b344d19539b43c7a0b9f88d559c06263751e7d5b/Screenshot%20From%202025-08-16%2000-46-00.png)


## Features

- **Instant download** - save any song with a single click
- **Suports conversion to mp3 files** - Any video can be downloaded and converted
- **Playlists** - Playlist download is also supported
- **Sstraightforward UI** - Easy to use, without any bloat

## 📦 Installation

First, to install the dependencies run the following in a system with Bash:

```bash
sudo apt install yt-dlp pygobject         # Debian/Ubuntu
sudo dnf install yt-dlp pygobject         # Fedora and its derivatives
sudo apk add mpv yt-dlp pygobject         # Alpine Linux
sudo pacman -S yt-dlp pygobject           #Arch linux and its derivatives

```
Then, move on to downloading the main file.

```bash
wget https://github.com/Abstract-AA/Simple-Youtube-Downloader-Converter/blob/be991b230006cbf7fbda72af1c970644b698d3cd/yoump3gtk.py

python3 yoump3gtk.py

```

Note: Some distributions have older versions of yt-dlp, and this can cause issues when running the app. Therefore, in this case its ideal to download the latest version of yt-dlp in a python enviroment, and then run the script:

```bash
# ====== INSTALL LATEST yt-dlp ON ARCH / FEDORA / DEBIAN/UBUNTU ======

# === 0. PREREQUISITES ===
# Make sure Python and pip are installed

sudo pacman -S python python-pip # Arch

sudo apt install python3 python3-pip # Debian/Ubuntu

sudo dnf install python3 python3-pip # Fedora

# === 1st METHOD: pipx (Recommended) ===

sudo pacman -S pipx # Arch

sudo apt install pipx # Debian/Ubuntu

sudo dnf install pipx # Fedora

pipx install yt-dlp  # Install yt-dlp via pipx

pipx upgrade yt-dlp # (To upgrade later)

# ====== 2nd METHOD: virtualenv (Manual isolation) ======

pip install --user virtualenv # Install virtualenv if needed

python3 -m venv yt-dlp-env
source yt-dlp-env/bin/activate  # Create and activate virtual environment

pip install yt-dlp # Install yt-dlp inside the venv

deactivate # Deactivate environment when done

```

## Legal Disclaimer & Ethical Use

This project, is provided for **educational and personal use only**. By using this software, you acknowledge and agree to the following:

1. **Content Access**: This tool uses `yt-dlp` to stream audio content from public sources. It does not host, distribute, or modify any copyrighted content.

2. **Fair Use**: Intended for personal, non-commercial use under principles of fair use (Section 107 of the U.S. Copyright Act). Commercial use is strictly prohibited.

3. **Copyright Compliance**: Users are responsible for ensuring they have the right to access any content they stream or download. Respect all applicable copyright laws in your jurisdiction.

4. **No Warranty**: The developer assumes no liability for misuse of this tool or copyright infringement by end users.

**Important**: YouTube's Terms of Service prohibit unauthorized access to their content. This tool is not affiliated with or endorsed by YouTube, or any content providers.

Consult legal counsel if uncertain about compliance in your region.

Furthermore, by using this software, the user should understand and agree to:
- Support artists through official platforms
- Use this tool only for content you legally own or have rights to access
- Not redistribute downloaded content
