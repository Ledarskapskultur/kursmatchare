# Kursmatchare: UGL-utbildningar

Denna Streamlit-app hämtar automatiskt kursinformation från tre olika webbsidor med UGL-utbildningar och matchar mot användarens önskemål (vecka, ort och maxpris).

## Funktioner

- Automatisk hämtning från:
  - https://www.uglkurser.se
  - https://rezon.se
  - https://corecode.se
- Filtrering på:
  - Ort/plats
  - Vecka
  - Maxpris
- Export av matchade kurser till CSV

## Kom igång

1. Klona detta repo:
```
git clone https://github.com/dittnamn/kursmatchare.git
cd kursmatchare
```

2. Installera beroenden:
```
pip install -r requirements.txt
```

3. Kör appen:
```
streamlit run app.py
```

## Byggd med

- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
