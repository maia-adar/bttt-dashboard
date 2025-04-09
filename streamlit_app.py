import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Sleep Dashboard", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #17065b;'>Dashboard:<br>The Big Taping Truth Trial</h1>",
    unsafe_allow_html=True
)

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

# Show image
image_url = drive_url(FILE_IDS["image"])

try:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    st.image(image, use_container_width=True)
except Exception as e:
    st.error("Failed to load image.")
    st.exception(e)

# Show funnel data
st.subheader("Current Number of Participants")
try:
    funnel_df = pd.read_csv(drive_url(FILE_IDS["funnel"]))
    num_participants = funnel_df["Participants"].iloc[2]  # adjust column name if needed
    st.markdown(f"<h1 style='text-align: center; color: #17065b;'>{int(num_participants):,}</h1>", unsafe_allow_html=True)

except Exception as e:
    st.error("Couldn't load funnel data.")
    st.exception(e)

# Show taping data
st.subheader("Current Amount of Data Collected")
try:
    taping_df = pd.read_csv(drive_url(FILE_IDS["taping"]))
    taping_df.columns = ["Data Type", "Amount"]
    st.dataframe(taping_df.style.hide(axis="index"))
except Exception as e:
    st.error("Couldn't load taping data.")
    st.exception(e)
