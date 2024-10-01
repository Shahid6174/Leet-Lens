import numpy as np

def company_wise_list(df):
    # Ensure the column name matches your DataFrame
    company = df['Company'].unique().tolist()  # Use 'Companies' if that's the correct name
    company.sort()  # Sort the list of companies
    return company

def question_wise_list(df):
    # Ensure the column name matches your DataFrame
    question = df['Title'].unique().tolist()  # Use 'Companies' if that's the correct name
    question.sort()  # Sort the list of companies
    
    return question

def fetch_company_ques(df,selected_company):
    company_questions = df[df['Company'] == selected_company]
    return company_questions