import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

st.cache_data.clear()

st.set_page_config(page_title="Sleep Dashboard", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Apply Inter font globally */
    html, body, div, span, appview-container, [class*="css"], .stText, .stMarkdown, .stDataFrame, .stButton, .stHeader, h1, h2, h3, h4, h5, h6, table, th, td {
        font-family: 'Inter', sans-serif !important;
    }

    /* Apply Inter font to Streamlit tables */
    .dataframe table {
        font-family: 'Inter', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)


# st.markdown(
#     "<h1 style='text-align: center; color: #17065b;'>Dashboard:<br>The Big Taping Truth Trial</h1>",
#     unsafe_allow_html=True
# )

# Today’s date format
today = datetime.today().strftime("%Y-%m-%d")

# File IDs (from Google Drive)
FILE_IDS = {
    "image": "1-D4sGmzF1syGUTUO_5UfloMLpLRqPnh8",
    "funnel": "1-Apq66H0DOEEfuCp5ghL4nRIOMb1WRiL",
    "taping": "1-9-FZjceasHwrFQ5y6H9I7Bs7myPjixW"
}

# Build direct links
def drive_url(file_id):
    return f"https://drive.google.com/uc?id={file_id}"

# Show funnel data
st.subheader("Current Number of Participants")
try:
    funnel_df = pd.read_csv(drive_url(FILE_IDS["funnel"]))
    num_participants = funnel_df["Participants"].iloc[4]  # adjust column name if needed
    st.markdown(f"<h1 style='text-align: center; color: #17065b;'>{int(num_participants):,}</h1>", unsafe_allow_html=True)

except Exception as e:
    st.error("Couldn't load funnel data.")
    st.exception(e)

# Show image
image_url = drive_url(FILE_IDS["image"])

st.subheader("Current Results")
try:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    st.image(image, use_container_width=True)
except Exception as e:
    st.error("Failed to load image.")
    st.exception(e)
st.markdown("""
    <p style="font-size:12px; color:gray;">
        Note: Do not publish. This dashboard displays combined averages, but final results must be based on a within-subjects analysis.
    </p>
    """, unsafe_allow_html=True)


# Show taping data
st.subheader("Current Amount of Data Collected")
try:
    taping_df = pd.read_csv(drive_url(FILE_IDS["taping"]))
    taping_df.columns = ["Data Type", "Amount"]
    taping_df = taping_df.reset_index(drop=True)
    st.dataframe(taping_df.style.hide(axis="index"))
except Exception as e:
    st.error("Couldn't load taping data.")
    st.exception(e)
