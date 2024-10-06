import pandas as pd
from datetime import datetime
import os
import numpy as np
import pickle
import json

import streamlit as st

st.set_page_config(
    page_title="Bangalore House Price Prediction",
    page_icon="🏡",  # Unicode emoji or path to a custom icon
)

login_signup_css = """
<style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar.st-emotion-cache-1itdyc2.eczjsme18 > div.st-emotion-cache-6qob1r.eczjsme11 > div.st-emotion-cache-1gwvy71.eczjsme12 > div > div > div > div > div:nth-child(1) > div > div > h1 > em{
    color:Red;
    }


    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8{
        background-image: url('https://t3.ftcdn.net/jpg/03/55/60/70/360_F_355607062_zYMS8jaz4SfoykpWz5oViRVKL32IabTP.jpg');
        background-size: cover;
        background-position: center;
    }

    #sing-up-login-required{
        color: rgb(0,0,0);
        font-weight: bold;
        }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(3) > div > label > div > p{
        color: rgb(0,0,0);
        font-weight: bold;
        font-size:20px;
        }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(3) > div > div > label:nth-child(1) > div.st-ba.st-bp.st-bq.st-br.st-bs.st-bt.st-bu.st-bv.st-bw.st-bx.st-by > div > p{
        color: rgb(0,0,0);
        font-weight: bold;
        font-size:20px;
        }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(3) > div > div > label:nth-child(2) > div.st-ba.st-bp.st-bq.st-br.st-bs.st-bt.st-bu.st-bv.st-bw.st-bx.st-by > div > p{
        color: rgb(0,0,0);
        font-weight: bold;
        font-size:20px;
        }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(4) > div > label > div > p{
        color: rgb(0,0,0);
        font-weight: bold;
        font-size:20px;
        }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(5) > div > label > div > p{
        color: rgb(0,0,0);
        font-weight: bold;
        font-size:20px;
    }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(7) > div > div{
            background-color: rgb(0,0,0); /* Light green background */
            color: rgb(255,255,255); /* Dark green text */
            # padding: 10px;
            border-radius: 8px;
            font-size:10px;
            # border: 1px solid #c3e6cb; /* Green border */
        }

</style>


        


<script type="text/javascript">
        window.onbeforeunload = function() {
            return 'Are you sure you want to leave? Changes you made may not be saved.';
        };
</script>
"""

main_app_css = """
<style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8{
        background-image: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGJlYXV0aWZ1bCUyMGhvdXNlfGVufDB8fDB8fHww');
        background-size: cover;
        background-position: center;
        opacity:0.6px;
    }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(7) > div > button > div > p{
        font-size:30px;}

    # #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(3) > div > div{
    #     background-color:#272625;
    #     border-color:rgb(0,0,0);
    #     }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(3) > div > div > div > div > div > div > p{
            color:rgb(0,0,0);
            background-color:#272625;
            font-weight: bold;
            font-size:20px;
            }

    #bangalore-house-price-predictor{
        background-color:black;
        align-content:center;
        padding:1rem;
        border-radius:10px;
        color: rgb(255,255,255);
        font-weight: bold;
        -webkit-text-stroke: 1px black;
        }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div.stForm.st-emotion-cache-qcpnpn.e10yg2by1 > div > div > div > div:nth-child(1) > div > label > div > p{
        background-color:#272625;
        padding:5px;
        border-radius:8px;
        font-weight: bold;
        font-size:20px;
        color: rgb(255,255,255);
        }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div.stForm.st-emotion-cache-qcpnpn.e10yg2by1 > div > div > div > div:nth-child(2) > div > label > div > p{
        background-color:#272625;
        padding:5px;
        border-radius:8px;
        font-weight: bold;
        font-size:20px;
        color: rgb(255,255,255)}

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div.stForm.st-emotion-cache-qcpnpn.e10yg2by1 > div > div > div > div:nth-child(3) > div > label > div > p{
        background-color:#272625 ;
        padding:5px;
        border-radius:8px;
        font-weight: bold;
        font-size:20px;
        color: rgb(255,255,255);}

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div.stForm.st-emotion-cache-qcpnpn.e10yg2by1 > div > div > div > div:nth-child(4) > div > label > div > p{
        background-color:#272625;
        padding:5px;
        border-radius:8px;
        font-weight: bold;
        font-size:20px;
        color: rgb(255,255,255);}

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(4){
        padding:8px;
        margin
        border-radius:5px;
        background-color:black;
        }
</style>

<script type="text/javascript">
        window.onbeforeunload = function() {
            return 'Are you sure you want to leave? Changes you made may not be saved.';
        };
</script>
"""

st.sidebar.title("*! IMPORTANT NOTICE !*")
page = st.sidebar.markdown("""<div><b>Here is a important instruction for all Users!<br>
 •Please click <font color = "red">TWICE</font> on LOGIN/LOGOUT button to proceed further processing, "its due to Security Purpose!"<br><br>
 •User for the first time must Signup then only he/she will be able to Login.<br></b>
                           
<h2><font color = "red">NOTE:-</font></h2>
<b>•The site is under development.
If you face any error ignore them and proceed, we are working on it. Sorry for the inconvenience!.<br><br>
***THANK YOU FOR YOUR SUPPORT!***</b> 
Contact us: kishan03.gupta@gmail.com<br><br>
Copyright © 2012 - 2024 TermsFeed®. All rights reserved.</div>""",unsafe_allow_html=True)


# Function to log signup data in signup_history.csv
def log_signup_data(username, password):
    now =datetime.now()
    signup_data = {
        "date": [now.date()],
        "day": [now.strftime("%A")],
        "time": [now.strftime("%H:%M:%S")],
        "username": [username],
        "password": [password]
    }
    df = pd.DataFrame(signup_data)
    
    # Append to signup_history.csv
    with open("signup_history.csv", "a") as f:
        df.to_csv(f, header=f.tell() == 0, index=False)

# Function to log login data in login_history.csv
def log_login_data(username):
    now =datetime.now()
    login_data = {
        "date": [now.date()],
        "day": [now.strftime("%A")],
        "time": [now.strftime("%H:%M:%S")],
        "username": [username],
    }
    df = pd.DataFrame(login_data)
    
    # Check if the file exists and append, else create new
    with open("login_history.csv", "a") as f:
        df.to_csv(f, header=f.tell() == 0, index=False)

# Function to check if a username already exists in signup_history.csv
def user_exists(username):
    if os.path.isfile("signup_history.csv"):
        df = pd.read_csv("signup_history.csv")
        return username in df['username'].values
    return False

# Function to verify if the provided username and password are correct
def verify_user(username, password):
    if os.path.isfile("signup_history.csv"):
        df = pd.read_csv("signup_history.csv")
        user_row = df[df['username'] == username]
        return not user_row.empty and user_row['password'].values[0] == password
    return False


import streamlit as st
# from auth import log_signup_data, log_login_data, user_exists, verify_user

# Set up Streamlit page
# st.set_page_config(page_title="My Web App", layout="wide")

if 'option' not in st.session_state:
    st.session_state.option = "Sign Up"  # Default option


# Initialize session state for login status and inputs
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username_input' not in st.session_state:
    st.session_state.username_input = ""
if 'password_input' not in st.session_state:
    st.session_state.password_input = ""

# Function to clear input fields in session state
# def clear_input_fields():
#     st.session_state.username_input = ""
#     st.session_state.password_input = ""

# Function to display the authentication form
def display_authentication():
    st.markdown(login_signup_css, unsafe_allow_html=True)
    st.header("Sing up/Login Required")

    option = st.radio("Select an option:", ["Sign Up", "Login"],horizontal=True)

    button_text = "Sign Up" if option == "Sign Up" else "Login"

    username = st.text_input("Username:", value=st.session_state.username_input, key="username_input")
    password = st.text_input("Password:", type="password", value=st.session_state.password_input, key="password_input")

    if st.button(button_text):
        if username == "" or password == "":
            st.error("Invalid Credentials!\nPlease enter both username and password.")
        else:
            if option == "Sign Up":
                if user_exists(username):
                    st.error("Username already exists. Please log in or choose a different username.")
                else:
                    log_signup_data(username, password)
                    st.success("Sign up successful! You can now log in.")
                    # clear_input_fields()  # Clear the input fields after sign-up
            elif option == "Login":
                if verify_user(username, password):
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    log_login_data(username)  # Log the login attempt
                    # clear_input_fields()  # Clear the input fields after login
                else:
                    st.error("Invalid username or password.")

def display_main_content():
    st.markdown(main_app_css, unsafe_allow_html=True)

    popup_placeholder = st.empty()


    def show_popup(message, message_type="info"):
        if message_type == "success":
            popup_placeholder.success(message)

        elif message_type == "error":
            popup_placeholder.error(message)

        elif message_type == "warning":
            popup_placeholder.warning(message)
        else:
            popup_placeholder.info(message)

    with open('banglore_home_prices_model.pkl', 'rb') as f:
        model = pickle.load(f)

    def predict_price(area, bhk, bath, location):
            # Assuming that the model takes input in the order [area, bhk, bath, location_encoded]
            loc_index = locations.index(location)
            x = np.zeros(len(locations))
            x[0] = area
            x[1] = bhk
            x[2] = bath
            x[loc_index] = 1
            return model.predict([x])[0]

    notice_message="""<div1><h2>Note:-</h2><h5>All prediction are subjected to datasets used at the time of training the model. The amount which is predicting on the screen can be different from the real world.
    (Predited Price will shown above this message, Scroll up after clicking on Button "Price Predict").</h5></div1>"""

    st.markdown(notice_message,unsafe_allow_html=True)
        # Create a Streamlit app interface
    st.title("Bangalore House Price Predictor!")


    
    with st.form(key="Bangalore House Price Prediction"):
        # User input fields for the model
            area = st.number_input("Enter the area in square feet:", min_value=500, max_value=30000, step=50)
            bhk = st.number_input("Enter the number of BHK:", min_value=2, max_value=16, step=1)
            bath = st.number_input("Enter the number of bathrooms:", min_value=1, max_value=16, step=1)

        # Location selection
            locations = [ "1st block jayanagar", "1st phase jp nagar", "2nd phase judicial layout", "2nd stage nagarbhavi", "5th block hbr layout", "5th phase jp nagar", "6th phase jp nagar", "7th phase jp nagar", "8th phase jp nagar", "9th phase jp nagar", "aecs layout", "abbigere", "akshaya nagar", "ambalipura", "ambedkar nagar", "amruthahalli", "anandapura", "ananth nagar", "anekal", "anjanapura", "ardendale", "arekere", "attibele", "beml layout", "btm 2nd stage", "btm layout", "babusapalaya", "badavala nagar", "balagere", "banashankari", "banashankari stage ii", "banashankari stage iii", "banashankari stage v", "banashankari stage vi", "banaswadi", "banjara layout", "bannerghatta", "bannerghatta road", "basavangudi", "basaveshwara nagar", "battarahalli", "begur", "begur road", "bellandur", "benson town", "bharathi nagar", "bhoganhalli", "billekahalli", "binny pete", "bisuvanahalli", "bommanahalli", "bommasandra", "bommasandra industrial area", "bommenahalli", "brookefield", "budigere", "cv raman nagar", "chamrajpet", "chandapura", "channasandra", "chikka tirupathi", "chikkabanavar", "chikkalasandra", "choodasandra", "cooke town", "cox town", "cunningham road", "dasanapura", "dasarahalli", "devanahalli", "devarachikkanahalli", "dodda nekkundi", "doddaballapur", "doddakallasandra", "doddathoguru", "domlur", "dommasandra", "epip zone", "electronic city", "electronic city phase ii", "electronics city phase 1", "frazer town", "gm palaya", "garudachar palya", "giri nagar", "gollarapalya hosahalli", "gottigere", "green glen layout", "gubbalala", "gunjur", "hal 2nd stage", "hbr layout", "hrbr layout", "hsr layout", "haralur road", "harlur", "hebbal", "hebbal kempapura", "hegde nagar", "hennur", "hennur road", "hoodi", "horamavu agara", "horamavu banaswadi", "hormavu", "hosa road", "hosakerehalli", "hoskote", "hosur road", "hulimavu", "isro layout", "itpl", "iblur village", "indira nagar", "jp nagar", "jakkur", "jalahalli", "jalahalli east", "jigani", "judicial layout", "kr puram", "kadubeesanahalli", "kadugodi", "kaggadasapura", "kaggalipura", "kaikondrahalli", "kalena agrahara", "kalyan nagar", "kambipura", "kammanahalli", "kammasandra", "kanakapura", "kanakpura road", "kannamangala", "karuna nagar", "kasavanhalli", "kasturi nagar", "kathriguppe", "kaval byrasandra", "kenchenahalli", "kengeri", "kengeri satellite town", "kereguddadahalli", "kodichikkanahalli", "kodigehaali", "kodigehalli", "kodihalli", "kogilu", "konanakunte", "koramangala", "kothannur", "kothanur", "kudlu", "kudlu gate", "kumaraswami layout", "kundalahalli", "lb shastri nagar", "laggere", "lakshminarayana pura", "lingadheeranahalli", "magadi road", "mahadevpura", "mahalakshmi layout", "mallasandra", "malleshpalya", "malleshwaram", "marathahalli", "margondanahalli", "marsur", "mico layout", "munnekollal", "murugeshpalya", "mysore road", "ngr layout", "nri layout", "nagarbhavi", "nagasandra", "nagavara", "nagavarapalya", "narayanapura", "neeladri nagar", "nehru nagar", "ombr layout", "old airport road", "old madras road", "padmanabhanagar", "pai layout", "panathur", "parappana agrahara", "pattandur agrahara", "poorna pragna layout", "prithvi layout", "r.t. nagar", "rachenahalli", "raja rajeshwari nagar", "rajaji nagar", "rajiv nagar", "ramagondanahalli", "ramamurthy nagar", "rayasandra", "sahakara nagar", "sanjay nagar", "sarakki nagar", "sarjapur", "sarjapur  road", "sarjapura - attibele road", "sector 2 hsr layout", "sector 7 hsr layout", "seegehalli", "shampura", "shivaji nagar", "singasandra", "somasundara palya", "sompura", "sonnenahalli", "subramanyapura", "sultan palaya", "tc palaya", "talaghattapura", "thanisandra", "thigalarapalya", "thubarahalli", "tindlu", "tumkur road", "ulsoor", "uttarahalli", "varthur", "varthur road", "vasanthapura", "vidyaranyapura", "vijayanagar", "vishveshwarya layout", "vishwapriya layout", "vittasandra", "whitefield", "yelachenahalli", "yelahanka", "yelahanka new town", "yelenahalli", "yeshwanthpur", "total_sqft", "bath", "bhk",]
            location = st.selectbox("Select the location:", locations)

            submit_button = st.form_submit_button("Predict Price")

    # show_popup("All prediction are subjected to datasets used at the time of training the model. The amount which is predicting on the screen can be different from the real world.", "warning")

    if submit_button:
        if model:  # Ensure the model is loaded
            prediction = predict_price(area, bhk, bath, location)
            st.button(f'The predicted price of the house is: ₹ {prediction:.2f} Lakhs', "success")
        else:
            show_popup("Prediction model is not available.", "error")




    file_path = 'banglore_home_prices_model.pkl'

    try:
            with open(file_path, 'rb') as f:
                model = pickle.load(f)
    except FileNotFoundError:
            st.error(f"The file {file_path} was not found.")
    except pickle.UnpicklingError:
            st.error("Error occurred while unpickling the file.")
    except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if st.session_state.logged_in and st.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()


# Main app logic
if not st.session_state.logged_in:
    display_authentication()
else:
    display_main_content()

