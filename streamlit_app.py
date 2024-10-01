import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="LeetLens", page_icon="🔍")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {content:''; visibility: hidden; display: none;}
            .e1pxoea1 {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df = pd.read_csv('LC_Total_List.csv')

st.sidebar.title("Gear Up for Success with Insights from LeetLens!")
user_menu = st.sidebar.radio(
    'Pick a section',
    ('About','Company-Wise', 'Question-Specific', 'CheatSheet')
)

if user_menu == 'About':
    st.markdown(
        """
        <h1 style='font-family: Arial; color: #4CAF50;'>About LeetLens🔎🔎🔎</h1>
        <p style='font-family: Arial; font-size: 18px;'>
            Welcome to <strong>LeetLens</strong>, your go-to platform for navigating the challenging landscape of technical interviews with <strong>Product-Based Companies</strong>. 
            Our mission is to provide you with the most comprehensive resource for understanding the interview landscape by compiling the <strong>most-asked</strong> questions from various companies.
        </p>
        <p style='font-family: Arial; font-size: 18px;'>
            At LeetLens, we believe that preparation is key to success. That's why we've meticulously curated a database of <strong>1167 unique problems</strong> that have been frequently asked in interviews. Our <strong>detailed analysis</strong> not only helps you identify the trends in questioning but also equips you with the insights necessary to excel in your coding interviews.
        </p>
        <p style='font-family: Arial; font-size: 18px;'>
            Whether you're a seasoned coder or just starting your journey, LeetLens is designed to enhance your preparation. <strong>Share it with your Coding Buddies </strong>to help them ace their interviews too! 
        </p>
        <p style='font-family: Arial; font-size: 18px;'>Dive in, explore the questions, and get ready to impress your future employers ✨✨✨.</p>
        """,
        unsafe_allow_html=True
    )

elif user_menu == 'Company-Wise':
    st.sidebar.header("Company-Wise")
    st.title("Company-Wise Analysis")
    company = helper.company_wise_list(df)
    
    selected_company = st.sidebar.selectbox("Select Company", company)
    st.write("This page shows analysis of questions asked by each company.")
    # Add your visualizations, tables, etc.
    company_ques = helper.fetch_company_ques(df,selected_company);

    difficulty_counts = company_ques['Difficulty'].value_counts()

        # Create a pie chart
    fig = px.pie(
            names=difficulty_counts.index, 
            values=difficulty_counts.values,  
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        # Show the pie chart in Streamlit
    st.write(f"<h3 style='font-size: 30px; color:green'>Distribution of Question Difficulties for {selected_company}</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)
    fig = px.scatter(
            company_ques, 
            x='Appearing Rate (%)', 
            y='Acceptance', 
            labels={"Appearing Rate (%)": "Appearing Rate (%)", "Acceptance": "Acceptance Rate (%)"},
            color='Difficulty',  # Optional: Color by difficulty level
            hover_name='Title',  # Show question title on hover
            size_max=10  # Adjust size of the points
    )
    st.write(f"<h3 style='font-size: 30px; color:green'>Acceptance Rate vs Appearing Rate for {selected_company}</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)
    
    df['Acceptance'] = df['Acceptance'].str.rstrip('%').astype(float)  # Remove '%' and convert to float

# Create a box plot for Acceptance Rate by Difficulty
    company_df = df[df['Company'] == selected_company]

    if not company_df.empty:
        
        # Display the violin plot for acceptance rates by difficulty
        st.write(f"<h3 style='font-size: 30px; color:green'>Acceptance Rates by Difficulty for {selected_company}</h3>", unsafe_allow_html=True)
        
        # Swarm Plot
        plt.figure(figsize=(10, 6))
        sns.swarmplot(x='Difficulty', y='Acceptance', data=company_df)
        plt.title(f'Acceptance Rates for {selected_company} by Difficulty')
        plt.xlabel('Difficulty Level')
        plt.ylabel('Acceptance Rate (%)')
        st.pyplot(plt)

        
        # Show the plot in Streamlit
    
    st.write(f"<h3 style='font-size: 30px; color:green'>List of Questions asked by {selected_company}</h3>", unsafe_allow_html=True)
    company_table = company_ques[['ID','Title','Difficulty','Leetcode Question Link']]
    st.table(company_table)

elif user_menu == 'Question-Specific':
    st.title("Question-Specific Analysis")
    st.sidebar.header("Question-Specific")
    ques = helper.question_wise_list(df)
    
    selected_ques = st.sidebar.selectbox("Search Question", ques)
    st.write("This page provides insights into specific questions.")
    
    filtered_df = df[df['Title'] == selected_ques]

    if not filtered_df.empty:
        # Count occurrences of the specific question
        question_count = filtered_df.shape[0]
        
        # Get details of the question
        acceptance_rate = filtered_df['Acceptance'].iloc[0]  # Assuming it's the same for the question
        average_appearing_rate = filtered_df['Appearing Rate (%)'].mean()   #Avg
        link = filtered_df['Leetcode Question Link'].iloc[0]
        companies = filtered_df['Company'].unique().tolist()  # Unique companies for the question

        # Displaying results in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h2 style='font-size: 24px;color:green;'>Question Title</h2>", unsafe_allow_html=True)
            st.write(f"<h3 style='font-size: 20px;'>{selected_ques}</h3>", unsafe_allow_html=True)

        with col2:
            st.markdown("<h4 style='font-size: 24px;color:green;'>Companies asking it</h4>", unsafe_allow_html=True)
            st.write(f"<h3 style='font-size: 20px;'>{question_count}</h3>", unsafe_allow_html=True)

        with col3:
            st.markdown("<h4 style='font-size: 24px; color:green;'>Acceptance Rate</h4>", unsafe_allow_html=True)
            st.write(f"<h3 style='font-size: 20px;'>{acceptance_rate}%</h3>", unsafe_allow_html=True)

        col1, col2,col3 = st.columns(3)

        with col1:
            st.markdown("<h4 style='font-size: 24px;color:green;'>Avg Appearing Rate (%)</h4>", unsafe_allow_html=True)
            st.write(f"<h3 style='font-size: 20px;'>{average_appearing_rate:.2f}%</h3>", unsafe_allow_html=True)

        with col2:
            st.markdown("<h4 style='font-size: 24px;color:green;'>LeetCode Link</h4>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='font-size: 20px;'><a href='{link}'>{link}</a></h3>", unsafe_allow_html=True)

        # Display companies
        # st.markdown("**Companies that Asked This Question:**")
        st.markdown("<h4 style='font-size: 24px;color:green;'>Companies that Asked This Question</h4>", unsafe_allow_html=True)
        # companies_text = ", ".join(companies)
        # st.markdown(f"<h3 style='font-size: 22px;'>{companies_text}</h3>", unsafe_allow_html=True)
        companies_per_row = 5

# Create rows based on the number of companies
        for i in range(0, len(companies), companies_per_row):
            # Create columns for each company in the current row
            cols = st.columns(companies_per_row)
            
            # Assign each company to a column in the current row
            for j in range(companies_per_row):
                # Check if there is a company to display
                if i + j < len(companies):
                    company = companies[i + j]
                    if cols[j].button(company):
                            pass# st.write(f"You selected {company}.")  # Action taken when the button is clicked
        
        st.write("<h4 style='font-size: 24px;color:green;'>Appearing Rate by Company</h4>",unsafe_allow_html=True)
        fig = px.bar(
                filtered_df,
                x='Company',
                y='Appearing Rate (%)',
                labels={'Appearing Rate (%)': 'Appearing Rate (%)', 'Company': 'Company'},
                text='Appearing Rate (%)'  # Display the appearing rate on the bars
        )
        st.plotly_chart(fig)
        
    else:
        st.write("No data available for the selected question.")

elif user_menu == 'CheatSheet':
    st.title("CheatSheet")
    st.write("This sheet comprises **1,167 unique problems** sourced from LeetCode, designed to help you sharpen your coding skills and prepare for technical interviews.")
    unique_questions_df = df[['ID', 'Title', 'Acceptance', 'Difficulty', 'Leetcode Question Link']].drop_duplicates()
    unique_questions_df = unique_questions_df.sort_values(by='ID')
    # Display unique questions with hyperlinks
    for index, row in unique_questions_df.iterrows():
        # Create a clickable hyperlink
        link = f"[{row['Title']}]({row['Leetcode Question Link']})"
        st.markdown(f"**ID**: {row['ID']}  | **Question**: {link} | **Acceptance**: {row['Acceptance']}%  |  **Difficulty**: {row['Difficulty']} ")
        
