import streamlit as st
import pandas as pd

def page_sale_price_prediction():
    """
    Displays sale price prediction for inherited
    as well as property with any given feautures in Iowa
    """
    # subheader
    st.subheader("Estimated sale price for client's inherited houses")

    st.write("* Find below 4 inherited houses profile and their estimated sale price")

    df=pd.DataFrame({'Hey':[1,2,3]})
    
    st.write(df)

    st.write(f'The sum of predicted sale price is {df.sum(axis=1)}')

    st.subheader("Predicted house sales prices in Ames, Iowa")


    st.button("Run Predictive Analysis")

    st.info(f'The predicted sale price for this house in Iowa is')