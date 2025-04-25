# Subito.it Scraper

Uno strumento di web scraping per Subito.it con comportamento umano simulato, basato su Streamlit e Selenium Wire.

## Installazione Automatizzata

Per installare automaticamente tutte le dipendenze, incluso Google Chrome:

```bash
python setup.py
```

Questo script:
1. Installa tutte le dipendenze Python dal file `requirements.txt`
2. Verifica se Chrome è già installato e, in caso contrario, lo installa automaticamente

## Installazione Manuale

Se preferisci installare manualmente:

1. Installa le dipendenze Python:
```bash
pip install -r requirements.txt
```

2. Assicurati che Google Chrome sia installato sul tuo sistema

## Esecuzione dell'Applicazione

Per avviare l'applicazione:

```bash
streamlit run app.py
```

## Funzionalità

- Web scraping di Subito.it con simulazione di comportamento umano
- Supporto per proxy tramite Selenium Wire
- Interfaccia utente intuitiva con Streamlit
- Esportazione dei dati in formato CSV

## Requisiti

- Python 3.7+
- Google Chrome
- Connessione Internet

## Note per Ambienti Automatizzati

In ambienti automatizzati come server CI/CD o container Docker:

1. Esegui `python install_chrome.py` per installare Chrome
2. Usa l'opzione `--no-sandbox` (già configurata nel codice)
3. Assicurati di avere i permessi necessari per l'installazione

## Utilizzo di Selenium Wire

Questo progetto utilizza Selenium Wire, che estende Selenium con funzionalità aggiuntive come:

- Intercettazione e modifica delle richieste HTTP
- Supporto avanzato per proxy
- Monitoraggio del traffico di rete

Per utilizzare un proxy:

```python
driver = get_selenium_driver(proxy="http://user:pass@host:port")
```