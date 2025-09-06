import tax_calculator.constants as c
import tax_calculator.layout as layout
import tax_calculator.tax_utils as utils

import numpy as np
import streamlit as st


st.title('Tax calculator')

# save and load data
if st.button(
        label=f"Save data",
        on_click=utils.save_session_to_file,
        type='primary',
        kwargs={
            'session': st.session_state,
            'file_name': utils.get_filename(__file__, st.session_state),
        }):
    (f"Successfully saved to "
     f"{utils.get_filename(__file__, st.session_state)}")

uploaded_file = st.file_uploader(label=f"Load data")
if uploaded_file is not None:
    utils.update_session_state(st.session_state, uploaded_file)

st.selectbox('Marital status:', ['single', 'married'], key='marital')
st.selectbox('Resident state:', ['CA'], key='state')
year = st.selectbox('Tax year:', [2023, 2024, 2025], key='year')

# Inputs for the incomes
def set_default_value(field, value):
    if field not in st.session_state:
        st.session_state[field] = value

st.subheader('Incomes ($)')
l, m, r = st.columns(3)
with l:
    st.number_input('Your base income:', key='income', step=c.AMOUNT_STEP)
    st.number_input('Your bonuses:', key='bonus', step=c.AMOUNT_STEP)
    st.number_input('Your RSUs:', key='rsu', step=c.AMOUNT_STEP)
    set_default_value('401k', utils.cap_401k(year))
    st.number_input('Your pre-tax 401k:', key='401k', step=100)
with m:
    st.number_input('Your spouse income:', key='sp_income', step=c.AMOUNT_STEP)
    st.number_input('Your spouse bonuses:', key='sp_bonus', step=c.AMOUNT_STEP)
    st.number_input('Your spouse RSUs:', key='sp_rsu', step=c.AMOUNT_STEP)
    set_default_value('sp_401k', utils.cap_401k(year))
    st.number_input('Your spouse pre-tax 401k:', key='sp_401k', step=100)
with r:
    st.number_input('other incomes:', key='other_incomes')
    set_default_value('short_gain', 0)
    st.number_input('short-term capital gains (loss):', key='short_gain')
    set_default_value('long_gain', 0)
    st.number_input('long-term capital gains (loss):', key='long_gain')

st.subheader('Dedcutions ($):')
st.number_input('Primary home mortgage interests:', key='mortgage_interest')
st.number_input('Primary home mortgage principal:', key='mortgage_amount')
set_default_value('donations', 3000)
st.number_input('Donations:', key='donations')
st.number_input('Property tax:', key='property_tax')
st.number_input('Qualified child dependents (age < 17):', key='child_below_17', step=1)
st.number_input('Qualified child dependents (age >= 17):', key='child_above_17', step=1)

st.subheader('Tax Withholds')
ll, rr = st.columns(2)
with ll:
    st.number_input('Current federal tax withhold:', key='federal_withhold')
    st.number_input('Current state tax withhold:', key='state_withhold')
    set_default_value('federal_rsu_rate', 0.22)
    st.number_input('RSU federal withhold rate:', key='federal_rsu_rate')
    set_default_value('federal_bonus_rate', 0.22)
    st.number_input('Bonus federal withhold rate:', key='federal_bonus_rate')
    st.number_input('Number of remaining paychecks:', key='num_pay', step=1)
    st.number_input('Federal withhold per paycheck:', key='federal_per_pay')
    st.number_input('State withhold per paycheck:', key='state_per_pay')
    st.number_input('Remaining bonus:', key='remain_bonus')
    st.number_input('Remaining RSU:', key='remain_rsu')
with rr:
    st.number_input('Current spouse federal tax withhold:',
                    key='sp_federal_withhold')
    st.number_input('Current spouse state tax withhold:', key='sp_state_withhold')
    set_default_value('sp_federal_rsu_rate', 0.22)
    st.number_input('Spouse federal RSU withhold rate:',
                    key='sp_federal_rsu_rate')
    set_default_value('sp_federal_bonus_rate', 0.22)
    st.number_input('Spouse federal bonus withhold rate:',
                    key='sp_federal_bonus_rate')
    st.number_input('Spouse number of remaining paychecks:', key='sp_num_pay', step=1)
    st.number_input('Spouse federal withhold per paycheck:', key='sp_federal_per_pay')
    st.number_input('Spouse state withhold per paycheck:', key='sp_state_per_pay')
    st.number_input('Spouse remaining bonus:', key='sp_remain_bonus')
    st.number_input('Spouse remaining RSU:', key='sp_remain_rsu')
    
st.subheader('Regular Tax')
withhold = utils.Withhold(st.session_state)
tax = utils.Tax(st.session_state, withhold.get_projected_state_withhold())

lll, rrr = st.columns(2)
with lll:
    st.write(layout.tax_output(
        total_income=tax.get_total_income(),
        federal_taxable_income=tax.get_federal_taxable_income(),
        state_taxable_income=tax.get_state_taxable_income(),
        federal_tax=tax.get_federal_income_tax(),
        state_tax=tax.get_state_income_tax(),
        fica_tax=tax.get_fica_tax(),
        medicare_tax=tax.get_medicare_tax(),
        sdi_tax=tax.get_state_sdi_tax(),
        child_credit=tax.get_child_tax_credit()
    ))
with rrr:
    st.write(layout.withhold_output(
        federal_tax=tax.get_federal_income_tax(),
        state_tax=tax.get_state_income_tax(),
        current_federal_withhold=withhold.get_current_federal_withhold(),
        current_state_withhold=withhold.get_current_state_withhold(),
        projected_federal_withhold=withhold.get_projected_federal_withhold(),
        projected_state_withhold=withhold.get_projected_state_withhold()
    ))
