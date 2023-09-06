def intf(x):
    return format(x, '.2f')

def ratio(x, y):
    return 0 if y == 0 else format(float(x / y * 100), '.2f')

def tax_output(total_income, federal_taxable_income, state_taxable_income, federal_tax, state_tax, fica_tax, medicare_tax, sdi_tax, child_credit):
    total_tax = federal_tax + fica_tax + medicare_tax + state_tax + sdi_tax
    take_home = total_income - total_tax

    federal_tax_rate = ratio(federal_tax, federal_taxable_income)
    fica_rate = ratio(fica_tax, federal_taxable_income)
    medicare_rate = ratio(medicare_tax, federal_taxable_income)
    state_tax_rate = ratio(state_tax, state_taxable_income)
    sdi_rate = ratio(sdi_tax, state_taxable_income)
    total_tax_rate = ratio(total_tax, total_income)
    take_home_rate = ratio(take_home, total_income)

    return f'''
    |Item                             | Amount                  | Ratio                     |
    |---------------------------------|-------------------------|---------------------------|
    |Total income                     | ${intf(total_income)}   |                           |
    |Federal taxable income           | ${intf(federal_taxable_income)} |                   |
    |State taxable income             | ${intf(state_taxable_income)}|                      |
    |Federal tax                      | ${intf(federal_tax)}    | {federal_tax_rate}%  |
    |State tax                        | ${intf(state_tax)}      | {state_tax_rate}%    |
    |social security tax              | ${intf(fica_tax)}       | {fica_rate}%         |
    |Medicare                         | ${intf(medicare_tax)}   | {medicare_rate}%     |
    |SUI/SDI                          | ${intf(sdi_tax)}        | {sdi_rate}%          |
    |Child care credit                | ${intf(child_credit)}   |                      |
    | __Total tax w/o AMT__           | ${intf(total_tax)}      | {total_tax_rate}% |
    | __Take home__                   | ${intf(take_home)}      | {take_home_rate}% |
    '''

def withhold_output(federal_tax, state_tax, current_federal_withhold, current_state_withhold, projected_federal_withhold, projected_state_withhold):
    federal_tax_owe = federal_tax - projected_federal_withhold
    state_tax_owe = state_tax - projected_state_withhold

    federal_withhold_rate = ratio(projected_federal_withhold, federal_tax)
    state_withhold_rate = ratio(projected_state_withhold, state_tax)

    return f'''
    |Item                      | Amount                  | Ratio                     |
    |--------------------------|-------------------------|---------------------------|
    |Current federal withhold  | ${intf(current_federal_withhold)}   |               |
    |Current state withhold    | ${intf(current_state_withhold)} |                   |
    |Projected_federal_withhold| ${intf(projected_federal_withhold)}|{federal_withhold_rate}%|
    |Projected_state_withhold  | ${intf(projected_state_withhold)}  |{state_withhold_rate}%  |
    |__Federal tax you owe__   | ${intf(federal_tax_owe)}|                           |
    |__State tax you owe__     | ${intf(state_tax_owe)}  |                           |
    '''
