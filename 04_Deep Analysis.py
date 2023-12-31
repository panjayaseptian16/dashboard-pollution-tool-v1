import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import sqlite3
import base64
import scipy.stats as stats

st.set_page_config(
    page_title="Deep Analysis",
    page_icon="🕵️‍♂️",
    layout="centered",
    initial_sidebar_state="auto"
    )

with st.sidebar: 
    file_ = open("us_epa.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    gif_url = "https://aqicn.org/scale/"
    st.markdown(
    f'<div style="text-align:left;">'
    f'<a href="{gif_url}" target="_blank">'
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" style="max-width:100%; cursor: pointer;">'
    f'</a></div>',
    unsafe_allow_html=True)
    st.markdown("<p style='margin-top:10px; text-align: center; font-size: 14px; color:#FFFD8C;'>Air Quality Index (AQI) scale as defined by the US-EPA 2016 standard. Check details in <a href='https://aqicn.org/scale/'>here</a></p>",
        unsafe_allow_html=True)
    
tab1,tab2,tab3 = st.tabs(['Hypotesis Testing','SWOT Analysis', 'Recommendation'])
with tab1: 
    hypothesis_option = st.selectbox("Select Hypothesis Test", ["Hypothesis 1: Impact of WFH and WFO Policy on Air Quality", "Hypothesis 2: Comparison of Air Pollution Levels on Dry Season and Rainy Season"], index=None)
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
                st.pyplot(fig,use_container_width=True)
                st.caption("_The Air Quality Index (AQI) is presented on the sidebar, where higher values indicate poorer air quality. Moving towards the right corresponds to higher AQI values and a decrease in air quality._")
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
    elif hypothesis_option == "Hypothesis 2: Comparison of Air Pollution Levels on Dry Season and Rainy Season":
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
                                <td>Season in Indonesia</td>
                                <td><a href="https://regional.kompas.com/read/2022/07/23/154321578/mengenal-2-jenis-musim-di-indonesia-musim-hujan-dan-musim-kemarau?page=all">Link</a></td>
                            </tr>
                        </tbody>
                    </table>
                    """,unsafe_allow_html=True
                )

        # Hypothesis 2
        st.header("Hypothesis 2: Comparison of Air Pollution Levels on Dry Season and Rainy Season")

        hypothesis_2_description = """
            I am evaluating the disparities in air pollution levels between the Dry Season (April-September) and Rainy Season (October-March) over a span of 6 years (Jan 01, 2018, to Oct 29, 2023).

            **Comparison: Dry Season vs. Rainy Season (Previous Year)**
            - **Previous-year conditions:** Maintaining consistency and controlling for year-specific variations enhances the reliability of the analysis.

            Considering both within-year and cross-year perspectives ensures a robust analysis.
            """
        st.write(hypothesis_2_description)
        st.divider()

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

            # Perform hypothesis testing
            if p_value < alpha:
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
            st.pyplot(fig,use_container_width=True)
            st.caption("_The Air Quality Index (AQI) is presented on the sidebar, where higher values indicate poorer air quality. Moving towards the right corresponds to higher AQI values and a decrease in air quality._")
            st.write("**Conclusion: The analysis reveals a significant difference in the AQI distribution between the Dry Season (April-September) and the Rainy Season (October-March).**")
            st.write("**The null hypothesis (H0) is rejected, suggesting that there is indeed a decrease in air quality during the Dry Season.**")

        # Run hypothesis test for dry season vs. rainy season across all available years
        run_hypothesis_test(
            "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (strftime('%m', date) BETWEEN '04' AND '09') ORDER BY date",
            "SELECT median FROM daily_aqi WHERE indicator LIKE '%pm25%' AND (strftime('%m', date) IN ('10','11','12','01','02','03')) ORDER BY date",
            "Dry Season (April-September)",
            "Rainy Season (October-March)"
        )

with st.container():
    with tab2: 
        import streamlit as st

        # Custom CSS styling for a more visually appealing presentation
        custom_style = """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
                text-align: center;
            }

            .card {
                padding: 20px;
                margin: 20px;
                background-color: #183D3D;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: box-shadow 0.3s ease;
                text-align:left;
            }

            .card:hover {
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                transform: scale(1.05);
            }

            .fade-in {
                opacity: 0;
                animation: fadeIn 1s forwards;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
        </style>
        """

        # Injecting custom CSS
        st.markdown(custom_style, unsafe_allow_html=True)

        # Layout
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # Strengths
        with col1:
            st.markdown("<div class='card fade-in' style='background-color: #183D3D;'>"
                        "<h2 style='font-size:18px;'>Strengths</h2>"
                        "<ol>"
                        "<li><b>Seasonal Patterns Awareness:</b> Understanding and leveraging knowledge of seasonal pollution patterns for targeted interventions.</li>"
                        "<li><b>Identification of Critical Pollutants:</b> Pinpointing major pollutants (CO, NO2, PM2.5, PM10, O3) allows for precise mitigation strategies.</li>"
                        "<li><b>Data-Driven Forecasting:</b> Utilizing forecasting models like Prophet for proactive measures and resource allocation.</li>"
                        "<li><b>Public Awareness Preferences:</b> Recognizing user priorities (Health Impact, High Pollution Notifications) for effective communication.</li>"
                        "</ol>"
                        "</div>", unsafe_allow_html=True)

        # Weaknesses
        with col2:
            st.markdown("<div class='card fade-in' style='background-color: #183D3D;>"
                        "<h2 style='font-size:18px;'>Weaknesses</h2>"
                        "<ol>"
                        "<li><b>Ineffective Policies:</b> Presence of unhealthy AQI levels suggests ineffective policies or enforcement.</li>"
                        "<li><b>Weekend Variation:</b> Higher AQI on Sundays indicates a potential gap in pollution control measures during weekends.</li>"
                        "<li><b>Limited Impact During WFH:</b> Despite WFH, overall AQI did not increase, suggesting potential weaknesses in remote work scenarios.</li>"
                        "</ol>"
                        "</div>", unsafe_allow_html=True)

        # Opportunities
        with col3:
            st.markdown("<div class='card fade-in' style='background-color: #183D3D;>"
                        "<h2 style='font-size:18px;'>Opportunities</h2>"
                        "<ol>"
                        "<li><b>Targeted Intervention During Dry Season:</b> Focused interventions during the Dry Season, addressing the significant decrease in air quality.</li>"
                        "<li><b>Public Health Emphasis:</b> Opportunities to implement health-focused policies and public health campaigns.</li>"
                        "<li><b>User Preferences Guidance:</b> Development of user-centric apps, notification systems, and campaigns based on health priorities.</li>"
                        "</ol>"
                        "</div>", unsafe_allow_html=True)

        # Threats
        with col4:
            st.markdown("<div class='card fade-in' style='background-color: #183D3D;>"
                        "<h2 style='font-size:18px;'>Threats</h2>"
                        "<ol>"
                        "<li><b>Economic Consequences:</b> Economic burden associated with pollution, emphasizing the need for effective pollution control.</li>"
                        "<li><b>Unpredictable AQI Spikes:</b> Constant threat to public health due to unpredictable spikes in AQI values.</li>"
                        "<li><b>Challenges in Information Accessibility:</b> Barriers like a lack of information sources knowledge and limited time can hinder effective communication.</li>"
                        "</ol>"
                        "</div>", unsafe_allow_html=True)
        
            
    with tab3:
        with st.container():
                # Custom CSS styling for a more visually appealing presentation
                custom_style = """
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 0;
                        text-align: left;
                    }

                    #header {
                        background-color: #183D3D;
                        padding: 20px;
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        transition: background-color 0.3s ease;
                        border-radius: 10px;
                    }

                    #header:hover {
                        background-color: #2A5E5A;
                    }

                    .recommendation {
                        margin: 20px;
                        padding: 20px;
                        background-color: #183D3D;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        transition: box-shadow 0.3s ease;
                    }

                    .recommendation:hover {
                        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                    }

                    .fade-in {
                        opacity: 0;
                        animation: fadeIn 1s forwards;
                    }

                    @keyframes fadeIn {
                        from {
                            opacity: 0;
                        }
                        to {
                            opacity: 1;
                        }
                    }

                    .card {
                        padding: 10px;
                        margin: 10px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        transition: box-shadow 0.3s ease;
                        background-color: #232D3F;
                    }

                    .card:hover {
                        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                        transform: scale(1.05);
                    }
                </style>
                """

                # Injecting custom CSS
                st.markdown(custom_style, unsafe_allow_html=True)

                # Header
                st.markdown("<div id='header'>Air Quality Improvement Recommendations</div>", unsafe_allow_html=True)

                # Recommendation 1
                st.markdown("<div class='recommendation fade-in'>"
                            "<h3 style='font-size:18px;'>Recommendation 1: Knowledge Check - Enhancing Awareness and Personalized Information</h3>"
                            "<div class='card'>"
                            "<b>Description:</b> Implementation of the Knowledge Check aims to assess public knowledge regarding air pollution in Jakarta. Upon completing the quiz, users will receive personalized video and article recommendations based on their understanding."
                            "</div>"
                            "<div class='card'>"
                            "<h3 style='font-size:18px;'>Benefits:</h3>"
                            "<ul>"
                            "<li>Increased Awareness: The Knowledge Check will elevate public awareness of air pollution issues by providing information tailored to their knowledge levels.</li>"
                            "<li>Personalized Recommendations: Personalized video and article recommendations ensure users receive content relevant to their understanding.</li>"
                            "<li>Real-time Statistics: Developers can offer real-time statistics to the government for in-depth analysis of public understanding and needs related to air pollution.</li>"
                            "</ul>"
                            "</div>"
                            "<div class='card'>"
                            "<h3 style='font-size:18px;'>Action Plan:</h3>"
                            "<ol>"
                            "<li>Knowledge Check Development: Create an interactive quiz with tailored questions to measure public knowledge.</li>"
                            "<li>Content Recommendation Implementation: Integrate a content recommendation system that provides videos and articles based on Knowledge Check results.</li>"
                            "<li>Real-time Dashboard: Develop a real-time dashboard for developers and the government to monitor statistics on answers, age, gender, and user locations.</li>"
                            "</ol>"
                            "</div>"
                            "</div>", unsafe_allow_html=True)

                # Recommendation 2
                st.markdown("<div class='recommendation fade-in'>"
                            "<h3 style='font-size:18px;'>Recommendation 2: Personal Pollution Tracker - Measuring and Reducing Personal Impact</h3>"
                            "<div class='card'>"
                            "<b>Description:</b> The Personal Pollution Tracker enables users to measure the pollution impact generated from their daily activities. Users can visualize the composition of their impact through a pie chart. For developers, real-time data collected can be used for further analysis and provide valuable information to the government to design programs that are more tailored to individual needs."
                            "</div>"
                            "<div class='card'>"
                            "<h3 style='font-size:18px;'>Benefits:</h3>"
                            "<ul>"
                            "<li>Personalized Awareness: Allows users to see their personal impact, enhancing awareness of individual contributions to air pollution.</li>"
                            "<li>Basis for Policy: Real-time data can offer insights to the government on activities with significant impact, aiding in designing more effective policies.</li>"
                            "<li>Reducing Personal Impact: By understanding their activity's impact, users can take actions to reduce their personal pollution impact.</li>"
                            "</ul>"
                            "</div>"
                            "<div class='card'>"
                            "<h3 style='font-size:18px;'>Action Plan:</h3>"
                            "<ol>"
                            "<li>Personal Pollution Tracker Development: Create an interactive application or platform enabling users to record and view their personal pollution impact.</li>"
                            "<li>Real-time Database: Build a real-time database to store user data, providing direct access to developers and the government.</li>"
                            "</ol>"
                            "</div>"
                            "</div>", unsafe_allow_html=True)
