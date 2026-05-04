<p align="center">
  <img src="assets/FX_logo_top_left.png" alt="Factory-X Logo" width="300">
</p>

# Factory-X Energy Savings v1.0

*Stand: 4. Mai 2026*

Die **Factory-X Energy Savings** App ist eine Streamlit-basierte Demonstrator-Anwendung zur Echtzeit-Ueberwachung und bedarfsgerechten Steuerung von Nebenaggregaten in Werkzeugmaschinen. Sie visualisiert simulierte Live-Sensordaten und zeigt Einsparpotenziale durch intelligente Abschaltstrategien.

## Kernfunktionen

| Tab | Funktion |
|-----|----------|
| **Mist extractor demo** | Ueberwachung des Oelnebelabscheiders mit PM10-Sensorik, Leistungsaufnahme und Ampel-Status. |
| **Mist extractor settings** | Simulationseinstellungen, Live-State, Reset und Sichtbarkeit der optionalen REST-Schnittstelle fuer externe Steuerung. |
| **Mist extractor savings** | Einsparbetrachtung fuer den Oelnebelabscheider. |

## Demo

Die App ist live verfuegbar auf der **Streamlit Community Cloud**:

[Factory-X Energy Savings starten](https://factory-x-energy-savings.streamlit.app/)

## Installation (Lokale Entwicklung)

1. **Repository klonen**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Factory-X_Energy_Savings.git
   cd Factory-X_Energy_Savings
   ```

2. **Abhaengigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Anwendung starten**:
   ```bash
   streamlit run app.py
   ```

Die Streamlit-App startet die lokale Simulation und den optionalen REST-Endpunkt automatisch im selben Prozess. Dadurch koennen externe REST-Kommandos die im UI sichtbare Demo steuern.

## Optionale REST-Schnittstelle

Die REST-API ist kein zwingender Backend-Pfad fuer die Streamlit-App. Ihre Rolle ist eine optionale externe Demonstrator-Schnittstelle, mit der andere lokale Tools den Simulationszustand lesen oder sichere Simulationsparameter setzen koennen.

Lokale Basis-URL:

```text
http://127.0.0.1:8000
```

Wichtige Endpunkte:

| Methode | Endpunkt | Zweck |
|---------|----------|-------|
| `GET` | `/health` | API-Verfuegbarkeit pruefen |
| `GET` | `/state` | Aktuellen Zustand und externe Steuerungsmetadaten lesen |
| `GET` | `/history` | Letzte Simulationssamples lesen |
| `POST` | `/control/pm10-rates` | PM10-Anstiegs- und Abfallrate setzen |
| `POST` | `/control/reset` | Simulation zuruecksetzen |

Beispiele:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/state
curl -X POST http://127.0.0.1:8000/control/pm10-rates \
  -H "Content-Type: application/json" \
  -d '{"rise_rate": 0.12, "fall_rate": 0.35}'
curl -X POST http://127.0.0.1:8000/control/reset \
  -H "Content-Type: application/json" \
  -d '{"source": "REST API"}'
```

Fuer einen API-only Lauf ohne Streamlit kann die FastAPI-App separat gestartet werden:

```bash
uvicorn app.services.data_service:app --reload
```

Hinweis: Die Schnittstelle ist fuer den lokalen Demonstrator gedacht. Sie ist keine produktive Maschinensteuerung und enthaelt bewusst keine Authentifizierung.

## Projektstruktur

```text
Factory-X_Energy_Savings/
├── app.py                 # Einstiegspunkt
├── app/
│   ├── config.py          # Zentrale Konfiguration
│   ├── main.py            # Hauptanwendungslogik und UI
│   ├── components.py      # Wiederverwendbare UI-Komponenten
│   ├── mist_extractor.py  # Oelnebelabscheider-Modul
│   ├── test_env.py        # Settings, Simulation und externe Steuerung
│   └── services/          # FastAPI-Schnittstelle und Datenservice
├── assets/                # Logos und Styling-Assets
└── requirements.txt
```

## Technologie-Stack

| Kategorie | Technologie |
|-----------|-------------|
| Frontend | Streamlit |
| Externe Schnittstelle | FastAPI, Uvicorn |
| Datenanalyse | Pandas, NumPy |
| Visualisierung | Plotly |
| HTTP-Kommunikation | Requests |

---

<p align="center">
  <i>Entwickelt im Rahmen des Factory-X Projekts zur Steigerung der Energieeffizienz in der Produktion.</i>
</p>
