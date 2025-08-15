import random
import datetime
import csv
import streamlit as st
from st_copy import copy_button


#Create Random and unique Asset Tag
def qr_code():
    seed_date = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S")
    seed_date_int = int(seed_date)

    random.seed(seed_date_int)
    num = random.randrange(0o00000001, 999999999, 1)

    gen_text = f"NeedsQRCode{num}"

    return gen_text


def main(text):
    st.title("Nlyte QR Code :blue[Generator] :sunglasses:")

    st.code(text, language="python")

    # To bring columns together
    st.markdown("""
                <style>
                    div[data-testid="stColumn"] {
                        width: fit-content !important;
                        flex: unset;
                    }
                    div[data-testid="stColumn"] * {
                        width: fit-content !important;
                    }
                </style>
                """, unsafe_allow_html=True)

    col2, col3 = st.columns([1,1], vertical_alignment="bottom")

    with col2:
        st.button("Generate QR Code")
    with col3:
        copy_button(text)

    # Add Empty Space
    for i in range(10):
        st.text("")



if __name__ == '__main__':
    text_code = qr_code()

    main(text_code)
