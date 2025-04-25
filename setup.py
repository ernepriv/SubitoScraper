#!/usr/bin/env python3
"""
Script di setup per installare tutte le dipendenze necessarie, incluso Google Chrome.
"""

import os
import subprocess
import sys
import platform

def install_requirements():
    """Installa le dipendenze Python dal file requirements.txt."""
    print("Installazione delle dipendenze Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dipendenze Python installate con successo.")

def install_chrome():
    """Installa Google Chrome utilizzando lo script dedicato."""
    print("Verifica e installazione di Google Chrome...")
    subprocess.check_call([sys.executable, "install_chrome.py"])

def main():
    """Funzione principale di setup."""
    print(f"Avvio del setup per l'ambiente di scraping su {platform.system()}...")
    
    # Installa le dipendenze Python
    install_requirements()
    
    # Installa Chrome
    install_chrome()
    
    print("\nSetup completato con successo!")
    print("Ora puoi eseguire l'applicazione con: streamlit run app.py")

if __name__ == "__main__":
    main()