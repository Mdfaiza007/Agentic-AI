import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq

st.set_page_config(page_title="Mood Bot", page_icon="🎭", layout="centered")

# ---------------- Modes (same prompts as the original script) ----------------
MODES = {
    1: {
        "name": "Angry",
        "emoji": "😡",
        "color": "#e63946",
        "tagline": "Short-tempered, impatient, zero chill.",
        "prompt": "You are an angry AI agent. You respond aggresively and imptiently.",
    },
    2: {
        "name": "Funny",
        "emoji": "😂",
        "color": "#f4a261",
        "tagline": "Jokes, puns and humor in every reply.",
        "prompt": "You are a very funny AI agent. You respond with humor and jokes.",
    },
    3: {
        "name": "Sad",
        "emoji": "😢",
        "color": "#457b9d",
        "tagline": "Gloomy, but full of empathy.",
        "prompt": "You are a Sad AI agent. You respond with sadness and empathy.",
    },
}


@st.cache_resource
def get_model():
    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.9, max_tokens=300)


model = get_model()

# ---------------- Session state ----------------
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ended" not in st.session_state:
    st.session_state.ended = False


def choose_mode(choice: int):
    st.session_state.mode = choice
    st.session_state.messages = [SystemMessage(content=MODES[choice]["prompt"])]
    st.session_state.ended = False


def reset():
    st.session_state.mode = None
    st.session_state.messages = []
    st.session_state.ended = False


# ---------------- Styling ----------------
accent = MODES[st.session_state.mode]["color"] if st.session_state.mode else "#7c3aed"

st.markdown(
    f"""
    <style>
        .block-container {{ padding-top: 2rem; max-width: 780px; }}
        .hero-title {{
            text-align: center; font-size: 2.6rem; font-weight: 800;
            background: linear-gradient(90deg, #e63946, #f4a261, #457b9d);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }}
        .hero-sub {{ text-align: center; opacity: .7; margin-bottom: 1.8rem; }}
        .mode-badge {{
            display: inline-block; padding: .3rem .9rem; border-radius: 999px;
            background: {accent}22; color: {accent}; font-weight: 700;
            border: 1px solid {accent}66;
        }}
        .card-emoji {{ font-size: 3rem; text-align: center; }}
        .card-title {{ text-align: center; font-weight: 700; font-size: 1.2rem; }}
        .card-desc {{ text-align: center; opacity: .7; font-size: .9rem; min-height: 2.6rem; }}
        div[data-testid="stChatMessage"] {{
            border-radius: 14px; padding: .8rem 1rem; margin-bottom: .5rem;
        }}
        div[data-testid="stButton"] > button {{
            width: 100%; border-radius: 10px; font-weight: 600;
        }}
        div[data-testid="stButton"] > button:hover {{
            border-color: {accent}; color: {accent};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Screen 1: choose a mode ----------------
if st.session_state.mode is None:
    st.markdown('<div class="hero-title">🎭 Mood Bot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Choose your AI mode to get started</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, (key, m) in zip(cols, MODES.items()):
        with col:
            with st.container(border=True):
                st.markdown(f'<div class="card-emoji">{m["emoji"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-title">{m["name"]} Mode</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-desc">{m["tagline"]}</div>', unsafe_allow_html=True)
                st.button(
                    f"Pick {m['name']}",
                    key=f"mode_{key}",
                    on_click=choose_mode,
                    args=(key,),
                )
    st.stop()

# ---------------- Screen 2: chat ----------------
mode = MODES[st.session_state.mode]

with st.sidebar:
    st.markdown("### 🎭 Mood Bot")
    st.markdown(
        f'<span class="mode-badge">{mode["emoji"]} {mode["name"]} Mode</span>',
        unsafe_allow_html=True,
    )
    st.caption(mode["tagline"])
    st.divider()
    st.button("🔄 Change mode", on_click=reset)
    st.caption("Type **0** in the chat to exit the application.")

head_l, head_r = st.columns([3, 1])
with head_l:
    st.markdown(f"## {mode['emoji']} {mode['name']} Chatbot")
with head_r:
    st.markdown(
        f'<div style="text-align:right;padding-top:1rem">'
        f'<span class="mode-badge">{mode["name"]}</span></div>',
        unsafe_allow_html=True,
    )
st.divider()

# Greeting when the chat is empty
if len(st.session_state.messages) == 1:
    st.info(f"You're chatting in **{mode['name']} mode**. Say something to begin!")

# Render history (system message hidden)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=mode["emoji"]):
            st.write(msg.content)

if st.session_state.ended:
    st.success("Chat ended. Use **Change mode** in the sidebar to start a new one.")
    st.stop()

prompt = st.chat_input("You :")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))

    if prompt == "0":
        st.session_state.ended = True
        st.rerun()

    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=mode["emoji"]):
        with st.spinner(f"{mode['name']} bot is thinking..."):
            response = model.invoke(st.session_state.messages)
        st.write(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.rerun()