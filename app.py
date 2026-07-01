from pathlib import Path
from datetime import datetime

import streamlit as st

from agent import chat


st.set_page_config(
    page_title="Tommy • NovaPay AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css = Path("assets/style.css").read_text()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompt" not in st.session_state:
    st.session_state.prompt = None

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


toggle_row = st.columns([0.6, 11.4])

with toggle_row[0]:
    if st.button("☰", key="sidebar_toggle"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()


if st.session_state.sidebar_open:
    left, main = st.columns(
        [1.15, 4],
        gap="large",
    )
else:
    left = None
    main = st.columns([1])[0]


if left is not None:
    with left:

        st.image("assets/tommy.png", width=90)

        st.markdown("## Tommy")
        st.caption("NovaPay AI Assistant")

        st.success(" Online")

        st.divider()

        if st.button(
            " New Chat",
            key="new_chat",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.session_state.prompt = None
            st.session_state.chat_started = False
            st.rerun()

        if st.button(
            " Knowledge Base",
            key="sidebar_docs",
            use_container_width=True,
        ):
            st.session_state.prompt = "What documentation does NovaPay provide?"
            st.rerun()

        if st.button(
            " Merchant Services",
            key="sidebar_merchant",
            use_container_width=True,
        ):
            st.session_state.prompt = "Tell me about NovaPay merchant services."
            st.rerun()

        if st.button(
            " Security",
            key="sidebar_security",
            use_container_width=True,
        ):
            st.session_state.prompt = "How does NovaPay protect customer funds and accounts?"
            st.rerun()

        if st.button(
            " Settings",
            key="sidebar_settings",
            use_container_width=True,
        ):
            st.session_state.prompt = "What account settings are available in NovaPay?"
            st.rerun()

        st.divider()

        st.markdown("##### Powered by")
        st.caption("NovaPay Technologies")


with main:

    if not st.session_state.chat_started:

        hero_left, hero_right = st.columns([1, 4])

        with hero_left:

            st.image(
                "assets/tommy.png",
                width=130,
            )

        with hero_right:

            st.title("Hi, I'm Tommy 👋")

            st.caption("NovaPay AI Payment Specialist")

            st.write(
                """
I'm here to help you with anything related to NovaPay.

I can answer questions about:

- Wallets
- Transfers
- Pricing
- Merchant Services
- APIs
- Documentation
- Security
- General Support
"""
            )

        st.write("### Quick Actions")

        row1 = st.columns(3)

        if row1[0].button(
            " Transaction Fees",
            key="quick_fees",
            use_container_width=True,
        ):
            st.session_state.prompt = (
                "What are NovaPay's transaction fees?"
            )
            st.rerun()

        if row1[1].button(
            " Wallet Services",
            key="quick_wallet",
            use_container_width=True,
        ):
            st.session_state.prompt = (
                "Tell me about NovaPay wallet services."
            )
            st.rerun()

        if row1[2].button(
            " Security",
            key="quick_security",
            use_container_width=True,
        ):
            st.session_state.prompt = (
                "How does NovaPay keep users secure?"
            )
            st.rerun()

        row2 = st.columns(3)

        if row2[0].button(
            " Merchant Services",
            key="quick_merchant",
            use_container_width=True,
        ):
            st.session_state.prompt = (
                "Tell me about NovaPay merchant services."
            )
            st.rerun()

        if row2[1].button(
            " Documentation",
            key="quick_docs",
            use_container_width=True,
        ):
            st.session_state.prompt = (
                "Show me NovaPay documentation."
            )
            st.rerun()

        if row2[2].button(
            "NovaPay API",
            key="quick_api",
            use_container_width=True,
        ):
            st.session_state.prompt = (
                "Tell me about the NovaPay API."
            )
            st.rerun()

        st.divider()


    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message("user", avatar="🧑"):

                st.markdown(message["content"])

        else:

            with st.chat_message("assistant"):

                header1, header2 = st.columns([8, 2])

                with header1:

                    st.image("assets/tommy.png", width=40)

                with header2:

                    st.caption(
                        message.get(
                            "time",
                            "",
                        )
                    )

                st.markdown("**Tommy**")

                st.caption(" Verified from NovaPay")

                st.markdown(message["content"])

                st.divider()

                st.caption(" Source")

                st.caption("NovaPay")


    user_prompt = st.chat_input(
        "Ask Tommy anything about NovaPay..."
    )


    if st.session_state.prompt:

        user_prompt = st.session_state.prompt

        st.session_state.prompt = None


    if user_prompt:

        st.session_state.chat_started = True

        user_message = {

            "role": "user",

            "content": user_prompt,

            "time": datetime.now().strftime("%I:%M %p"),

        }

        st.session_state.messages.append(
            user_message
        )

        with st.chat_message(
            "user",
            avatar="🧑",
        ):

            st.markdown(user_prompt)

        with st.chat_message("assistant"):

            top1, top2 = st.columns([8, 2])

            with top1:

                st.image(
                    "assets/tommy.png",
                    width=40,
                )

            with top2:

                st.caption(
                    datetime.now().strftime(
                        "%I:%M %p"
                    )
                )

            st.markdown("**Tommy**")

            st.caption(
                "Tommmy is thinking"
            )

            response = chat(user_prompt)

            st.caption(
                " Verified from NovaPay Documentation"
            )

            st.markdown(response)

            st.divider()

            st.caption(" Source")

            st.caption("NovaPay Profile.pdf")

        st.session_state.messages.append(

            {

                "role": "assistant",

                "content": response,

                "time": datetime.now().strftime(
                    "%I:%M %p"
                ),

            }

        )

        st.rerun()