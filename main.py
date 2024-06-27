import streamlit as sl
import plotly.graph_objects as go
from datetime import datetime
import calendar
from streamlit_option_menu import option_menu
import database as db


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

def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
sl.markdown(hide_st_style, unsafe_allow_html=True)

selected = option_menu(
    menu_title = None,
    options = ['Data Entry', 'Visualization'],
    icons = ['pencil-fill', 'bar-chart-fill'],
    orientation = 'horizontal'
)

if selected == 'Data Entry':
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
            period = str(sl.session_state['year']) + '-' + str(sl.session_state['month'])
            incomes = {income: sl.session_state[income] for income in incomes}
            expenses = {expense: sl.session_state[expense] for expense in expenses}
            db.insert_period(period, incomes, expenses, comment)
            sl.success("It's Saved")

else:
    sl.header('Visualization')
    with sl.form('saved_periods'):
        period = sl.selectbox('Period', get_all_periods())
        submitted = sl.form_submit_button('Plot Period')
        if submitted:
            period_data = db.get_period(period)
            comment = period_data('comment')
            expenses = period_data('expenses')
            income = period_data('income')

            total_income = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remaining = total_income - total_expenses
            col1, col2, col3 = sl.columns(3)
            col1.metric('Total Income', f"{total_income}{currency}")
            col1.metric('Total Expenses', f"{total_expenses}{currency}")
            col1.metric('Remaining', f"{remaining}{currency}")
            sl.text(f"Comment: {comment}")

            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())


            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="grey")
            data = go.Sankey(link=link, node=node)


            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            sl.plotly_chart(fig, use_container_width=True)




