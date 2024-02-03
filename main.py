import streamlit as st
import backend_api as api

APP_MESSAGES_KEY = "app_messages"

def streamlit_init():
    if st.session_state.get(APP_MESSAGES_KEY, None) is None:
        st.session_state[APP_MESSAGES_KEY] = []

def main():
    streamlit_init()
    st.title("TokGen")
    st.write("Welcome to TokGen! This is a tool for tiktok trend analysis.")
    st.write("To get started, input the topic that you are interested in.")
    for message in st.session_state[APP_MESSAGES_KEY]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # React to user input
    if query := st.chat_input("Enter a question?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(query)
        # Add user message to chat history
        st.session_state[APP_MESSAGES_KEY].append({"role": "user", "content": query})
        with st.spinner("Analyzing..."):
            # generate response
            response = api.query(query).response
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state[APP_MESSAGES_KEY].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()