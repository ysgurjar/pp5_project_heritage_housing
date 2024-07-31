import streamlit as st
import pandas as pd
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

    st.subheader("Business Requirement-1")
    st.write(
        "The client is interested in discovering how the house attributes correlate with the sale price. Therefore, the client expects data visualisations of the correlated variables against the sale price to show that."
    )
