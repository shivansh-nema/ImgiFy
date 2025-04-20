import json
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from PIL import Image
import google.generativeai as genai

api_key = st.secrets["API_KEY"]
headers = {
    "authorization": api_key,
    "content-type": "application/json"
}
model_name = "gemini-2.0-flash"

genai.configure(api_key=api_key)
ai_model = genai.GenerativeModel(model_name)

st.set_page_config(
    page_title="ImgiFy",
    page_icon="Imgify_Favicon.png",
)

page_bg_img = """   
<style>
.block-container {
        padding-top: 2.5rem !important;
}

[data-testid="stAppViewContainer"]{
    background-image: url(https://images.unsplash.com/photo-1638742385167-96fc60e12f59?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D) 
}

[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}

[data-testid="stSidebarContent"]{
    background-color: rgb(240, 240, 240);
}

[data-testid="stHeadingWithActionElements"]{
    font-size: 50px;
}

[data-testid="stImageContainer"]{
    width: 420px;
    height: 415px;
}

[data-testid="stButton"]{
    display: flex;
    align-items: center;
    justify-content: center;
}

[data-testid="stBaseButton-secondary"]{
    padding: 0px 20px;
    border-radius: 30px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

def generate_description(input_image, description_prompt):
    open_image = Image.open(input_image)
    response = ai_model.generate_content([description_prompt, open_image])
    return response.text

st.title("ImgiFy")
st.write("An AI-powered shopping app leverages advanced image recognition and generative AI to enhance your shopping experience. Simply upload an image, and the app accurately detects products, provides detailed descriptions, and suggests similar or alternative items. Designed for ease and efficiency, it helps users make informed buying decisions with minimal effort.")

with st.sidebar:
    input_image = st.file_uploader("Upload Image:", type=["jpg", "png"])

if input_image:
    with st.sidebar:    
        st.image(input_image, caption="Uploaded Image", width=350)

    description_prompt ="Describe this product for an online shopping app. Include style, color, material, and category."
    recommendation_prompt = (
        f"Recommand 5 similar products to a {input_image} with there shopping links"
        f"And Don't show the Disclaimer"
    )

    user_choice = option_menu(
        "What are you looking for?", 
        options=["Product Description", "Similar Recommendations"], 
        icons=["file-earmark-text-fill","window-stack"], 
        menu_icon="arrow-right-circle-fill",  
        default_index=0, 
        orientation="horizontal",
    )

    if st.button("Generate"):
        if user_choice == "Product Description":
            st.subheader("→ Product Description:-")
            with st.spinner("Generating description..."):
                description = generate_description(input_image, description_prompt)
                st.write(description)
        else:
            st.subheader("→ Similar Recommendations")
            with st.spinner("Generating recommendation..."):
                recommendations = generate_description(input_image, recommendation_prompt)
                st.write(recommendations)