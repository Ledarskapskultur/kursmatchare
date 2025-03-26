import streamlit as st
import pandas as pd
import requests

# Funktioner för att hämta och bearbeta data
@st.cache_data
def hamta_kurser_uglkurser():
    url = "https://www.uglkurser.se/datumochpriser.php"
    tables = pd.read_html(url)
    df = tables[0].copy()
    df.columns = ["Datum", "Ort", "Handledare", "Arrangör", "Pris"]
    df["Källa"] = "uglkurser.se"
    return df

@st.cache_data
def hamta_kurser_rezon():
    url = "https://rezon.se/kurskategorier/ugl/"
    tables = pd.read_html(url)
    df = tables[0].copy()
    df.columns = ["Datum", "Ort", "Pris", "Handledare"]
    df["Arrangör"] = "Rezon"
    df["Källa"] = "rezon.se"
    return df

@st.cache_data
def hamta_kurser_corecode():
    url = "https://www.corecode.se/oppna-utbildningar/ugl-utbildning?showall=true&filterBookables=-1"
    tables = pd.read_html(url)
    df = tables[0].copy()
    df.columns = ["Datum", "Ort", "Handledare", "Pris"]
    df["Arrangör"] = "CoreCode"
    df["Källa"] = "corecode.se"
    return df

# Sidhuvud
st.title("Kursmatchare: UGL-utbildningar")

st.sidebar.header("Filtrera på dina önskemål")
val_ort = st.sidebar.text_input("Ort/plats")
val_vecka = st.sidebar.text_input("Vecka (valfri, skriv t.ex. 12)")
val_maxpris = st.sidebar.number_input("Maxpris (SEK)", min_value=0, value=20000, step=500)

# Hämta all data
st.info("Hämtar kurser från 3 webbplatser...")
df1 = hamta_kurser_uglkurser()
df2 = hamta_kurser_rezon()
df3 = hamta_kurser_corecode()

# Kombinera data
kurser = pd.concat([df1, df2, df3], ignore_index=True)

# Rensa och konvertera
kurser["Pris"] = kurser["Pris"].replace("[ SEK]*", "", regex=True).str.replace(" ", "").astype(float)
kurser["Datum"] = pd.to_datetime(kurser["Datum"], errors="coerce")
kurser["Vecka"] = kurser["Datum"].dt.isocalendar().week

# Filtrering
if val_ort:
    kurser = kurser[kurser["Ort"].str.contains(val_ort, case=False, na=False)]

if val_vecka:
    try:
        vecka = int(val_vecka)
        kurser = kurser[kurser["Vecka"] == vecka]
    except ValueError:
        st.warning("Vänligen ange en giltig veckonummer.")

kurser = kurser[kurser["Pris"] <= val_maxpris]

# Visa resultat
st.subheader("Matchade kurser")
st.write(f"Antal träffar: {len(kurser)}")
st.dataframe(kurser.reset_index(drop=True))

# Exportfunktion
csv = kurser.to_csv(index=False).encode('utf-8')
st.download_button(
    "Ladda ner som CSV",
    data=csv,
    file_name="matchade_kurser.csv",
    mime="text/csv"
)

st.caption("Byggd med Streamlit. Källor: uglkurser.se, rezon.se, corecode.se")
