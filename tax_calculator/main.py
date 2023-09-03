import tax_calculator.constants as c
import tax_calculator.tax_utils as utils

import streamlit as st
import numpy as np


st.title('Tax calculator')
marital = st.selectbox('Martial status:', ['single', 'married'])
state = st.selectbox('Resident state:', ['CA'])
year = st.selectbox('Tax year:', [2023])

# Inputs for the incomes
st.subheader('Incomes ($)')
l, m, r = st.columns(3)
with l:
    income = st.number_input('Your base income:', step=c.AMOUNT_STEP)
    bonus = st.number_input('Your bonuses:', step=c.AMOUNT_STEP)
    rsu = st.number_input('Your RSUs:', step=c.AMOUNT_STEP)
    retirement_401k = st.number_input('Your pre-tax 401k:', step=100, value=utils.cap_401k(year))

with m:
    sp_income = st.number_input('Your spouse income:', step=c.AMOUNT_STEP)
    sp_bonus = st.number_input('Your spouse bonuses:', step=c.AMOUNT_STEP)
    sp_rsu = st.number_input('Your spouse RSUs:', step=c.AMOUNT_STEP)
    sp_retirement_401k = st.number_input('Your spouse pre-tax 401k:', step=100, value=utils.cap_401k(year))

with r:
    other_incomes = st.number_input('other incomes:')
    short_gain = st.number_input('short-term capital gains (loss):', value=0)
    long_gain = st.number_input('long-term capital gains (loss):', value=0)


st.subheader('Dedcutibes ($):')
mortgage_interest = st.number_input('Primary home mortgage interests:')
mortgage_amount = st.number_input('Primary home mortgage principal:')
donations = st.number_input('Donations:', value=3000)
salt = st.number_input('State tax withold + property tax:', value=10000)


st.subheader('Federal Tax')


st.subheader('State Tax')
