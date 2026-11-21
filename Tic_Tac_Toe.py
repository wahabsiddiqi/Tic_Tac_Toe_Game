import numpy as np
import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")

SYMBOLS = {0: "\u2003", 1: "X", -1: "O"}


# ---------- Game logic (same as your original) ----------
def check_winner(b):
    if 3 in np.sum(b, axis=0) or 3 in np.sum(b, axis=1):
        return "X"
    if -3 in np.sum(b, axis=0) or -3 in np.sum(b, axis=1):
        return "O"
    if np.trace(b) == 3 or np.trace(np.fliplr(b)) == 3:
        return "X"
    if np.trace(b) == -3 or np.trace(np.fliplr(b)) == -3:
        return "O"
    if not 0 in b:
        return "Draw"
    return None


# ---------- Session state ----------
def reset_board():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current_player = 1
    st.session_state.result = None


if "board" not in st.session_state:
    reset_board()
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}


def play(row, col):
    """Callback jab koi cell click ho."""
    if st.session_state.result is not None:
        return
    if st.session_state.board[row, col] != 0:
        return

    st.session_state.board[row, col] = st.session_state.current_player
    result = check_winner(st.session_state.board)

    if result is not None:
        st.session_state.result = result
        st.session_state.scores[result] += 1
    else:
        st.session_state.current_player *= -1


# ---------- UI ----------
st.markdown(
    """
    <style>
    div.stButton > button {
        height: 5rem;
        font-size: 2rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎮 Tic Tac Toe")

# Scoreboard
c1, c2, c3 = st.columns(3)
c1.metric("Player X", st.session_state.scores["X"])
c2.metric("Player O", st.session_state.scores["O"])
c3.metric("Draws", st.session_state.scores["Draw"])

st.divider()

# Status message
result = st.session_state.result
if result is None:
    turn = "X" if st.session_state.current_player == 1 else "O"
    st.info(f"Player **{turn}** turns! ⏳")
elif result == "Draw":
    st.warning("Ohhhh, It's a draw! 🤝")
else:
    st.success(f"Player {result} wins! 🎉")

# Board
board = st.session_state.board
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        cols[c].button(
            SYMBOLS[int(board[r, c])],
            key=f"cell_{r}_{c}",
            on_click=play,
            args=(r, c),
            disabled=(board[r, c] != 0 or st.session_state.result is not None),
            use_container_width=True,
        )

st.write("")
b1, b2 = st.columns(2)
b1.button("🔄 New Game", on_click=reset_board, use_container_width=True)


def reset_all():
    reset_board()
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}


b2.button("🗑️ Reset Scores", on_click=reset_all, use_container_width=True)