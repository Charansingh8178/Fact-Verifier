import streamlit as st
from PIL import Image
import base64
import requests
from io import BytesIO
import time

# ---- Set page config ----
st.set_page_config(page_title="Fact Checker", layout="wide")

# Function to convert image file to base64
def img_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to set the background image using PIL and CSS
def set_image_as_page_bg(image_file):
    img = Image.open(image_file)
    img_base64 = img_to_base64(img)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{img_base64}") no-repeat center center fixed;
            background-size: cover;
        }}

        .title-text {{
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 57px;
            color: black;
            font-weight: bold;
            text-align: center;
            z-index: 100;
            text-shadow: 1px 1px 2px white;
        }}

        .left-text {{
            margin-top: 150px;
            margin-left: 10px;
            font-size: 28px;
            color: black;
            font-weight: bold;
            text-shadow: 1px 1px 2px white;
        }}

        .proceed-button {{
            margin-left: 800px;
            margin-top: 20px;
        }}

        .fact_page {{
            margin-left: 10px;
            margin-top:10px;
            font-size: 90px;
            font-weight: bold;
        }}

        .text {{
            margin-top: 90px;
            margin-left: 10px;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            text-shadow: 1px 1px 2px white;
        }}

        .home-button button {{
            font-size: 25px !important;
            padding: 10px 24px;
            margin-top: 100px !important;
            margin-left: 700px;
            color: white;
            border-radius: 8px;
        }}

        .custom-button {{
            font-size: 22px !important;
            padding: 10px 20px !important;
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 10px !important;
            text-align: center;
            cursor: pointer;
        }}
        
        </style>
        """,
        unsafe_allow_html=True,
    )

def welcome_page():
    set_image_as_page_bg('FACT.jpg')  
    st.markdown('<div class="title-text">Welcome to Fact Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="left-text">Please click the button below to proceed.</div>', unsafe_allow_html=True)
    
    #proceed = st.markdown('<div class="custom-button" >Click here to proceed</div>', unsafe_allow_html=True)
    
    proceed = st.button("Click here to proceed", key="proceed_button")    

    if proceed:
        st.session_state.page = "fact_check_page"
        st.balloons()
        st.rerun()

    

api_key =  1                                    #YOUR API KEY HERE  
def preprocess(question):
    clean= question.lower().strip()
    clean=clean.replace("is it true that","")
    clean=clean.replace("?","")
    return clean.strip()

def fact_checking(question, api_key):
    clean = preprocess(question)  
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": clean,
        "languageCode": "en-US",
        "pageSize": 5,
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        return results
    else:
        st.error(f"Error: {response.status_code}")
        return None

def fact_check_page():
    set_image_as_page_bg('FACT1.jpg')
    st.markdown('<div class="fact_page"> Fact Check Page </div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Get your Myths cleared  </div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:30px; margin-top:80px; font-weight:bold; ">Enter your Question:</div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Target the text input container */
    div[data-testid="stTextInput"] {
        margin-top: 10px;
        font-size: 50px;
        height: 2.5em !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    question = st.text_input(" ", key="user_input", placeholder="Type your question here...")  
    
    
    check_button = st.markdown('<div class="custom-button" >CHECK FACT!</div>', unsafe_allow_html=True)

    if check_button and question.strip() != "":  
        st.write("Your Question:", question)
        with st.spinner("Finding Truth 🔥!!!"):
            time.sleep(3) 

            result = fact_checking(question, api_key)

            if result and 'claims' in result:
                for claim in result['claims']:
                    st.subheader(f"Claim: {claim.get('text')}")
                    for review in claim.get('claimReview', []):
                        st.write(f"**Publisher:** {review.get('publisher', {}).get('name')}")
                        st.write(f"**Title:** {review.get('title')}")
                        st.write(f"[Read More]({review.get('url')})")
                        st.write(f"**Rating:** {review.get('textualRating')}")
                        st.write("---")
            else:
                st.warning("No fact-checked claims were found for this question. Please try rephrasing or asking a different question.!!!")


    st.write(" ")
    st.write(" ")
    
    spacer= st.empty()
    spacer.write(" ")
    
    spacer= st.empty()

    
    if st.button('🏠 Home', key="button-2"):
        st.session_state.page = 'welcome_page'
        st.rerun()


if 'page' not in st.session_state:
    st.session_state.page = "welcome_page"

if st.session_state.page == "welcome_page":
    welcome_page()
elif st.session_state.page == "fact_check_page":
    fact_check_page()
