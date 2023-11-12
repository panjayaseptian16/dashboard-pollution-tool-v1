import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import sqlite3

tab1,tab2,tab3 = st.tabs(['Hypotesis Testing','SWOT Analysis', 'Recommendation'])
with tab1: 
    with st.expander('Source_Data'):
        st.markdown(
            """
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 16px;
                }

                th, td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 12px;
                }

                th {
                    background-color: #183D3D;
                }

                td a {
                    color: #1e90ff;
                    text-decoration: none;
                    transition: color 0.3s ease;
                }

                td a:hover {
                    color: #0077cc;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <table>
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>MRT Terpadat</td>
                        <td><a href="https://kumparan.com/kumparannews/stasiun-mrt-lebak-bulus-gerbang-suar-jakarta-yang-selalu-dipadati-pengunjung-21MZHQJB9aw">Link</a></td>
                    </tr>
                    <tr>
                        <td>KRL Terpadat</td>
                        <td><a href="https://commuterline.id/informasi-publik/berita/commuterline-jabodetabek-layani-lebih-dari-442-ribu-pengguna-hingga-sore-ini">Link</a></td>
                </tbody>
            </table>
            """,unsafe_allow_html=True
        )


def run_hypothesis_test(query_before, query_after, label_before, label_after):
    # Connect to the SQLite database
    conn = sqlite3.connect('pollution.db')  # Replace 'pollution.db' with your database name
    cursor = conn.cursor()

    # Execute the query for before the event
    result_before = pd.read_sql_query(query_before, conn)

    # Execute the query for after the event
    result_after = pd.read_sql_query(query_after, conn)

    # Close the database connection
    conn.close()

    # Conduct an independent t-test
    t_stat, p_value = ttest_ind(result_before['median'], result_after['median'], equal_var=False)

    # Set the significance level (alpha)
    alpha = 0.05

    # Define the number of tests for Bonferroni correction
    num_tests = 2

    # Calculate Bonferroni-adjusted significance level
    bonferroni_alpha = alpha / num_tests

    # Define the null hypothesis (H0) and alternative hypothesis (H1)
    h0 = f"There is no significant difference between the median AQI {label_before} and {label_after}."
    h1 = f"There is a significant difference between the median AQI {label_before} and {label_after}."

    # Display the test results along with H0 and H1
    st.write(f"bonferroni_alpha: {bonferroni_alpha}")
    st.write(f"H0: {h0}")
    st.write(f"H1: {h1}")
    st.write(f"T-Test Results ({label_before} vs {label_after}):")
    st.write("T-Statistic:", t_stat)
    st.write("P-Value:", p_value)
    

    # Perform hypothesis testing with Bonferroni correction
    if p_value < bonferroni_alpha:
        st.write(f"Reject H0: {h0} (With Bonferroni Correction)")
        plot_boxplot_difference(result_before, result_after, label_before, label_after)
        plot_distribution_comparison(result_before, result_after, label_before, label_after)
    else:
        st.write(f"Not enough evidence to reject H0: {h0} (With Bonferroni Correction)")
    st.divider()
def plot_boxplot_difference(result_before, result_after, label_before, label_after):
    # Combine the results using Pandas
    merged_result = pd.concat([result_before['median'], result_after['median']], axis=1)
    merged_result.columns = [label_before, label_after]

    # Create a boxplot
    fig, ax = plt.subplots()
    sns.boxplot(data=merged_result, ax=ax)
    ax.set_ylabel('Median AQI (PM2.5)')
    ax.set_title(f'Comparison of AQI Distribution {label_before} and {label_after}')
    st.pyplot(fig)

def plot_distribution_comparison(result_before, result_after, label_before, label_after):
    # Create a distribution plot
    fig, ax = plt.subplots()
    sns.kdeplot(result_before['median'], label=label_before, fill=True)
    sns.kdeplot(result_after['median'], label=label_after, fill=True)
    ax.set_xlabel('Median AQI (PM2.5)')
    ax.set_ylabel('Density')
    ax.set_title(f'Comparison of AQI Distribution {label_before} and {label_after}')
    ax.legend()
    st.pyplot(fig)
    st.write("Conclusion: The analysis suggests a significant difference in the AQI distribution before and during the WFH event.")
    st.write("However, it appears that the AQI increased during the WFH event.")

# Run hypothesis test for before and after the event
run_hypothesis_test(
    "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (date BETWEEN '2023-06-20' AND '2023-08-20') ORDER BY date",
    "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (date BETWEEN '2023-08-21' AND '2023-10-21') ORDER BY date",
    "Before WFH Event",
    "WFH Event"
)

# Run hypothesis test for 2 months before and after the event
run_hypothesis_test(
    "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (date BETWEEN '2022-08-21' AND '2022-10-21') ORDER BY date",
    "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (date BETWEEN '2023-08-21' AND '2023-10-21') ORDER BY date",
    "2 Months Before",
    "WFH Event"
)


