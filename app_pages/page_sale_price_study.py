import streamlit as st
from src.data_management import load_housing_data
import matplotlib.pyplot as plt
import seaborn as sns
import ppscore as pps

sns.set_style("whitegrid")
import numpy as np
import plotly.express as px


def page_sale_price_study_body():
    """
    Display correlated features and a checkbox to show the show
    house price per correlated variable.
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

    df = load_housing_data()

    if st.checkbox("Inspect dataset"):
        st.write(f"* The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
        st.write(
            """* The last column ```SalePrice``` is our taget variable for finding correlation."""
        )
        st.write("""
            * Sale Price is in USD and area measurement is in square feet. For additional variable \
            definition and metadata, refer to the project [ReadMe](https://github.com/ysgurjar/pp5_project_heritage_housing)\
            on Github.
            """)
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

    # ==== Code to generate plots ====

    # create a custom dict to display categories labels instead of names on plots

    var_labels = {
        "1stFlrSF": "1st Floor Square Feet",
        "GarageArea": "Garage Area",
        "GrLivArea": "Ground Living Area",
        "TotalBsmtSF": "Total Basement Square Feet",
        "OverallQual": "Overall Quality",
        "GarageFinish": "Garage Finish",
        "KitchenQual": "Kitchen Quality",
        "YearBuilt": "Original Construction Year",
        "GarageYrBlt": "Year Garage was Built",
    }

    # create a custom order dict for categorical variables to define plotting order

    cat_var_order = {
        "OverallQual": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "KitchenQual": ["Fa", "TA", "Gd", "Ex"],
        "GarageFinish": ["None", "Unf", "RFn", "Fin"],
    }

    # plot categorical variables

    def plot_cat_var():
        cat_var = ["OverallQual", "GarageFinish", "KitchenQual"]

        for x in cat_var:
            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
            p = sns.boxplot(data=df, y="SalePrice", x=x, order=cat_var_order[x])
            p.axes.set_title(f"Sale Price vs {var_labels[x]}", fontsize=30)
            p.axes.set_ylabel("Sale Price", fontsize=20)
            p.axes.set_xlabel(var_labels[x], fontsize=20)
            # Show the plot
            st.pyplot(fig)

    # plot numerical variables
    def plot_num_var():
        num_var = [
            "GrLivArea",
            "TotalBsmtSF",
            "1stFlrSF",
            "GarageArea",
            "YearBuilt",
            "GarageYrBlt",
        ]

        for x in num_var:
            # sns.set_theme()
            # sns.set_context('paper')
            plt.figure(figsize=(15, 15))  # Set the figure size for each subplot
            if x in ("YearBuilt", "GarageYrBlt"):
                p = sns.lineplot(data=df, x=x, y="SalePrice")
                # Inspired from https://python-charts.com/seaborn/lines/
                # Add a vertical line to seperate two trends
                p.axvline(x=1950, color="black", linestyle="dashed")
            else:
                # set robust = True reduce the effect of outliers
                p = sns.regplot(
                    data=df, x=x, y="SalePrice", marker="x", robust=True
                )
            p.set_title(f"Sale Price vs {var_labels[x]}", fontsize=30)  # Setting title for each plot

            # set labels
            plt.xlabel(var_labels[x], fontsize=20)  # Optionally set the x-axis label
            plt.ylabel("Sale Price", fontsize=20)  # Optionally set the y-axis label
            # Show the plot
            st.pyplot(plt)

    if st.checkbox("Show Correlation Plots"):
        plot_cat_var()
        plot_num_var()
