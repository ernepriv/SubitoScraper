#!/usr/bin/env python3
"""
Script per installare Google Chrome in un ambiente automatizzato.
Supporta Windows, macOS e Linux.
"""

import os
import platform
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
import shutil
from pathlib import Path

def is_chrome_installed():
    """Verifica se Chrome è già installato nel sistema."""
    system = platform.system().lower()
    
    if system == "windows":
        # Percorsi comuni di installazione di Chrome su Windows
        chrome_paths = [
            os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
        ]
        return any(os.path.exists(path) for path in chrome_paths)
    
    elif system == "darwin":  # macOS
        return os.path.exists("/Applications/Google Chrome.app")
    
    elif system == "linux":
        try:
            # Verifica se il comando 'google-chrome' è disponibile
            subprocess.run(["which", "google-chrome"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
    
    return False

def install_chrome():
    """Installa Google Chrome in base al sistema operativo."""
    system = platform.system().lower()
    
    print(f"Installazione di Google Chrome su {system}...")
    
    if system == "windows":
        # URL per il download dell'installer di Chrome per Windows
        chrome_url = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"
        installer_path = os.path.join(tempfile.gettempdir(), "chrome_installer.exe")
        
        # Download dell'installer
        print("Download dell'installer di Chrome...")
        urllib.request.urlretrieve(chrome_url, installer_path)
        
        # Esecuzione dell'installer in modalità silenziosa
        print("Esecuzione dell'installer...")
        subprocess.run([installer_path, "/silent", "/install"], check=True)
        
        # Pulizia
        os.remove(installer_path)
    
    elif system == "darwin":  # macOS
        # URL per il download di Chrome per macOS
        chrome_url = "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg"
        dmg_path = os.path.join(tempfile.gettempdir(), "googlechrome.dmg")
        
        # Download del DMG
        print("Download di Chrome per macOS...")
        urllib.request.urlretrieve(chrome_url, dmg_path)
        
        # Montaggio del DMG
        print("Montaggio del DMG...")
        mount_point = "/Volumes/Google Chrome"
        subprocess.run(["hdiutil", "attach", dmg_path], check=True)
        
        # Copia dell'app nella cartella Applications
        print("Installazione di Chrome...")
        subprocess.run(["cp", "-r", f"{mount_point}/Google Chrome.app", "/Applications/"], check=True)
        
        # Smontaggio del DMG
        print("Smontaggio del DMG...")
        subprocess.run(["hdiutil", "detach", mount_point], check=True)
        
        # Pulizia
        os.remove(dmg_path)
    
    elif system == "linux":
        # Rileva la distribuzione Linux
        try:
            with open("/etc/os-release") as f:
                os_release = f.read()
            
            # Debian/Ubuntu
            if "debian" in os_release.lower() or "ubuntu" in os_release.lower():
                print("Rilevata distribuzione Debian/Ubuntu")
                
                # Aggiungi il repository di Chrome
                subprocess.run(["wget", "-q", "-O", "-", "https://dl.google.com/linux/linux_signing_key.pub", "|", "sudo", "apt-key", "add", "-"], shell=True)
                subprocess.run(["sudo", "sh", "-c", 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'])
                
                # Aggiorna e installa Chrome
                subprocess.run(["sudo", "apt-get", "update"])
                subprocess.run(["sudo", "apt-get", "install", "-y", "google-chrome-stable"])
            
            # CentOS/RHEL/Fedora
            elif "centos" in os_release.lower() or "rhel" in os_release.lower() or "fedora" in os_release.lower():
                print("Rilevata distribuzione CentOS/RHEL/Fedora")
                
                # Crea il file repo per Chrome
                repo_file = "/etc/yum.repos.d/google-chrome.repo"
                repo_content = """[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
"""
                with open("/tmp/google-chrome.repo", "w") as f:
                    f.write(repo_content)
                
                subprocess.run(["sudo", "mv", "/tmp/google-chrome.repo", repo_file])
                
                # Installa Chrome
                subprocess.run(["sudo", "yum", "install", "-y", "google-chrome-stable"])
            
            else:
                print("Distribuzione Linux non supportata per l'installazione automatica.")
                print("Per favore, installa Google Chrome manualmente.")
                return False
        
        except Exception as e:
            print(f"Errore durante l'installazione di Chrome su Linux: {e}")
            return False
    
    else:
        print(f"Sistema operativo {system} non supportato per l'installazione automatica di Chrome.")
        return False
    
    print("Google Chrome è stato installato con successo!")
    return True

def main():
    """Funzione principale."""
    if is_chrome_installed():
        print("Google Chrome è già installato nel sistema.")
    else:
        print("Google Chrome non è installato. Avvio dell'installazione...")
        if install_chrome():
            print("Installazione completata con successo.")
        else:
            print("Impossibile installare Google Chrome automaticamente.")
            sys.exit(1)

if __name__ == "__main__":
    main()