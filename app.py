import streamlit as st
import base64
from audio_recorder_streamlit import audio_recorder
from utility import setup_openai_client, transcribe_audio, fetch_ai_response,text_to_audio

def auto_play_audio(audio_file):
    with open(audio_file, "rb") as audio_file:
        audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay>'
    st.markdown(audio_html, unsafe_allow_html=True)

def main():
    with st.sidebar:
        st.subheader("APi Configuration Key")

        api_key = st.text_input("Enter you OpenAI API key", type="password")
        if st.button("Connect"):
            if api_key is not None:
                st.session_state.apikey = api_key                

    st.title("🎙️ AtanuGpt Audio")
    st.write("Hi! Click on the recorder and start chatting with me. Speak slowly 🙂")    

    if "apikey" in st.session_state:  
        client = setup_openai_client(st.session_state.apikey)      
        recorded_audio = audio_recorder()
        
        if recorded_audio is None:
            st.rerun()

        if recorded_audio:
            audio_file = "audio.wav"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)
            
            transcribed_text = transcribe_audio(client, audio_file)
            st.write("You have asked: ", transcribed_text)

            with st.spinner("Generating response ..."):
                ai_response = fetch_ai_response(client, transcribed_text)
                response_audio_file = "audio_response.wav"
                text_to_audio(client, ai_response, response_audio_file)
                #st.audio(response_audio_file)
                #st.write("AI Response: ", ai_response)
                auto_play_audio(response_audio_file)
    

if __name__ == "__main__":
    main()