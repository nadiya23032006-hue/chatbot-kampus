import streamlit as st
import json
import requests
import os

st.set_page_config(page_title="Chatbot Kampus Vokasi", layout="wide")
st.title("Chatbot Kampus Vokasi 💬")

# Load data TXT
txt_path = "data.txt"
txt_content = open(txt_path, "r", encoding="utf-8").read() if os.path.exists(txt_path) else ""

# Load data JSON
json_path = "data.json"
json_content = ""
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        if isinstance(json_data, dict):
            json_content = " ".join([str(v) for v in json_data.values()])
        elif isinstance(json_data, list):
            json_content = " ".join([str(v) for item in json_data for v in (item.values() if isinstance(item, dict) else [item])])
        else:
            json_content = str(json_data)

# Pilih sumber data
option = st.selectbox("Pilih sumber data:", ["TXT", "JSON"])
data_text = txt_content if option == "TXT" else json_content
st.write("Data berhasil dimuat!" if data_text else "Tidak ada data.")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input user
user_input = st.text_input("Tanya sesuatu:")

if st.button("Kirim") and user_input.strip():
    if not data_text:
        st.error("Tidak ada data untuk konteks.")
    else:
        # Gabungkan data + user input
        prompt = f"{data_text}\nUser: {user_input}"

        with st.spinner("AI sedang memproses..."):
            try:
                res = requests.post("http://127.0.0.1:8000/chat", json={"message": prompt}, timeout=90)
                if res.status_code == 200:
                    reply = res.json().get("reply", "AI tidak mengembalikan jawaban.")
                else:
                    reply = f"AI Error {res.status_code}: {res.text}"
            except Exception as e:
                reply = f"AI Error: {str(e)}"

        # Simpan ke chat history
        st.session_state.history.append({"user": user_input, "reply": reply})

# Tampilkan chat history ala Laravel
for chat in st.session_state.history:
    st.markdown(f"**Kamu:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['reply']}")
    st.markdown("---")
