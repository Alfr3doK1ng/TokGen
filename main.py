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
    st.title("Meet TokGen!")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("logo.png", width=200)  # An image that represents a content genie

    with col2:
        st.markdown("""
            ## 🌟 Your AI Content Genie 🌟
            **TokGen** is here to revolutionize your TikTok presence!
            Dive into the world of endless creativity with our AI-powered
            assistant designed to elevate your content game to the next level."
            with "I'm here to revolutionize your TikTok presence! Save time and
            boost user engagement by elevating your content game!.""" , unsafe_allow_html=True)
    st.markdown("""
        ### Why TokGen?
        - **Trend Tracker**: Stay ahead of the curve by discovering the latest trends tailored to your niche.
        - **Content Crafter**: Generate personalized content ideas that resonate with your audience.
        
        Ready to unleash your full potential ? Let's TokGen-erate some magic 🚀
    """, unsafe_allow_html=True)
    
    # Enhance the "Get Started" button with some styling
    if st.button("✨ Get Started ✨", key="get_started"):
        st.session_state.page = "ask_question"
        st.rerun()

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

def display_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        if message["type"] == "text":
            st.write(f"{role}: {content}")
        elif message["type"] == "video":
            st.markdown(f"{role}: {content}", unsafe_allow_html=True)


def ask_question_page():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("logo.png", width=100)  # Adjust the width as needed
    with col2:
        st.title("TokGen")
    st.write("Hey there, TikTok star! Let's get your content to the next level.")
    display_chat_history()
    with st.sidebar:
        st.header("Ask a Question")
        video_list = []
        messages = st.container(height=500)
        if query := st.chat_input("Say something"):
            messages.chat_message("user", avatar = "👤").write(query)
            st.session_state.chat_history.append({"role": "You", "content": query, "type": "text"})
            # Process the query
            vo = api.search_tiktok_trending_videos(query)
            for v in vo:
                video_list.append(v.path)
                video_info = f"- [{v.title}]({v.url})"
                st.session_state.chat_history.append({"role": "TokGen", "content": video_info, "type": "video"})
                messages.chat_message("TokGen", avatar = 'logo.png').write(f"[{v.title}]({v.url})")
    for video in video_list:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.video(video)
    video_list = []

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def main():
    streamlit_init()
    if st.session_state.page == "home":
        homepage()
    elif st.session_state.page == "ask_question":
        ask_question_page()

if __name__ == "__main__":
    main()