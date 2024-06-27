import streamlit as sl
import plotly.graph_objects as go
from datetime import datetime
import calendar


incomes = ['Salary','Another Source']
expenses = ['Rent','Food','Transportation','Insurance','Others','Saving']

currency = 'EUR'
page_title = 'Income and Expenses Tracker'
page_icon = ':money_with_wings:'
layout = 'centered'


sl.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
sl.title(page_title)

years = [datetime.today().year, datetime.today().year - 1, datetime.today().year - 2]
months = list(calendar.month_name[1:])


sl.header(f"Data Entry in {currency}")
with sl.form('entry_form', clear_on_submit=True):
    col1, col2 = sl.columns(2)
    col1.selectbox('Month: ', months, key='month')
    col1.selectbox('Year: ', years, key='year')

    '---'

    with sl.expander('Income'):
        for i in incomes:
            sl.number_input(f"{i}:", min_value=0, format='%i', step=50, key=i)
    with sl.expander('Expenses'):
        for j in expenses:
            sl.number_input(f"{j}:", min_value=0, format='%i', step=50, key=j)
    with sl.expander('Comments'):
        comment = sl.text_area('',placeholder='Add your comment here')

    '---'

    submitted = sl.form_submit_button('Save')
    if submitted:
        period = str(sl.session_state['year']) + '-' + str(sl.session_state('month'))
