import tax_calculator.constants as c
import tax_calculator.tax_utils as utils

import streamlit as st
import numpy as np


st.title('Tax calculator')
st.selectbox('Martial status:', ['single', 'married'], key='martial')
st.selectbox('Resident state:', ['CA'], key='state')
year = st.selectbox('Tax year:', [2023], key='year')

# Inputs for the incomes
st.subheader('Incomes ($)')
l, m, r = st.columns(3)
with l:
    st.number_input('Your base income:', key='income', step=c.AMOUNT_STEP)
    st.number_input('Your bonuses:', key='bonus', step=c.AMOUNT_STEP)
    st.number_input('Your RSUs:', key='rsu', step=c.AMOUNT_STEP)
    st.number_input('Your pre-tax 401k:', key='401k', step=100, value=utils.cap_401k(year))

with m:
    st.number_input('Your spouse income:', key='sp_income', step=c.AMOUNT_STEP)
    st.number_input('Your spouse bonuses:', key='sp_bonus', step=c.AMOUNT_STEP)
    st.number_input('Your spouse RSUs:', key='sp_rsu', step=c.AMOUNT_STEP)
    st.number_input('Your spouse pre-tax 401k:', key='sp_401k', step=100, value=utils.cap_401k(year))

with r:
    st.number_input('other incomes:', key='other_incomes')
    st.number_input('short-term capital gains (loss):', key='short_gain', value=0)
    st.number_input('long-term capital gains (loss):', key='long_gain', value=0)


st.subheader('Dedcutions ($):')
st.number_input('Primary home mortgage interests:', key='mortgage_interest')
st.number_input('Primary home mortgage principal:', key='mortgage_amount')
st.number_input('Donations:', value=3000, key='donations')
st.number_input('State tax withold:', key='state_withold', value=10000)
st.number_input('Property tax:', key='property_tax')
st.number_input('Qualified child dependents:', key='child_dependents')

st.subheader('Tax Witholds')

st.subheader('Regular Tax')
tax = utils.Tax(st.session_state)
output = utils.tax_output(
    total_income=tax.get_total_income(),
    federal_taxable_income=tax.get_federal_taxable_income(),
    state_taxable_income=tax.get_state_taxable_income(),
    federal_tax=tax.get_federal_income_tax(),
    state_tax=tax.get_state_income_tax(),
    fica_tax=tax.get_fica_tax(),
    medicare_tax=tax.get_medicare_tax(),
    sdi_tax=tax.get_state_sdi_tax(),
    child_credit=0)
st.write(output)

