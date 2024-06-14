import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
current_directory = os.getcwd()

# Streamlit app
st.title('EM 2024 Tippspiel')
# file_path = 

st.markdown(current_directory)

# List all files and directories in the current working directory
files_and_directories = os.listdir(current_directory)

# Display the list
st.markdown("**Contents of the current working directory:**")
for item in files_and_directories:
    st.markdown(f"- {item}")

# groups = pd.read_parquet(os.path.join(current_directory, "group_votes.parquet"))
# groups.columns = groups.columns.get_level_values(1)
# groups["Punkte"] = 2

# ranks = pd.read_parquet(os.path.join(current_directory, "overall_votes.parquet"))

# st.markdown("## Gruppen-Tipps")
# st.table(groups) 

# st.markdown("## Europameister Tipps")
# st.table(ranks.set_index("Tipp")) 

# # Plot a bar chart with the leading person


# st.markdown("## Live Tippstand")

# # Sample data
# data = {
#     'Names': ['Augi', 'Consi', 'Lele', 'Lia & Klaus', 'Mama', 'Oma', 'Papa'],
#     'Points': [0, 1, 0, 0, 0, 0, 0]
# }

# df = pd.DataFrame(data)

# # Create bar chart with different colors for each bar
# colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink', 'lightseagreen', 'lightsteelblue']
# plt.style.use('dark_background')

# # Create bar chart with different colors for each bar and additional horizontal lines
# plt.figure(figsize=(10, 6))
# plt.bar(df['Names'], df['Points'], color=colors)
# plt.axhline(y=5, color='blue', linestyle='--', label='Anfänger')
# plt.axhline(y=12, color='red', linestyle='--', label='Heimlicher Tipico Wettstudio Besucher')
# # plt.axhline(y=17, color='green', linestyle='--', label='Profi Tipper')

# plt.xlabel('Tipper')
# plt.ylabel('Punkte')
# plt.title('Live Tippstand')
# plt.xticks(rotation=45)
# plt.legend()
# plt.tight_layout()

# # Show plot
# st.pyplot(plt)

