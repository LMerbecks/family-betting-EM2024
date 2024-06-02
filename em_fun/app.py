import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import pandas as pd

def generate_hash(username, vote_id):
    hash_input = f"{username}-{vote_id}-{datetime.now()}"
    return hashlib.sha256(hash_input.encode()).hexdigest()


def init_votes_db():
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id TEXT PRIMARY KEY,
            vote_id TEXT NOT NULL,
            vote_value TEXT NOT NULL,
            username TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_votes(username, votes):
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()
    for vote_id, vote in votes.items():
        unique_id = generate_hash(username, vote_id)
        c.execute("INSERT INTO votes (id, vote_id, vote_value, username, date) VALUES (?, ?, ?, ?, ?)", (unique_id, vote_id, vote["vote_value"], username, vote['date']))
    conn.commit()
    conn.close()

def get_all_votes():
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM votes')
    all_votes = c.fetchall()
    conn.close()
    
    # Convert to DataFrame
    df = pd.DataFrame(all_votes, columns=['ID', 'Vote ID', "Vote Value", 'Username', 'Date'])
    return df


# Function to initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Insert a test user (optional, only insert if table is empty)
    c.execute("INSERT INTO users (username, password) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username=?)", ('admin', 'password', 'admin'))
    conn.commit()
    conn.close()

# Function to check user credentials
def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    return result

# Initialize the database
init_db()
init_votes_db()

# Streamlit app
st.title('EM 2024 Gewinnspiel by Merbecks')

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login section
if not st.session_state.logged_in:
    st.header('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    login_button = st.button('Login')

    if login_button:
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
            st.success(f'Welcome, {username}!')
        else:
            st.error('Invalid username or password')
else:
    st.success(f'Welcome, {st.session_state.username}!')
    
    if st.session_state.username == 'admin':
        st.header('All User Votes Overview')
        all_votes_df = get_all_votes()
        if not all_votes_df.empty:
            st.dataframe(all_votes_df)
        else:
            st.write("No votes have been submitted yet.")
    else:
        st.header('Vote for Group Positions')
        # Group A-F 1.2. place
        group_dict = {
        "A": ["Germany", "Scotland", "Hungary", "Switzerland"],
        "B": ["Spain", "Croatia", "Italy", "Albania"],
        "C": ["Slovenia", "Denmark", "Serbia", "England"],
        "D": ["Poland", "Netherlands", "Austria", "France"],
        "E": ["Belgium", "Slovakia", "Romania", "Ukraine"],
        "F": ["Turkey", "Georgia", "Portugal", "Czech Republic"]
        }
        
        champion_dict = {
            "champion": ["Germany", "Scotland", "Hungary", "Switzerland", "Spain", "Croatia", "Italy", "Albania", "Slovenia", "Denmark", "Serbia", "England", "Poland", "Netherlands", "Austria", "France", "Belgium", "Slovakia", "Romania", "Ukraine", "Turkey", "Georgia", "Portugal", "Czech Republic"],
            "vice_champion": ["Germany", "Scotland", "Hungary", "Switzerland", "Spain", "Croatia", "Italy", "Albania", "Slovenia", "Denmark", "Serbia", "England", "Poland", "Netherlands", "Austria", "France", "Belgium", "Slovakia", "Romania", "Ukraine", "Turkey", "Georgia", "Portugal", "Czech Republic"],
            "third_place": ["Germany", "Scotland", "Hungary", "Switzerland", "Spain", "Croatia", "Italy", "Albania", "Slovenia", "Denmark", "Serbia", "England", "Poland", "Netherlands", "Austria", "France", "Belgium", "Slovakia", "Romania", "Ukraine", "Turkey", "Georgia", "Portugal", "Czech Republic"],
            "fourth_place": ["Germany", "Scotland", "Hungary", "Switzerland", "Spain", "Croatia", "Italy", "Albania", "Slovenia", "Denmark", "Serbia", "England", "Poland", "Netherlands", "Austria", "France", "Belgium", "Slovakia", "Romania", "Ukraine", "Turkey", "Georgia", "Portugal", "Czech Republic"]
        }

        group_positions = {}

        for group, countries in group_dict.items():
            st.subheader(f'Group {group}')
            first_place = st.selectbox(f'Select 1st place for Group {group}', countries, key=f'1st_{group}')
            second_place = st.selectbox(f'Select 2nd place for Group {group}', [c for c in countries if c != first_place], key=f'2nd_{group}')
            group_positions[group] = {
                '1st_place': first_place,
                '2nd_place': second_place
            }

        st.header('Vote for Champions and Positions')
        champion = st.selectbox('Select the Champion', champion_dict['champion'])
        vice_champion = st.selectbox('Select the Vice Champion', [c for c in champion_dict['vice_champion'] if c != champion])
        third_place = st.selectbox('Select the Third Place', [c for c in champion_dict['third_place'] if c != champion and c != vice_champion])
        fourth_place = st.selectbox('Select the Fourth Place', [c for c in champion_dict['fourth_place'] if c != champion and c != vice_champion and c != third_place])

        st.header('Your Selections')
        st.subheader('Group Positions')
        for group, positions in group_positions.items():
            st.write(f"Group {group}: 1st - {positions['1st_place']}, 2nd - {positions['2nd_place']}")

        st.subheader('Champions')
        st.write(f"Champion: {champion}")
        st.write(f"Vice Champion: {vice_champion}")
        st.write(f"Third Place: {third_place}")
        st.write(f"Fourth Place: {fourth_place}")

        if st.button('Submit'):
            # Prepare votes data
            votes = {}
            for group, positions in group_positions.items():
                votes[f'{group}_1st_place'] = {"vote_value": positions['1st_place'], 'username': st.session_state.username, 'date': str(datetime.now())}
                votes[f'{group}_2nd_place'] = {"vote_value": positions['2nd_place'], 'username': st.session_state.username, 'date': str(datetime.now())}
            votes['champion'] = {'vote_value': champion, 'username': st.session_state.username, 'date': str(datetime.now())}
            votes['vice_champion'] = {'vote_value': vice_champion, 'username': st.session_state.username, 'date': str(datetime.now())}
            votes['third_place'] = {'vote_value': third_place, 'username': st.session_state.username, 'date': str(datetime.now())}
            votes['fourth_place'] = {'vote_value': fourth_place, 'username': st.session_state.username, 'date': str(datetime.now())}

            # Save votes to the database
            save_votes(st.session_state.username, votes)
            
            st.success('Your votes have been submitted!')