import streamlit as st

def page_project_hypothesis_body():
    st.write("### Project Hypotheses and Validation")

    # conclusions taken from "03 - Correlation_Study" notebook
    st.success(
        """
        - The client did not present any hypothesis upfront, but after discussion
        the client informed us that she will expect higher price for properties with larger 
        built up area. So, that formed the basis for our hypothesis.
        
        - This hypothesis is **Correct**.

        - Pearson correlation, which accounts for linear relation shows 0.6 to 0.7 score between
        sale price and

            - Above Ground Living Area (GrLivArea)
            - Total square feet of Basement Area (TotalBsmtSF)
            - 1st floor square feet (1stFlrSF)
            - Garage Area (GarageArea)

        - Additionally, ML algorithm with performance R2 score greater than 0.7 also idetified GrLivArea and Garage Area to be two
        of the top 5 parameters affecting sale price.

        This evidence is statastically significant to say that the hypothesis is correct.

        """
    )
