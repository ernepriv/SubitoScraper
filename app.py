import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import pandas as pd
import io

# Configurazione della pagina
st.set_page_config(
    page_title="Subito.it Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Stile CSS personalizzato per un'interfaccia più moderna e compatta
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    h1, h2, h3 {
        margin-top: 0;
    }
    .stButton button {
        width: 100%;
        border-radius: 4px;
        height: 2.5rem;
        background-color: #4CAF50;
        color: white;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .css-1544g2n {
        padding: 1rem;
        border-radius: 5px;
    }
    .stExpander {
        border: none;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        border-radius: 4px;
    }
    .stImage {
        border-radius: 4px;
    }
    .css-1v0mbdj {
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Titolo e descrizione in un container compatto
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995470.png", width=80)
    with col2:
        st.title("Subito.it Scraper")
        st.caption("Strumento di web scraping esclusivo per Subito.it con comportamento umano")


# Inizializzazione di Selenium (in background)

# Cache solo l'installazione del ChromeDriverManager
@st.cache_resource
def get_driver_path():
    """Installa e restituisce il percorso del ChromeDriver."""
    return ChromeDriverManager().install()

def get_selenium_driver(user_agent=None, disable_headless=False):
    """
    Inizializza e restituisce un driver Selenium configurato per apparire più umano.
    
    Args:
        user_agent: User agent personalizzato da utilizzare
        disable_headless: Se True, disabilita la modalità headless (mostra il browser)
    """
    try:
        chrome_options = Options()
        
        # Modalità headless solo se richiesto
        if not disable_headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Impostazioni per apparire più umani
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disabilita il flag di automazione
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Rimuove il banner "Chrome is being controlled by automated software"
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Imposta una dimensione della finestra realistica
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Imposta un user agent realistico se non specificato
        if user_agent:
            chrome_options.add_argument(f"--user-agent={user_agent}")
        else:
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Abilita JavaScript
        chrome_options.add_argument("--enable-javascript")
        
        # Accetta i cookie
        chrome_options.add_argument("--enable-cookies")
        
        # Usa il percorso del driver memorizzato nella cache
        driver_path = get_driver_path()
        driver = webdriver.Chrome(
            service=Service(driver_path),
            options=chrome_options
        )
        
        # Modifica il navigator.webdriver per rendere più difficile il rilevamento
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        st.error(f"Errore nell'inizializzazione del driver Selenium: {e}")
        return None



# Funzione per il web scraping di Subito.it
def scrape_subito(url, human_like=True, disable_headless=False, search_term=None):
    """
    Funzione per il web scraping di Subito.it con Selenium.
    
    Args:
        url: URL di Subito.it
        human_like: Se True, simula comportamenti umani durante la navigazione
        disable_headless: Se True, mostra il browser durante lo scraping
        search_term: Termine di ricerca da cercare su Subito.it
    """
    # Scegli casualmente uno user agent da una lista di user agent comuni
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ]
    user_agent = random.choice(user_agents)
    
    driver = get_selenium_driver(user_agent=user_agent, disable_headless=disable_headless)
    if not driver:
        return "Impossibile inizializzare il driver Selenium."
    
    try:
        # Aggiungi un ritardo casuale prima di caricare la pagina (come farebbe un umano)
        if human_like:
            time.sleep(random.uniform(1, 3))
        
        # Carica la pagina
        driver.get(url)
        
        # Utilizzo di WebDriverWait per attendere che la pagina si carichi
        wait = WebDriverWait(driver, 15)  # Timeout aumentato a 15 secondi
        # Attendi che il body sia completamente caricato
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Comportamenti umani simulati
        if human_like:
            # Simula lo scrolling della pagina come farebbe un umano
            body = driver.find_element(By.TAG_NAME, "body")
            
            # Scrolling lento e casuale
            total_height = driver.execute_script("return document.body.scrollHeight")
            viewport_height = driver.execute_script("return window.innerHeight")
            
            # Calcola quanti "schermi" ci sono da scorrere
            num_screens = max(1, total_height // viewport_height)
            
            # Scorri lentamente la pagina con pause casuali
            for i in range(min(num_screens, 3)):  # Limita a 3 schermate per non impiegare troppo tempo
                # Scrolling con velocità variabile
                driver.execute_script(f"window.scrollTo(0, {(i+1) * viewport_height});")
                time.sleep(random.uniform(0.5, 2))  # Pausa casuale tra gli scrolling
            
            # Torna in cima alla pagina
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Simula movimenti casuali del mouse (solo se non in modalità headless)
            if not disable_headless:
                try:
                    # Trova alcuni elementi casuali su cui muovere il mouse
                    elements = driver.find_elements(By.CSS_SELECTOR, "a, button, input, div")
                    if elements:
                        actions = ActionChains(driver)
                        # Seleziona fino a 3 elementi casuali
                        for _ in range(min(3, len(elements))):
                            elem = random.choice(elements)
                            try:
                                actions.move_to_element(elem).perform()
                                time.sleep(random.uniform(0.3, 1.0))
                            except:
                                pass  # Ignora errori nel movimento del mouse
                except:
                    pass  # Ignora errori nella simulazione del mouse
        
        # Gestione dei cookie (cerca e accetta i banner dei cookie)
        try:
            # Lista di possibili selettori per i pulsanti di accettazione dei cookie
            cookie_button_selectors = [
                "button[id*='cookie' i]", 
                "button[class*='cookie' i]",
                "a[id*='cookie' i]",
                "a[class*='cookie' i]",
                "button[id*='accept' i]",
                "button[class*='accept' i]",
                "button[id*='consent' i]",
                "button[class*='consent' i]",
                "button[id*='privacy' i]",
                "button[class*='privacy' i]",
                "button[id*='didomi-notice-agree-button' i]"
            ]
            
            for selector in cookie_button_selectors:
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed() and any(term in button.text.lower() for term in ['accept', 'accetta', 'ok', 'agree', 'consenti']):
                            button.click()
                            time.sleep(random.uniform(0.5, 1.0))
                            break
                except:
                    continue
        except:
            pass  # Ignora errori nella gestione dei cookie
        
        # Gestione della ricerca su Subito.it
        if search_term and "subito.it" in url.lower():
            try:
                # Attendi che il campo di ricerca sia visibile
                search_box_selectors = [
                    "input[id='main-keyword-field']",

                ]
                
                search_box = None
                for selector in search_box_selectors:
                    try:
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        search_boxes = driver.find_elements(By.CSS_SELECTOR, selector)
                        for box in search_boxes:
                            if box.is_displayed():
                                search_box = box
                                break
                        if search_box:
                            break
                    except:
                        continue
                
                if search_box:
                    # Simula la digitazione umana
                    if human_like:
                        for char in search_term:
                            search_box.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.2))  # Pausa tra i caratteri
                    else:
                        search_box.send_keys(search_term)
                    
                    time.sleep(random.uniform(0.5, 1.5))  # Pausa prima di premere Invio
                    
                    # Premi Invio per avviare la ricerca
                    search_box.send_keys(Keys.RETURN)
                    
                    # Attendi che i risultati di ricerca si carichino
                    time.sleep(random.uniform(2, 4))
                    
                    # Scorri un po' per vedere i risultati
                    if human_like:
                        # Scrolling lento e casuale
                        for _ in range(3):
                            driver.execute_script(f"window.scrollBy(0, {random.randint(300, 700)});")
                            time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"Errore durante la ricerca su Subito.it: {e}")
        
        # Esempio di estrazione del titolo della pagina
        title = driver.title
        
        # Estrazione di elementi HTML
        elements = driver.find_elements(By.TAG_NAME, "h1")
        extracted_texts = [elem.text for elem in elements if elem.text]
        
        # Se siamo su Subito.it, estrai anche i risultati della ricerca
        if "subito.it" in url.lower() and search_term:
            try:
                # Selettori comuni per i risultati di ricerca su Subito.it
                result_selectors = [
                    ".item-card", 
                    ".listing-item", 
                    ".result-item",
                    "[data-testid*='item']",
                    "[data-testid*='listing']",
                    "[data-testid*='result']"
                ]
                
                search_results = []
                for selector in result_selectors:
                    try:
                        items = driver.find_elements(By.CSS_SELECTOR, selector)
                        if items:
                            for item in items[:10]:  # Limita a 10 risultati
                                try:
                                    # Estrai titolo, prezzo e link
                                    title_elem = item.find_element(By.CSS_SELECTOR, "h2, h3, [class*='title']")
                                    title_text = title_elem.text.strip() if title_elem else "Titolo non disponibile"
                                    
                                    price_elem = item.find_element(By.CSS_SELECTOR, "[class*='price'], [data-testid*='price']")
                                    price_text = price_elem.text.strip() if price_elem else "Prezzo non disponibile"
                                    
                                    link = None
                                    try:
                                        link_elem = item.find_element(By.TAG_NAME, "a")
                                        link = link_elem.get_attribute("href")
                                    except:
                                        link = "Link non disponibile"
                                    
                                    search_results.append({
                                        "titolo": title_text,
                                        "prezzo": price_text,
                                        "link": link
                                    })
                                except:
                                    continue
                            break  # Se abbiamo trovato risultati, esci dal ciclo
                    except:
                        continue
                
                if search_results:
                    extracted_texts.append(f"Risultati di ricerca per '{search_term}':")
                    for i, result in enumerate(search_results, 1):
                        extracted_texts.append(f"{i}. {result['titolo']} - {result['prezzo']}")
            except Exception as e:
                print(f"Errore durante l'estrazione dei risultati di ricerca: {e}")
        
        # Risultato da restituire
        result = {
            "title": title,
            "elements": extracted_texts
        }
        
        # Aggiungi i risultati di ricerca di Subito.it se disponibili
        if search_term and 'search_results' in locals() and search_results:
            result["search_results"] = search_results
        
        return result
    except Exception as e:
        return f"Errore durante lo scraping: {e}"
    finally:
        # Chiudi sempre il driver dopo l'uso
        driver.quit()

# Interfaccia principale in un container compatto
with st.container():
    st.markdown("### 🌐 Ricerca su Subito.it")

    # Intestazione per la sezione input
    st.markdown('<div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:10px;"><h4 style="margin:0; color:#262730;">📝 Input</h4></div>', unsafe_allow_html=True)

    # URL fisso di Subito.it (non editabile)
    url_input = "https://www.subito.it"
    st.markdown(f"**URL del sito:** {url_input}")
    
    # Campo di ricerca per Subito.it
    search_term = st.text_input("Cosa vuoi cercare su Subito.it?", 
                              placeholder="es. iPhone, bicicletta, divano...")
    
    # Opzioni in una riga compatta
    col_opt1, col_opt2, col_opt3 = st.columns([2, 2, 1])
    with col_opt1:
        human_like = st.checkbox("Comportamento umano", value=True, 
                               help="Simula comportamenti umani")
    with col_opt2:
        disable_headless = st.checkbox("Mostra browser", value=False, 
                                     help="Utile per debug")
    with col_opt3:
        st.button("Esegui", type="primary")


# Sezione risultati
if st.button("Esegui", type="primary", key="main_button"):
    
    with st.spinner("Esecuzione in corso..."):
        # Verifica che sia stato inserito un termine di ricerca
        if not search_term:
            st.error("Inserisci un termine di ricerca per continuare.")
        else:
            # Esegui lo scraping con le opzioni selezionate
            result = scrape_subito(
                url_input, 
                human_like=human_like, 
                disable_headless=disable_headless,
                search_term=search_term
            )
            
            if isinstance(result, dict):
                # Mostra i risultati in un container compatto
                with st.container():
                    st.markdown("### 📊 Risultati")
                    
                    # Intestazione per la sezione risultati
                    st.markdown('<div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:10px;"><h4 style="margin:0; color:#262730;">📊 Informazioni estratte</h4></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"**Titolo:** {result['title']}")
                    
                    # Mostra i risultati di ricerca di Subito.it se disponibili
                    if "search_results" in result and result["search_results"]:
                        st.markdown("### 🔍 Risultati di ricerca su Subito.it")
                        
                        # Crea una tabella per i risultati
                        data = []
                        for item in result["search_results"]:
                            data.append({
                                "Titolo": item["titolo"],
                                "Prezzo": item["prezzo"],
                                "Link": item['link'] if item['link'] != "Link non disponibile" else "Link non disponibile"
                            })
                        
                        # Mostra la tabella
                        st.table(data)
                        
                        # Aggiungi pulsante per scaricare i risultati in Excel
                        if data:
                            df = pd.DataFrame(data)
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='Risultati')
                            
                            excel_data = excel_buffer.getvalue()
                            st.download_button(
                                label="📥 Scarica risultati in Excel",
                                data=excel_data,
                                file_name=f"risultati_subito_{search_term.replace(' ', '_')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    
                    elif result["elements"]:
                        st.markdown("**Elementi H1:**")
                        for i, text in enumerate(result["elements"], 1):
                            st.markdown(f"- {text}")
                    else:
                        st.info("Nessun risultato trovato. Prova con un altro termine di ricerca.")
            else:
                st.error(result)

# Footer minimalista
st.markdown("---")
st.caption("Subito.it Scraper • Creato con ❤️ da ernepriv")