import streamlit as st
from src.data_management import load_housing_data
import matplotlib.pyplot as plt
import seaborn as sns
import ppscore as pps

sns.set_style("whitegrid")
from feature_engine.discretisation import ArbitraryDiscretiser
import numpy as np
import plotly.express as px


def page_sale_price_study_body():
    """
    Display correlated features and a checkbox to show the show
    house price per variable.
    """

    # Subheader : Business requirement
    st.subheader("Business Requirement-1")
    st.info(
        "The client is interested in discovering how the house attributes\
         correlate with the sale price. Therefore, the client expects data\
         visualisations of the correlated variables against the sale price to show that."
    )    
    # Inspect dataset
    st.subheader("Explore Dataset")

    df= load_housing_data()

    if(st.checkbox( "Inspect dataset")):
        st.write(f'The dataset has {df.shape[0]} rows and {df.shape[1]} columns.')
        st.write("""The last column ```SalePrice``` is our taget variable for finding correlation.""")
        st.write(df)

    # Correlated variables summary
    st.subheader("Correlation Study Summary")
    st.write(
        "A correlation study was carried out to explore linear and non linear relationship.\
        The following variables showed better correlation with sale prices compare to rest of them.\
        These **correlations can be linear or non-linear**."
    )

    st.info(
            """
            - **Size** :
                - **First Floor Square feet** (1stFlrSF): Larger the area, higher the price
                - **Garage Area** (GarageArea): Larger the area, higher the price
                - **Ground Living Area** (GrLivArea) : Larger the area, higher the price
                - **Total Basement Square Feet** (TotalBsmtSF): Larger the area, higher the price
            - **Quality** :
                - **Overall Quality** (OverallQual): Better the quality, higher the price
                - **Garage Finish** (GarageFinish) : Houses finished garages have typically higher prices compare\
                    to unfinished garages
                - **Kitchen Quality** (KitchenQual): Better the quality, higher the price
            - **Time** :
                - **Original Consutruction Year** (YearBlt) : The house prices look relatively flat until 1950\
                    but after that newer houses typically have higher prices
                - **Year Garage was built** (GarageYrBlt) : The house prices look relatively flat until 1950\
                    but after that newer houses typically have higher prices. PS: This field contains a lot of missing values\
                    so be careful to analyse it.
            """
        )
    
    if(st.checkbox( "Show Correlation Plots")):
        st.write(f'The dataset has {df.shape[0]} rows and {df.shape[1]} columns.')
        st.write("""The last column ```SalePrice``` is our taget variable for finding correlation.""")
        st.write(df)
    
    ## ==== Code to generate plots ===