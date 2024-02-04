import streamlit as st
import backend_api as api

APP_MESSAGES_KEY = "app_messages"

def streamlit_init():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if APP_MESSAGES_KEY not in st.session_state:
        st.session_state[APP_MESSAGES_KEY] = []
import streamlit as st

def homepage():
    # st.container().image("logo.png", width=100)  # Assuming you have a logo image
    st.title("Welcome to TokGen!")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("logo.png", width=200)  # An image that represents a content genie

    with col2:
        st.markdown("""
            ## 🌟 Your AI Content Genie 🌟
            **TokGen** is here to revolutionize your TikTok presence! Dive into
            the world of endless creativity with our AI-powered assistant designed
            to elevate your content game to the next level.""" , unsafe_allow_html=True)
    st.markdown("""
        ### Why TokGen?
        - **Trend Tracker**: Stay ahead of the curve by discovering the latest trends tailored to your niche.
        - **Content Crafter**: Generate personalized content ideas that resonate with your audience.
        
        Ready to unleash your full potential? Let's get started and transform your content into something magical! 🚀
    """, unsafe_allow_html=True)
    
    # Enhance the "Get Started" button with some styling
    if st.button("✨ Get Started ✨", key="get_started"):
        st.session_state.page = "ask_question"
        st.experimental_rerun()

    st.markdown("---")
    
    # Optionally, add a section for testimonials or success stories
    st.subheader("Hear from Our Successful TikTokers")
    st.write("Discover how TokGen has transformed their content creation journey and led them to viral success!")

    # Placeholder for testimonials; replace with actual data or remove if not applicable
    testimonials = ["TokGen helped me triple my followers in just a month!", 
                    "Thanks to TokGen, I'm now trending in my niche.",
                    "Creating content has never been easier. I love TokGen!"]

    for testimonial in testimonials:
        st.info(testimonial)

    st.subheader("Github Repo")
    st.markdown("[Github Code](https://github.com/Alfr3doK1ng/TokGen)")

def ask_question_page():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("logo.png", width=100)  # Adjust the width as needed
    with col2:
        st.title("TokGen")
    st.header("Ask a Question")
    st.write("Hey there, TikTok star! Let's get your content to the next level.")

    # Display chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        st.container().markdown(f"**{message['role']}**: {message['content']}")

    query = st.text_input("Enter your question here:", key="query_input")
    
    if st.button("Submit", key="submit_query"):
        if query:  # Check if the query is not empty
            st.session_state.chat_history.append({"role": "You", "content": query})

            response = "This is a simulated response."  # Here you would call your actual API
            st.session_state.chat_history.append({"role": "TokGen", "content": response})
            st.experimental_rerun()

    # Button to navigate back to the main page
    if st.button("Back to Home", key="back_to_home"):
        st.session_state.page = "home"
        st.experimental_rerun()

def main():
    streamlit_init()
    if st.session_state.page == "home":
        homepage()
    elif st.session_state.page == "ask_question":
        ask_question_page()

if __name__ == "__main__":
    main()