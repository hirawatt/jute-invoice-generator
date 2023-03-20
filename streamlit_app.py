import pdfkit
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
import base64

# credentials
page_title = st.secrets['initialize']['page_title']
sidebar_title = st.secrets['initialize']['sidebar_title']
website = st.secrets['credits']['website']
name = st.secrets['credits']['name']
buymeacoffee = st.secrets['credits']['buymeacoffee']
api_key = st.secrets['api_key']
api_secret = st.secrets['api_secret']

# streamlit
st.set_page_config(
    '{}'.format(page_title),
    '🖨',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        "Get Help": "{}".format(website),
        "About": "Jute Invoice Generator",
    },
)

col1, col2 = st.columns(2)
col1.header('🌱 ' + page_title)
col2.header("📜 Generated Invoice")

current_directory = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(current_directory), autoescape=select_autoescape())
template = env.get_template("/invoice/invoice_template.html")

# variables
company_name_list = st.secrets["data"]["company_name_list"]
company_address_data = st.secrets["data"]["company_address_data"]
company_website = st.secrets["data"]["company_website"]
company_phone1 = st.secrets["data"]["company_phone1"]
company_phone2 = st.secrets["data"]["company_phone2"]
customer_name_list = st.secrets["data"]["customer_name_list"]
customer_address_list = st.secrets["data"]["customer_address_list"]
product_type_list = st.secrets["data"]["product_type_list"]
hsn = st.secrets["data"]["hsn"]
year = st.secrets["data"]["year"]


with col1.form("template_form"):
    l, r = st.columns(2)
    invoice_number = l.number_input("Invoice No.", min_value=1, step=1)
    date = r.date_input("Select Date")
    # company details
    company_name = r.selectbox("Company name", company_name_list)
    company_address = r.text_input("Company address", value=company_address_data)
    # customer details
    customer_name = l.selectbox("Customer name", customer_name_list)
    customer_address = r.text_input("Customer address", value=customer_address_list[0])
    # invoice details
    c1, c2, c3, c4 = st.columns(4)
    product_type = c1.selectbox("Product type", product_type_list)
    quantity = c2.number_input("Quantity", 1, 10)
    price_per_unit = c3.number_input("Price per unit")
    # logistics details
    less = c1.checkbox("Less")
    claims = c2.checkbox("Claims")
    moisture = c3.checkbox("Moisture")
    # invoice display
    color = c1.color_picker("Color", value="#b4cffa")
    no_of_products = c2.number_input("Select no. of products")
    # calculations
    total = price_per_unit * quantity
    submit = st.form_submit_button()

html = template.render(
    invoice_number=invoice_number,
    date=date,
    company_name=company_name,
    company_address=company_address,
    customer_name=customer_name,
    customer_address=customer_address,
    product_type=product_type,
    quantity=quantity,
    price_per_unit=price_per_unit,
    total=total,
    color=color,
    hsn=hsn,
)

pdf = pdfkit.from_string(html, False)

with col2:
    components.html(html, height = 800)

st.success("🎉 Your invoice was generated!")

st.download_button(
    "⬇️ Download Invoice",
    data=pdf,
    file_name="invoice-{}-{}.pdf".format(invoice_number, year),
    mime="application/octet-stream",
    use_container_width=True
)
