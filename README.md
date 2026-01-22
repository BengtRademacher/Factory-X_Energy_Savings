<p align="center">
  <img src="assets/FX_logo_top_left.png" alt="Factory-X Logo" width="300">
</p>

# Factory-X Energy Savings v0.1

*Stand: 22. Januar 2026*

Die **Factory-X Energy Savings** App ist eine Streamlit-basierte Anwendung zur Echtzeit-Überwachung und bedarfsgerechten Steuerung von Nebenaggregaten in Werkzeugmaschinen. Sie ermöglicht die Visualisierung von Live-Sensordaten und zeigt Einsparpotenziale durch intelligente Abschaltstrategien auf.

## Kernfunktionen

| Tab | Funktion |
|-----|----------|
| **Monitoring** | Zentrale Übersicht aller überwachten Nebenaggregate mit Echtzeit-Statusanzeige und Leistungswerten. |
| **Mist extractor** | Überwachung des Ölnebelabscheiders mit PM₁₀-Sensorik. Visualisierung von Leistungsaufnahme und Partikelkonzentration mit Ampel-Status. |
| **Chip conveyor** | Monitoring des Späneförderers mit Leistungsvisualisierung und Zustandsüberwachung für bedarfsgerechten Betrieb. |
| **Testing** | Testumgebung zur Simulation von Sensordaten und Validierung der Steuerungslogik. |

## Demo

Die App ist live verfügbar auf der **Streamlit Community Cloud**:

👉 [**Factory-X Energy Savings starten**](https://factory-x-energy-savings.streamlit.app/)

## Installation (Lokale Entwicklung)

1. **Repository klonen**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Factory-X_Energy_Savings.git
   cd Factory-X_Energy_Savings
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Anwendung starten**:
   ```bash
   streamlit run app.py
   ```

4. **Optional: REST API starten** (für Live-Daten):
   ```bash
   uvicorn app.services.data_service:app --reload
   ```

## Projektstruktur

```
Factory-X_Energy_Savings/
├── app.py                 # Einstiegspunkt
├── app/
│   ├── config.py          # Zentrale Konfiguration
│   ├── main.py            # Hauptanwendungslogik und UI
│   ├── components.py      # Wiederverwendbare UI-Komponenten
│   ├── mist_extractor.py  # Ölnebelabscheider-Modul
│   ├── chip_conveyor.py   # Späneförderer-Modul
│   ├── test_env.py        # Testumgebung und Datensimulation
│   └── services/          # Backend-Services (REST API)
├── assets/                # Logos und Styling-Assets
└── requirements.txt
```

## Design und Styling

Die Anwendung folgt dem **Factory-X Design-Guide**:
- **Material Design**: Material Symbols Rounded für intuitive Navigation
- **Responsive Layout**: Optimiert für Wide-Mode mit Live-Updates
- **Branding**: Factory-X Logos und Farbschema mit grünem Akzent (Energiethema)
- **Ampel-Feedback**: Visueller Status über Farbcodierung (grün/gelb/rot)

## Technologie-Stack

| Kategorie | Technologie |
|-----------|-------------|
| Frontend | Streamlit |
| Backend/API | FastAPI, Uvicorn |
| Datenanalyse | Pandas, NumPy |
| Visualisierung | Plotly |
| HTTP-Kommunikation | Requests |

---

<p align="center">
  <i>Entwickelt im Rahmen des Factory-X Projekts zur Steigerung der Energieeffizienz in der Produktion.</i>
</p>
