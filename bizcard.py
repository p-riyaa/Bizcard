import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import easyocr
import pandas as pd
import numpy as np
import re
import psycopg2
import cv2
# from config import load
curr = None
conn = None
#connection to Postgresql
try:
    # reader = easyocr.Reader(['en'])
    conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="MyDB123")
    curr = conn.cursor()
    curr.execute('''
     CREATE TABLE IF NOT EXISTS Biz_card 
                      (id SERIAL PRIMARY KEY ,
                      name VARCHAR(25),
                      designation VARCHAR(25),
                      organization VARCHAR(25),
                      contact VARCHAR(25),
                      email VARCHAR(25),
                      website VARCHAR(25),
                      area VARCHAR(25),
                      city VARCHAR(25),
                      state VARCHAR(25),
                      pincode VARCHAR(25)
                      )
                      ''')
    conn.commit()
    def extract_text(image):
        reader = easyocr.Reader(['en'], gpu=True)
        text_para = reader.readtext(image, detail=0, paragraph=True)
        text = reader.readtext(image, detail=0, paragraph=False)
        name = text[0]
        des = text[1]
        op = {}
        contact = []
        for i in text:
            if '-' in i:
                contact.append(i)

        mail = ''
        for i in text:
            if "@" in i:
                mail = i
                break

        web = ''
        for i in text:
            if '.com' in i:
                if 'www' in i or 'wwW' in i:

                    web = i
                else:
                    web = ("www." + i)

        adds = ''
        for i in text_para:
            if len(i) > 30:
                adds = i

        address = adds.replace(';', ',')

        area_pattern = r'\b\d+\s+\w+\s+St\b'  # r'^123.*?St'
        area = re.findall(area_pattern, address)

        city_pattern = r',\s*([\w\s]+),\s*TamilNadu'
        city = re.findall(city_pattern, address)

        state_pattern = 'TamilNadu'
        state = re.findall(state_pattern, address)

        pin_pattern = r'\d{6,7}'
        pincode = re.findall(pin_pattern, address)

        if '.' not in text_para[-1]:
            org = text_para[-1]
        else:
            org = text_para[-2]

        op = {
            "Name": name,
            "Designation": des,
            "Organization": org,
            "Contact": contact,
            "Email_Id": mail,
            "Website": web,
            "Area": area,
            "City": city,
            "State": state,
            "Pincode": pincode
        }
        return op
    st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR", page_icon=':credit_card:',
                       layout='wide')
    #Background
    st.markdown(
        """<style>.main {background-color: #FADBD8;}</style>""",unsafe_allow_html=True
    )
    selected = option_menu(
    menu_title="BizCardX-Extracting Business Card Data with OCR",
    options = ["Home","Upload & Extract","Retrive & Update","Delete"],
    icons = ["house","database-add","building-add","calendar-x"],
    # default_index = 0,
    orientation="horizontal",
    styles={
    "nav-link": {
    "font-size": "25px",
    "font-family": "Fira Sans",
    "font-weight": "Bold",
    "text-align": "center",
    "margin": "-3px",
    "--hover-color": "#E7D4D4"#Grayish red
    },
    "icon": {"font-size": "25px"},
    "container": {"max-width": "4000px"},
    }
    )
    if selected == "Home":
        col1, col2 = st.columns(2)
        with col1:
            st.write("## :red[**How to Use?**]")
            st.write("### * Upload your business card image in :red[**Scan/edit**] page and scan you card. Now card details are displayed in the page.")
            st.write("### * If you need to modify the information edit the information or just add it in the database by clicking the ")
            st.write("### * If you need to remove any data which is expired or not in use that can be easily done in :red[**Delete**] page")
            st.write("### * Input the data you no longer need and click delete button to remove your card information from backend")

        with col2:
            st.image(Image.open("C:\\Users\\Pooja\\Downloads\\cardscannerhome.jpg"), width=300)
            st.write(
            "### :red[**Your Problem:**]Sifting through stacks of business cards and keeping track of contacts can feel like a daunting task")
            st.write(
            "### :red[**Our Solution:**]You have find the right place to transform your business card into CRM Contact in seconds, So you will"
            " spend less time in inputting data and more time creating great customer experiences."
            )
    if selected == "Upload & Extract":
        file_upload = st.file_uploader(":red[:credit_card:***UPLOAD YOUR CARD HERE***]",
                                       type=["jpg", "jpeg", "png", "tiff", "tif", "gif"])
        # st.image(
        #     "https://media.istockphoto.com/id/1006701810/video/identity-icon-animation.jpg?s=640x640&k=20&c=Fkn8E8fbyEVoCbCQZkyTvYNpsApscoF8ekuZAWIlQsI=", )

        if file_upload is not None:
            image = cv2.imdecode(np.frombuffer(file_upload.read(), np.uint8), 1)
            st.image(image, caption='Card Uploaded Successfully', width=500)
            if st.button('Extract & Store'):
                data = extract_text(image)
                st.write("Extracted Data from the Card :")
                st.dataframe(data)
                with conn.cursor() as curr:
                        postgres_insert_query = "INSERT INTO Biz_card (name, designation, organization, contact, email, website, area, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        record_to_insert = (
                             data["Name"],
                             data["Designation"],
                             data["Organization"],
                             data["Contact"][0],
                             data["Email_Id"],
                             data["Website"],
                             data["Area"][0],
                             data["City"][0],
                             data["State"][0],
                             data["Pincode"][0],
                             )
                        curr.execute(postgres_insert_query, record_to_insert)
                        conn.commit()
                st.success("Above Data Inserted Successfully in the Database")
    if selected == "Retrive & Update":
        select_query = "Select * from biz_card"

        curr.execute(select_query)
        table = curr.fetchall()
        conn.commit()

        table_df = pd.DataFrame(table,columns=("id","Name","Designation","Organization","Contact","Email","Website",
                                                                "Area","City","state","Pincode"))
        col1,col2 = st.columns(2)
        with col1:
            selected_name = st.selectbox("Select the Name",table_df["Name"] )
        df1 = table_df[table_df["Name"] == selected_name]
        st.dataframe(df1)
        df2 = df1.copy()

        col1,col2 = st.columns(2)
        with col1:
            modname = st.text_input("Name",df1["Name"].unique()[0])
            df2["Name"] = modname
            moddes = st.text_input("Designation",df1["Designation"].unique()[0])
            df2["Designation"] = moddes
            modorg = st.text_input("Organization",df1["Organization"].unique()[0])
            df2["Organization"] = modorg
            modcon = st.text_input("Contact", df1["Contact"].unique()[0])
            df2["Contact"] = modcon
            modmail = st.text_input("Email", df1["Email"].unique()[0])
            df2["Email"] = modmail


        with col2:
            modweb = st.text_input("Website", df1["Website"].unique()[0])
            df2["Website"] = modweb
            modarea = st.text_input("Area", df1["Area"].unique()[0])
            df2["Area"] = modarea
            modcity = st.text_input("City", df1["City"].unique()[0])
            df2["City"] = modcity
            modst = st.text_input("state", df1["state"].unique()[0])
            df2["state"] = modst
            modpin = st.text_input("Pincode", df1["Pincode"].unique()[0])
            df2["Pincode"] = modpin
        st.write("UPDATED DATA")
        st.dataframe(df2)
        col1,col2 = st.columns(2)
        with col1:
            buttonclick = st.button("MODIFY", use_container_width=True)

        if buttonclick:
            curr.execute(f'''UPDATE biz_card SET name = '{modname}',
                            designation = '{moddes}', organization = '{modorg}',
                            contact = '{modcon}', email = '{modmail}' , website = '{modweb}',
                            area = '{modarea}', city = '{modcity}', state = '{modst}', pincode = '{modpin}'
                            where name = '{selected_name}' 
                                ''')
            conn.commit()
            st.success("Successfully updated in database !!!")



    if selected == "Delete" :
        select_query = "Select * from biz_card"

        curr.execute(select_query)
        table = curr.fetchall()
        conn.commit()

        table_df = pd.DataFrame(table,columns=("id", "Name", "Designation", "Organization", "Contact", "Email", "Website",
                                         "Area", "City", "state", "Pincode"))
        col1, col2 = st.columns(2)
        with col1:
            selected_name = st.selectbox("Select the Name", table_df["Name"])
        df1 = table_df[table_df["Name"] == selected_name]
        st.dataframe(df1)
        col1,col2 = st.columns(2)
        with col1:
                    buttonclick = st.button("DELETE", use_container_width=True)

        if buttonclick:
                    curr.execute(f'''DELETE FROM biz_card where name = '{selected_name}' ''')
                    conn.commit()
                    st.success("Successfully Deleted from database !!!")

except Exception as error:
    print(error)
    print("exception occurred")

