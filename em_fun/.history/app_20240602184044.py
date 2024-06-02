import streamlit as st
import sqlite3

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
            st.success(f'Welcome, {username}!')
        else:
            st.error('Invalid username or password')
else:
    st.success(f'Welcome, {st.session_state.username}!')
    
    # Group A-F 1.2. place
    group_dict = {
        'A': ['Turkey', 'Italy', 'Wales', 'Switzerland'],
        'B': ['Denmark', 'Finland', 'Belgium', 'Russia'],
        'C': ['Netherlands', 'Ukraine', 'Austria', 'North Macedonia'],
        'D': ['England', 'Croatia', 'Scotland', 'Czech Republic'],
        'E': ['Spain', 'Sweden', 'Poland', 'Slovakia'],
        'F': ['Hungary', 'Portugal', 'France', 'Germany']
    }

    # champion, vice champion, third place, fourth place
    champion_dict = {
        "champion": ["Turkey", "Italy", "Netherlands", "England", "Spain", "Hungary"],
        "vice_champion": ["Italy", "Turkey", "Ukraine", "Croatia", "Sweden", "Portugal"],
        "third_place": ["Switzerland", "Wales", "Austria", "Scotland", "Poland", "France"],
        "fourth_place": ["Wales", "Switzerland", "North Macedonia", "Czech Republic", "Slovakia", "Germany"]
    }

    st.header('Vote for Group Positions')
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
        st.success('Your votes have been submitted!')
