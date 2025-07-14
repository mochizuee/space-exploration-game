import sys
import subprocess


print("welcome to the game")
print('for Eglish type "ENG"')

print("oyuna hoş geldiniz")
print('Türkçe için "TR" yazın')

def run_language_version(language):
    if language == "tr":
        subprocess.run([sys.executable, "projeTR.py"])
    elif language == "en":
        subprocess.run([sys.executable, "projeENG.py"])
    else:
        print("Invalid choice. Please type 'tr' or 'en'.")

if __name__ == "__main__":
    lang = input("Choose language / Dil seçin (en/tr): ").strip().lower()
    run_language_version(lang)
