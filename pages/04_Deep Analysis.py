import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import sqlite3

st.set_page_config(
    page_title="Deep Analysis",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto"
    )


tab1,tab2,tab3 = st.tabs(['Hypotesis Testing','SWOT Analysis', 'Recommendation'])
with tab1: 
    hypothesis_option = st.selectbox("Select Hypothesis Test", ["Hypothesis 1: Impact of WFH and WFO Policy on Air Quality", "Hypothesis 2"])
    # Hypothesis 1
    if hypothesis_option == "Hypothesis 1: Impact of WFH and WFO Policy on Air Quality":
            st.markdown('##')
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
                                <td>WFH Policy 1</td>
                                <td><a href="https://jdih.maritim.go.id/cfind/source/files/surat-edaran/2023semenpanrb017.pdf">Link</a></td>
                            </tr>
                            <tr>
                                <td>WFH Policy 2</td>
                                <td><a href="https://news.detik.com/berita/d-6887325/asn-di-jakarta-mulai-wfh-50-persen-hari-ini-simak-kebijakan-lengkapnya">Link</a></td>
                            </tr>
                        </tbody>
                    </table>
                    """,unsafe_allow_html=True
                )

            # Hypothesis 1
            st.header("Hypothesis 1: Impact of WFH and WFO Policy on Air Quality")

            hypothesis_1_description = """
            I am assessing the impact of the Work From Home (WFH) and Work From Office (WFO) policy over two months (Aug 21, 2023, to Oct 21, 2023), aligning with "Surat Edaran MenPAN-RB No.17/2023".

            **Comparison 1: During Policy vs. Before Policy (Same Year)**
            - **Same-year conditions:** Control for external factors, ensuring a direct policy impact comparison.
            - **Two months before policy:** Crucial, given historical high AQI levels in June and July; cross-year analysis enhances effectiveness insights.
            - **Type I Error Control:** Apply Bonferroni correction for multiple test control.

            **Comparison 2: During Policy vs. Before Policy (Previous Year)**
            - **Previous-year conditions:** Consistency and control for year-specific variations.
            - **Two months before policy:** Establish baseline; consider historical trends.
            - **Type I Error Control:** Apply Bonferroni correction.

            Ensuring a robust analysis, considering within-year and cross-year perspectives, while controlling potential errors via Bonferroni correction.
            """

            st.write(hypothesis_1_description)
            st.divider()

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
                st.write(f"**Bonferroni Alpha:** {bonferroni_alpha}")
                st.write(f"**H0:** {h0}")
                st.write(f"**H1:** {h1}")
                st.write(f"**T-Test Results ({label_before} vs {label_after}):**")
                st.write("**T-Statistic:**", t_stat)
                st.write("**P-Value:**", p_value)
                

                # Perform hypothesis testing with Bonferroni correction
                if p_value < bonferroni_alpha:
                    st.write(f"**Reject H0:** {h1} (With Bonferroni Correction)")
                    plot_distribution_comparison(result_before, result_after, label_before, label_after)
                else:
                    st.write(f"**Not enough evidence to reject H0:** {h0} (With Bonferroni Correction)")
                st.divider()

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
                st.write("**Conclusion: The analysis suggests a significant difference in the AQI distribution before and during the WFH event.**")
                st.write("**However, it appears that the AQI did not increase during the WFH event**")

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
                "Same Month (2022)",
                "WFH Event (2023)"
            )
    elif hypothesis_option == "Hypothesis 2":
        
        st.write(hypothesis_2_description)



