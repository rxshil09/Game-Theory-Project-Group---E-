import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

# Payoff matrix
payoffs = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (1, 1)
}

# Strategy functions
def always_cooperate(_, __): return 'C'
def always_defect(_, __): return 'D'
def tit_for_tat(my_hist, opp_hist): return 'C' if not opp_hist else opp_hist[-1]

strategies = {
    "Always Cooperate": always_cooperate,
    "Always Defect": always_defect,
    "Tit for Tat": tit_for_tat
}

# Simulate one match
def play_match(strat1, strat2, rounds):
    history1, history2 = [], []
    score1 = 0

    for _ in range(rounds):
        move1 = strat1(history1, history2)
        move2 = strat2(history2, history1)
        payoff1, _ = payoffs[(move1, move2)]
        score1 += payoff1
        history1.append(move1)
        history2.append(move2)

    return score1

# UI Layout
st.title("🎲 Prisoner's Dilemma Simulator")
st.write("Compare strategies in an iterated Prisoner's Dilemma.")

rounds = st.slider("Number of Rounds", 10, 200, 100)

# Run tournament and collect data
names = list(strategies.keys())
results = []

for name1 in names:
    row = []
    for name2 in names:
        score = play_match(strategies[name1], strategies[name2], rounds)
        row.append(score)
    results.append(row)

# Create a DataFrame for results
df = pd.DataFrame(results, columns=names, index=names)

# Plotting
st.subheader("📊 Strategy Performance")
fig, ax = plt.subplots()
width = 0.2
x = range(len(names))

for idx, strategy in enumerate(names):
    ax.bar([i + width * idx for i in x], df.loc[strategy], width=width, label=strategy)

ax.set_xticks([i + width for i in x])
ax.set_xticklabels(names)
ax.set_ylabel("Score")
ax.set_title("Scores Against Other Strategies")
ax.legend()
st.pyplot(fig)

# Show table
st.subheader("📋 Score Table")
st.dataframe(df)

# CSV download
csv = df.to_csv()
st.download_button(
    label="📥 Download CSV Report",
    data=csv,
    file_name='prisoners_dilemma_results.csv',
    mime='text/csv'
)