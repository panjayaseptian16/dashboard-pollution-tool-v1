import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import streamlit as st

# Define bonferroni_alpha if it's not defined already
bonferroni_alpha = 0.05

def run_hypothesis_test(query_dry_season, query_rainy_season, label_dry_season, label_rainy_season):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('pollution.db')  # Replace 'pollution.db' with your database name
        cursor = conn.cursor()

        # Execute the query for the dry season
        result_dry_season = pd.read_sql_query(query_dry_season, conn)

        # Execute the query for the rainy season
        result_rainy_season = pd.read_sql_query(query_rainy_season, conn)

    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return

    finally:
        # Close the database connection
        conn.close()

    # Conduct an independent t-test
    t_stat, p_value = ttest_ind(result_dry_season['median'], result_rainy_season['median'], equal_var=False)

    # Set the significance level (alpha)
    alpha = 0.05

    # Define the null hypothesis (H0) and alternative hypothesis (H1)
    h0 = f"There is no significant difference between the median AQI {label_dry_season} and {label_rainy_season}."
    h1 = f"There is a significant difference between the median AQI {label_dry_season} and {label_rainy_season}."

    # Display the test results along with H0 and H1
    st.write(f"**Alpha:** {alpha}")
    st.write(f"**H0:** {h0}")
    st.write(f"**H1:** {h1}")
    st.write(f"**T-Test Results ({label_dry_season} vs {label_rainy_season}):**")
    st.write("**T-Statistic:**", t_stat)
    st.write("**P-Value:**", p_value)

    # Perform hypothesis testing with Bonferroni correction
    if p_value < bonferroni_alpha:
        st.write(f"**Reject H0:** {h1}")
        plot_distribution_comparison(result_dry_season, result_rainy_season, label_dry_season, label_rainy_season)
    else:
        st.write(f"**Not enough evidence to reject H0:** {h0}")
    st.divider()


def plot_distribution_comparison(result_before, result_after, label_before, label_after):
    # Create a distribution plot
    fig, ax = plt.subplots()
    sns.kdeplot(result_before['median'], label=label_before, fill=True, color='chocolate')  # Set color for dry season
    sns.kdeplot(result_after['median'], label=label_after, fill=True, color='skyblue')     # Set color for rainy season
    ax.set_xlabel('Median AQI (PM2.5)')
    ax.set_ylabel('Density')
    ax.set_title(f'Comparison of AQI Distribution {label_before} and {label_after}')
    ax.legend()
    st.pyplot(fig)
    st.write("**Conclusion: The analysis suggests a significant difference in the AQI distribution before and during the WFH event.**")
    st.write("**However, it appears that the AQI did not increase during the WFH event**")

# Run hypothesis test for dry season vs. rainy season across all available years
run_hypothesis_test(
    "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (strftime('%m', date) BETWEEN '04' AND '09') ORDER BY date",
    "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (strftime('%m', date) IN ('10','11','12','01','02','03')) ORDER BY date",
    "Dry Season (April-September)",
    "Rainy Season (October-March)"
)

