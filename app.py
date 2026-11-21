import tkinter as tk
from tkinter import scrolledtext
import requests
import time
import threading
import subprocess
import re

def ispisi(tekst):
    rezultati_box.insert(tk.END, tekst + "\n")
    rezultati_box.see(tk.END)

def ocisti_ekran():
    rezultati_box.delete(1.0, tk.END)

def pokreni_ip():
    ip_adresa = unos_polje.get().strip()
    if not ip_adresa:
        ispisi("[!] Upiši IP adresu ili domenu u polje iznad!")
        return
    
    ocisti_ekran()
    ispisi(f"Pretražujem IP / domenu: {ip_adresa}...\n")
    
    def zadatak():
        try:
            odgovor = requests.get("http://ip-api.com" + ip_adresa, timeout=5).json()
            if odgovor.get("status") == "success":
                ispisi("--- REZULTATI ZA IP ---")
                ispisi(f"Država: {odgovor.get('country')}")
                ispisi(f"Grad: {odgovor.get('city')}")
                ispisi(f"Operater: {odgovor.get('isp')}")
                ispisi(f"Vremenska zona: {odgovor.get('timezone')}")
            else:
                ispisi("[!] Neispravna ili privatna IP adresa.")
        except:
            ispisi("[!] Greška pri spajanju na IP servis.")

    threading.Thread(target=zadatak, daemon=True).start()

def pokreni_korisnika():
    korisnik = unos_polje.get().strip()
    if not korisnik:
        ispisi("[!] Upiši korisničko ime u polje iznad!")
        return

    ocisti_ekran()
    ispisi(f"Pretražujem javne profile za: {korisnik}...\n")

    def zadatak():
        stranice = {
            "GitHub": "https://github.com",
            "GitLab": "https://gitlab.com",
            "Chess.com": "https://chess.com",
            "Lichess": "https://lichess.org",
            "Reddit": "https://reddit.com",
            "Roblox": "https://roblox.com",
            "Steam": "https://steamcommunity.com",
            "Pastebin": "https://pastebin.com",
            "Dev.to": "https://dev.to",
            "About.me": "https://about.me",
            "Pinterest": "https://pinterest.com",
            "SoundCloud": "https://soundcloud.com",
            "Vimeo": "https://vimeo.com",
            "Behance": "https://behance.net",
            "Dribbble": "https://dribbble.com",
            "Medium": "https://medium.com@",
            "Replit": "https://replit.com@",
            "HackerRank": "https://hackerrank.com",
            "CodePen": "https://codepen.io",
            "Gravatar": "https://gravatar.com",
            "Linktree": "https://linktr.ee",
            "Patreon": "https://patreon.com"
        }

        zaglavlje = {"User-Agent": "Mozilla/5.0"}

        for naziv, bazni_url in stranice.items():
            puni_url = bazni_url + korisnik
            try:
                odgovor = requests.get(puni_url, headers=zaglavlje, timeout=5)
                if odgovor.status_code == 200:
                    ispisi(f"[+] PRONAĐENO ({naziv}): {puni_url}")
                else:
                    ispisi(f"[-] Nema na {naziv}")
            except:
                ispisi(f"[!] Greška ({naziv})")
            
            time.sleep(0.4)
        
        ispisi("\n--- Pretraga završena ---")

    threading.Thread(target=zadatak, daemon=True).start()

def pokreni_mail():
    email = unos_polje.get().strip()
    if not email or "@" not in email:
        ispisi("[!] Upiši ispravnu e-mail adresu u polje iznad!")
        return

    ocisti_ekran()
    ispisi(f"Pretražujem servise za e-mail: {email} (pričekaj 10-ak sekundi)...\n")

    def zadatak():
        try:
            # Pokreće holehe u pozadini bez otvaranja crnog CMD prozora
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            proces = subprocess.run(
                ["holehe", email, "--only-used"],
                capture_output=True,
                text=True,
                startupinfo=startupinfo
            )

            # Uklanja ANSI kodove za boje iz terminala
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            cisti_izlaz = ansi_escape.sub('', proces.stdout)

            pronadeno = False
            for linija in cisti_izlaz.splitlines():
                linija_trim = linija.strip()
                # Prikazuje isključivo redove koji počinju s [+]
                if linija_trim.startswith("[+]"):
                    ispisi(linija_trim)
                    pronadeno = True

            if not pronadeno:
                ispisi("[-] Nije pronađen nijedan javno povezan račun.")

            ispisi("\n--- Provjera e-maila završena ---")

        except FileNotFoundError:
            ispisi("[!] Greška: Alat 'holehe' nije pronađen. Provjeri je li instaliran (pip install holehe).")
        except Exception as e:
            ispisi(f"[!] Došlo je do greške: {e}")

    threading.Thread(target=zadatak, daemon=True).start()

prozor = tk.Tk()
prozor.title("OSINT Alat v2.0")
prozor.geometry("680x520")
prozor.configure(bg="#121212")

naslov = tk.Label(prozor, text="OSINT", font=("Consolas", 32, "bold"), fg="#00ff41", bg="#121212")
naslov.pack(pady=(15, 0))

podnaslov = tk.Label(prozor, text="Alat za provjeru javnih IP adresa, korisničkih profila i e-maila", font=("Arial", 10), fg="#aaaaaa", bg="#121212")
podnaslov.pack(pady=(0, 15))

unos_polje = tk.Entry(prozor, font=("Consolas", 13), width=38, bg="#1e1e1e", fg="#ffffff", insertbackground="white", justify="center")
unos_polje.pack(pady=5, ipady=5)

okvir_gumbi = tk.Frame(prozor, bg="#121212")
okvir_gumbi.pack(pady=15)

gumb_ip = tk.Button(okvir_gumbi, text="Provjeri IP / Domenu", font=("Arial", 10, "bold"), bg="#007acc", fg="white", width=17, height=2, cursor="hand2", command=pokreni_ip)
gumb_ip.grid(row=0, column=0, padx=6)

gumb_user = tk.Button(okvir_gumbi, text="Provjeri Korisnika", font=("Arial", 10, "bold"), bg="#28a745", fg="white", width=17, height=2, cursor="hand2", command=pokreni_korisnika)
gumb_user.grid(row=0, column=1, padx=6)

gumb_mail = tk.Button(okvir_gumbi, text="Provjeri Mail", font=("Arial", 10, "bold"), bg="#d97706", fg="white", width=15, height=2, cursor="hand2", command=pokreni_mail)
gumb_mail.grid(row=0, column=2, padx=6)

gumb_ocisti = tk.Button(okvir_gumbi, text="Očisti", font=("Arial", 10, "bold"), bg="#444444", fg="white", width=10, height=2, cursor="hand2", command=ocisti_ekran)
gumb_ocisti.grid(row=0, column=3, padx=6)

rezultati_box = scrolledtext.ScrolledText(prozor, font=("Consolas", 10), width=78, height=18, bg="#0d0d0d", fg="#00ff41")
rezultati_box.pack(pady=10, padx=15)

prozor.mainloop()
