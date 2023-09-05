cap_401k_table = {
    2023: 22500,
}

deduction_table = {
    ('federal', 'single', 2023): 13850,
    ('federal', 'married', 2023): 27700,
    ('CA', 'single', 2023): 5202,
    ('CA', 'married', 2023): 10404,
}

tax_bracket_table = {
    ('federal', 'single', 2023): (
        [0, 11000, 44725, 95375, 182100, 231250, 578125],
        [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]),
    ('federal', 'married', 2023): (
        [0, 22000, 89450, 190750, 364200, 462500, 693750],
        [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]),
    ('CA', 'single', 2023): (
        [0, 10099, 23942, 37788, 52455, 66295, 338639, 406364, 677275],
        [0.01, 0.02, 0.04, 0.06, 0.08, 0.093, 0.103, 0.113, 0.123]),
    ('CA', 'married', 2023): (
        [0, 20198, 47884, 75576, 104910, 132590, 677278, 812728, 1354550],
        [0.01, 0.02, 0.04, 0.06, 0.08, 0.093, 0.103, 0.113, 0.123]),
}

long_term_capital_gain_tax_rate_table = {
    ('single', 2023): ([0, 44625, 492300], [0.0, 0.15, 0.2]),
    ('married', 2023): ([0, 89250, 553850], [0.0, 0.15, 0.2]),
}

state_deduction_adjustment_table = {
    ('CA', 'single', 2023): 229908,
    ('CA', 'married', 2023): 459821,
}

fica_table = {
    2023: [160200, 0.062]
}

state_sdi_table = {
    ('CA', 2023): [153164, 0.009]
}

def cap_401k(year):
    return cap_401k_table[year]

def standard_deduction(type, martial, year):
    key = (type, martial, year)
    return deduction_table[key]

def qualified_mortgage(interest, principal):
    if principal <= 750000:
        return interest
    else:
        return interest * 750000 / principal

def tax_bracket(type, martial, year):
    key = (type, martial, year)
    return tax_bracket_table[key]

def calculate_tax(income, brackets, rates):
    result = income * rates[0]
    for i in range(1, len(brackets)):
        bracket = brackets[i]
        rate = rates[i]

        if income <= bracket:
            break
        result += abs(income - bracket) * (rates[i] - rates[i - 1])
    return result
        
def long_term_capital_gain_tax_rate(taxable_income, martial, year):
    key = (martial, year)
    bracket, rate = long_term_capital_gain_tax_rate_table[key]
    for i in range(len(bracket)):
        idx = len(bracket) - i - 1
        if taxable_income > bracket[i]:
            return rate[i]
    return 0.0

def get_additional_medicare_tax_threshold(martial):
    if martial == 'single':
        return 200000
    elif martial == 'married':
        return 250000

def tax_output(total_income, federal_taxable_income, state_taxable_income, federal_tax, state_tax, fica_tax, medicare_tax, sdi_tax, child_credit):
    total_tax = federal_tax + fica_tax + medicare_tax + state_tax + sdi_tax
    take_home = total_income - total_tax

    intf = lambda x: format(x, '.2f')
    ratio = lambda x, y: 0 if y == 0 else format(float(x / y * 100), '.2f')

    federal_tax_rate = ratio(federal_tax, federal_taxable_income)
    fica_rate = ratio(fica_tax, federal_taxable_income)
    medicare_rate = ratio(medicare_tax, federal_taxable_income)
    state_tax_rate = ratio(state_tax, state_taxable_income)
    sdi_rate = ratio(sdi_tax, state_taxable_income)
    total_tax_rate = ratio(total_tax, total_income)
    take_home_rate = ratio(take_home, total_income)

    return f'''
    |                                 |                         |                           |
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


class Tax:
    def __init__(self, session):
        self._year = session['year']
        self._martial = session['martial']
        self._state = session['state']
    
        self._income = session['income']
        self._bonus = session['bonus']
        self._rsu = session['rsu']
        self._401k = session['401k']
        self._sp_income = session['sp_income']
        self._sp_bonus = session['sp_bonus']
        self._sp_rsu = session['sp_rsu']
        self._sp_401k = session['sp_401k']
        self._other_incomes = session['other_incomes']
        self._short_gain = session['short_gain']
        self._long_gain = session['long_gain']
        self._mortgage_interest = session['mortgage_interest']
        self._mortgage_amount = session['mortgage_amount']
        self._donations = session['donations']
        self._state_withold = session['state_withold']
        self._property_tax = session['property_tax']
        self._child_dependents = session['child_dependents']

        self._salt = min(self._state_withold + self._property_tax, 10000)


    def capital_gain(self):
        net_gain = self._short_gain + self._long_gain
        if net_gain < 0:
            return max(-3000, net_gain)
        else:
            return net_gain
        
    def get_wages(self):
        return self._income + self._bonus + self._rsu

    def get_spouse_wages(self):
        return self._sp_income + self._sp_bonus + self._sp_rsu

    def get_total_income(self):
        return max(0, self.get_wages() + self.get_spouse_wages() + self._other_incomes + self.capital_gain() - self._401k - self._sp_401k)

    def get_federal_deduction(self):
        standard = standard_deduction('federal', self._martial, self._year)
        mortgage = qualified_mortgage(self._mortgage_interest, self._mortgage_amount)
        itemized_deduction = self._salt + mortgage + self._donations

        return max(standard, itemized_deduction)

    def get_federal_taxable_income(self):
        return max(0, self.get_total_income() - self.get_federal_deduction())

    def get_federal_income_tax(self):
        brackets, rates = tax_bracket('federal', self._martial, self._year)
        taxable_income = self.get_federal_taxable_income()
        if self.capital_gain() <= 0 or self._long_gain <= 0:
            result = calculate_tax(taxable_income, brackets, rates)
        else:
            result = calculate_tax(taxable_income - self._long_gain, brackets, rates)
            long_tax_rate = long_term_capital_gain_tax_rate(taxable_income, self._martial, self._year)
            result += self._long_gain * long_tax_rate
        return result

    def get_fica_tax(self):
        key = self._year
        cap, rate = fica_table[key]
        return rate * (min(self.get_wages(), cap) + min(self.get_spouse_wages(), cap))

    def get_medicare_tax(self):
        threshold = get_additional_medicare_tax_threshold(self._martial)
        total_wages = self.get_wages() + self.get_spouse_wages()
        return 0.0145 * total_wages + 0.009 * max(0, total_wages - threshold)

    def get_state_deduction(self):
        standard = standard_deduction(self._state, self._martial, self._year)
        
        itemized_deduction = self._property_tax + self._mortgage_interest + self._donations
        threshold = state_deduction_adjustment_table[(self._state, self._martial, self._year)]
        federal_agi = self.get_total_income()
        if federal_agi > threshold:
            line4 = itemized_deduction * 0.8
            line8 = (federal_agi - threshold) * 0.06
            line9 = min(line4, line8)
            itemized_deduction -= line9
        return max(standard, itemized_deduction)

    def get_state_taxable_income(self):
        return max(0, self.get_total_income() - self.get_state_deduction())

    def get_state_income_tax(self):
        brackets, rates = tax_bracket(self._state, self._martial, self._year)
        taxable_income = self.get_state_taxable_income()
        result = calculate_tax(taxable_income, brackets, rates)
        return result
        
    def get_state_sdi_tax(self):
        key = (self._state, self._year)
        cap, rate = state_sdi_table[key]
        return rate * (min(self.get_wages(), cap) + min(self.get_spouse_wages(), cap))
        
