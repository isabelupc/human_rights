import streamlit as st
import json

with open('human_rights.json', 'r') as file:
    data = json.load(file)

st.title('Drets Humans per a nens')

import matplotlib.pyplot as plt
 
# Create data

level1 = 30
level2 = 30
level3 = 10

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot bars in stack manner
ax.bar(' ', level1, color='g')
ax.bar(' ', level2, bottom=level1, color='orange')
ax.bar(' ', level3, bottom=level1+level2, color='r')

ax.set_yticks([30, 60, 90])  # Set specific y-ticks to show
ax.axis('off')  # Turn off all axes

# Use Streamlit to display the figure
st.pyplot(fig)

st.write(f"Correct answers in streak:  👑")
