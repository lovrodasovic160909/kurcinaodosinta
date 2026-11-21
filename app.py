import streamlit as st
import requests
import time
import subprocess
import re

st.set_page_config(page_title="OSINT Alat v2.0", page_icon="🕵️", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #00ff41;
    }
    h1 {
        color: #00ff41 !important;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    .subtitle {
        text-align: center;
        color: #aaaaaa;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>OSINT</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Alat za provjeru javnih IP adresa, korisničkih profila i e-maila</p>", unsafe_allow_html=True)

unos = st.text_input("Upiši IP adresu, korisničko ime ili e-mail:", placeholder="npr. 8.8.8.8 ili nekimejl@gmail.com")

col1, col2, col3 = st.columns(3)
with col1:
    btn_ip = st.button("🌐 Provjeri IP", use_container_width=True)
with col2:
    btn_user = st.button("👤 Korisnik", use_container_width=True)
with col3:
    btn_mail = st.button("📧 Provjeri Mail", use_container_width=True)

if btn_ip:
    ip_adresa = unos.strip()
    if not ip_adresa:
        st.warning("[!] Upiši IP adresu ili domenu u polje iznad!")
    else:
        with st.spinner(f"Pretražujem IP / domenu: {ip_adresa}..."):
            try:
                odgovor = requests.get(f"http://ip-api.com{ip_adresa}", timeout=5).json()
                if odgovor.get("status") == "success":
                    rezultat = (
                        f"--- REZULTATI ZA IP ---\n"
                        f"Država: {odgovor.get('country')}\n"
                        f"Grad: {odgovor.get('city')}\n"
                        f"Operater: {odgovor.get('isp')}\n"
                        f"Vremenska zona: {odgovor.get('timezone')}"
                    )
                    st.code(rezultat, language="text")
                else:
                    st.error("[!] Neispravna ili privatna IP adresa.")
            except Exception:
                st.error("[!] Greška pri spajanju na IP servis.")

if btn_user:
    korisnik = unos.strip()
    if not korisnik:
        st.warning("[!] Upiši korisničko ime u polje iznad!")
    else:
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
        ispis_linije = [f"Pretražujem javne profile za: {korisnik}...\n"]
        
        okvir_rezultata = st.empty()
        okvir_rezultata.code("\n".join(ispis_linije), language="text")

        for naziv, bazni_url in stranice.items():
            puni_url = bazni_url + korisnik
            try:
                odgovor = requests.get(puni_url, headers=zaglavlje, timeout=5)
                if odgovor.status_code == 200:
                    ispis_linije.append(f"[+] PRONAĐENO ({naziv}): {puni_url}")
                else:
                    ispis_linije.append(f"[-] Nema na {naziv}")
            except Exception:
                ispis_linije.append(f"[!] Greška ({naziv})")
            
            okvir_rezultata.code("\n".join(ispis_linije), language="text")
            time.sleep(0.3)

        ispis_linije.append("\n--- Pretraga završena ---")
        okvir_rezultata.code("\n".join(ispis_linije), language="text")

if btn_mail:
    email = unos.strip()
    if not email or "@" not in email:
        st.warning("[!] Upiši ispravnu e-mail adresu u polje iznad!")
    else:
        with st.spinner(f"Pretražujem servise za e-mail: {email} (pričekaj 10-15 sekundi)..."):
            try:
                proces = subprocess.run(
                    ["holehe", email, "--only-used"],
                    capture_output=True,
                    text=True
                )
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                cisti_izlaz = ansi_escape.sub('', proces.stdout)

                pronadeni = []
                for linija in cisti_izlaz.splitlines():
                    linija_trim = linija.strip()
                    if linija_trim.startswith("[+]"):
                        pronadeni.append(linija_trim)

                if pronadeni:
                    rezultat = "\n".join(pronadeni) + "\n\n--- Provjera e-maila završena ---"
                    st.code(rezultat, language="text")
                else:
                    st.info("[-] Nije pronađen nijedan javno povezan račun.")
            except Exception as e:
                st.error(f"[!] Greška pri pokretanju alata: {e}")
