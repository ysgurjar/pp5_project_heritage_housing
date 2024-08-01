import streamlit as st
from app_pages.multipage import MultiPage

# load pages scripts
from app_pages.page_summary import page_summary_body
from app_pages.page_sale_price_study import page_sale_price_study_body
from app_pages.page_sale_price_prediction import page_sale_price_prediction
from app_pages.page_project_hypothesis import page_project_hypothesis_body

app = MultiPage(app_name= "Sale Price Study") # Create an instance of the app 

# Add your app pages here using .add_page()
app.add_page("Sale Price Prediction", page_sale_price_prediction)
app.add_page("Sale Price Correlations",page_sale_price_study_body)
app.add_page("Quick Project Summary", page_summary_body)
app.add_page("Project Hypothesis",page_project_hypothesis_body)

app.run() # Run the  app