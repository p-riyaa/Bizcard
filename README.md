# Bizcard
# BizCardX: Extracting Business Card Data with OCR

# Introduction  
Business card data extraction using Optical Character Recognition (OCR) is a cutting-edge technology that streamlines the process of digitizing contact information from physical business cards. By harnessing the power of OCR, businesses can efficiently convert printed text on business cards into digital data, enabling easy integration into contact management systems and enhancing networking and customer relationship management efforts. 

# Overview  
In Streamlit web app, you can upload an image of a business card and extract relevant information such as Name, Designation, Company, Contact Details, Address Details etc from it using easyOCR method. You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information. 

# Tools Installed  
PyCharm Community Edition 2023.3.3 
PgAdmin 4(PostgreSQL) 

# Required Libraries 
Streamlit, Easyocr, CV2, Mysql-connector-python, Pandas, RE, Matplotlib 

# ETL and EDA Process 
a) Extracting the data - Extract the business card data by using easyocr. 
b) Transforming the data - After the extraction process, the text data extracted is converted into structured data in the form of dataframe. 
c) Loading data after - The transformation process, the data in the form of dataframe is stored in the MySQL database. 
d) Visualizing, Updating, deleting the data - The extracted data can be visualized using matplotlib and in the form of dataframe. 
The data can also be updated, modified and deleted from the database. 

# User Guide 

**Step 1** - Home Tab provides a brief overview of the project and the tools required for the project. 
**Step 2** - Upload and Extract Tab allows to browse a business card file (image) using “Browse Files” button and upload the image in upload here section. The image will be processed, and the required data will be collected. The processed image will appear with collected data in the text format. Click “Extract & Store” button to store the data in the backend “pgAdmin”. The details are displayed in dataframe format in the UI Screen. User will get a Success message as” Above Data Inserted Successfully in the Database” if the extracted data is stored in DB. 
**Step 3** - Retrieve & Update Tab we can retrieve the information of the selected user from the dropdown and alter the data collected from a business card. Upload the modified data to the database and then we can view the modified data as well.  
**Step 4** - Delete Tab used for deleting the information of the person which is no longer needed. Just select the Username from the Dropdown and click “DELETE” button to remove that row from the db. Success message “Successfully Deleted from database !!!” is rendered when done. 
