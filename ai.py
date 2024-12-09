
python -m venv venv
.\venv\Scripts\activate
pip install streamlit
streamlit run app.py














import streamlit as st
from streamlit_chat import message
import requests
import json

# Streamlit config
st.set_page_config(
    page_title="Llama 2-7b HF Chat",
    page_icon=":robot:"
)
st.header("Llama 2-7b HF Chat 🦙🤗")

# API Request config
API_URL = "http://34.57.49.2/api/generate"  # Update with the new API URL
headers = {"Content-Type": "application/json", "accept": "application/json"}

# Streamlit session-state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []


# Function to make the API request
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response


# Chat interactive components
input_text = st.text_input("You: ", "Enter your text", key="input")
send_button = st.button("Send")

# Conversation handling
if input_text and send_button:
    # Prepare the payload to match the format in your curl command
    data_payload = {
        "model": "llama3.2",  # Update this model name if needed
        "prompt": input_text,
        "temperature": 0.7,
        "max_tokens": 100
    }
    # Send the request and get the response
    full_response = query(data_payload)

    # Extract the response and append it to session state
    if full_response.status_code == 200:
        output = full_response.json().get("response", "")  # Adjust this key based on API response format
        st.session_state.past.append(input_text)
        st.session_state.generated.append(output)
    else:
        st.session_state.past.append(input_text)
        st.session_state.generated.append("Error: Unable to get a response from the model.")

# Display the conversation
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
