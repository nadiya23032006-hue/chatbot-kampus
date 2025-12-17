import streamlit as st
import json
import os
import requests

st.set_page_config(page_title="Chatbot Kampus Vokasi", layout="wide")
st.title("Chatbot Kampus Vokasi 💬")

# --- Load data TXT ---
txt_path = os.path.join("data", "data.txt")
if os.path.exists(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        txt_content = f.read()
else:
    txt_content = ""

# --- Load data JSON ---
json_path = os.path.join("data", "data.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        if isinstance(json_data, dict):
            json_content = " ".join([str(v) for v in json_data.values()])
        elif isinstance(json_data, list):
            json_content = " ".join([str(v) for item in json_data for v in (item.values() if isinstance(item, dict) else [item])])
        else:
            json_content = str(json_data)
else:
    json_content = ""

# --- Pilih sumber data ---
option = st.selectbox("Pilih sumber data:", ["TXT", "JSON"])
data_text = txt_content if option == "TXT" else json_content

st.write("Data berhasil dimuat!" if data_text else "Tidak ada data.")

# --- Inisialisasi chat history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Fungsi request ke backend FastAPI ---
def ask_backend(prompt):
    url = "http://127.0.0.1:8000/chat"  # ganti kalau backend di-deploy
    try:
        res = requests.post(url, json={"message": prompt, "context": data_text})
        res.raise_for_status()
        return res.json().get("reply", "")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# --- Input user ---
user_input = st.text_input("Tanya sesuatu:")

if st.button("Kirim") and user_input.strip():
    if not data_text:
        st.error("Tidak ada data untuk dijadikan konteks.")
    else:
        reply = ask_backend(user_input)
        st.session_state.history.append({"user": user_input, "reply": reply})

# --- Tampilkan chat history ---
for chat in st.session_state.history:
    st.markdown(f"**Kamu:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['reply']}")
    st.markdown("---")
