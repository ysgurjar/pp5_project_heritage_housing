import streamlit as st

def page_ml_sale_predict_body():
    st.info(
        """
        - The pipeline was tunes aiming for R2 score of at least 0.7 on train and test set.

        - The pipeline performance on train and test set is 0.87 and 0.79 respectively.

        - Additional efforts were made to reduce R2 score difference between train and test set
        to reduce overfitting.

        - Additional efforts were made to reduce complexity of pipeline while maintaining performance.
        """
    )