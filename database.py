import streamlit as st
from deta import Deta 


DETA_KEY = st.secrets["DETA_KEY"]

deta = Deta(DETA_KEY)

db = deta.Base("monthly_reports")


def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)
