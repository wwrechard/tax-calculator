from math import ceil
import tax_calculator.tables as t

def cap_401k(year):
    return t.cap_401k_table[year]

def standard_deduction(type, marital, year):
    key = (type, marital, year)
    return t.deduction_table[key]

def qualified_mortgage(interest, principal):
    if principal <= 750000:
        return interest
    else:
        return interest * 750000 / principal

def tax_bracket(type, marital, year):
    key = (type, marital, year)
    return t.tax_bracket_table[key]

def calculate_tax(income, brackets, rates):
    result = income * rates[0]
    for i in range(1, len(brackets)):
        bracket = brackets[i]
        rate = rates[i]

        if income <= bracket:
            break
        result += abs(income - bracket) * (rates[i] - rates[i - 1])
    return result
        
def long_term_capital_gain_tax_rate(taxable_income, marital, year):
    key = (marital, year)
    bracket, rate = t.long_term_capital_gain_tax_rate_table[key]
    for i in range(len(bracket)):
        idx = len(bracket) - i - 1
        if taxable_income > bracket[i]:
            return rate[i]
    return 0.0

def get_additional_medicare_tax_threshold(marital):
    if marital == 'single':
        return 200000
    elif marital == 'married':
        return 250000

def rount_up_to(num, unit):
    return ceil(num / unit) * unit

class Tax:
    def __init__(self, session, projected_state_withhold):
        self._year = session['year']
        self._marital = session['marital']
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
        self._property_tax = session['property_tax']
        self._child_below_17 = session['child_below_17']
        self._child_above_17 = session['child_above_17']

        self._salt = min(projected_state_withhold + self._property_tax, 10000) 

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

    def get_child_tax_credit(self):
        credit = self._child_below_17 * 2000 + self._child_above_17 * 500
        threshold = 400000 if self._marital == 'married' else 200000
        credit -= rount_up_to(max(0, self.get_total_income() - threshold), 1000) * 0.05
        return max(0, credit)

    def get_federal_deduction(self):
        standard = standard_deduction('federal', self._marital, self._year)
        mortgage = qualified_mortgage(self._mortgage_interest, self._mortgage_amount)
        itemized_deduction = self._salt + mortgage + self._donations

        return max(standard, itemized_deduction)

    def get_federal_taxable_income(self):
        return max(0, self.get_total_income() - self.get_federal_deduction())

    def get_federal_income_tax(self):
        brackets, rates = tax_bracket('federal', self._marital, self._year)
        taxable_income = self.get_federal_taxable_income()
        if self.capital_gain() <= 0 or self._long_gain <= 0:
            result = calculate_tax(taxable_income, brackets, rates)
        else:
            result = calculate_tax(taxable_income - self._long_gain, brackets, rates)
            long_tax_rate = long_term_capital_gain_tax_rate(taxable_income, self._marital, self._year)
            result += self._long_gain * long_tax_rate
        result -= self.get_child_tax_credit()
        return result

    def get_fica_tax(self):
        key = self._year
        cap, rate = t.fica_table[key]
        return rate * (min(self.get_wages(), cap) + min(self.get_spouse_wages(), cap))

    def get_medicare_tax(self):
        threshold = get_additional_medicare_tax_threshold(self._marital)
        total_wages = self.get_wages() + self.get_spouse_wages()
        return 0.0145 * total_wages + 0.009 * max(0, total_wages - threshold)

    def get_state_deduction(self):
        standard = standard_deduction(self._state, self._marital, self._year)
        
        itemized_deduction = self._property_tax + self._mortgage_interest + self._donations
        threshold = t.state_deduction_adjustment_table[(
            self._state, self._marital, self._year)]
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
        brackets, rates = tax_bracket(self._state, self._marital, self._year)
        taxable_income = self.get_state_taxable_income()
        result = calculate_tax(taxable_income, brackets, rates)
        return result
        
    def get_state_sdi_tax(self):
        key = (self._state, self._year)
        cap, rate = t.state_sdi_table[key]
        return rate * (min(self.get_wages(), cap) + min(self.get_spouse_wages(), cap))
        

class Withhold:
    def __init__(self, session):
        self._marital = session['marital']
        self._state = session['state']
        self._year = session['year']

        self._federal_withhold = session['federal_withhold']
        self._state_withhold = session['state_withhold']
        self._federal_rsu_rate = session['federal_rsu_rate']
        self._federal_bonus_rate = session['federal_bonus_rate']
        self._state_rsu_rate = t.state_rsu_withhold_table[(self._state, self._year)]
        self._state_bonus_rate = t.state_bonus_withhold_table[(self._state, self._year)]
        self._num_pay = session['num_pay']
        self._federal_per_pay = session['federal_per_pay']
        self._state_per_pay = session['state_per_pay']
        self._remain_bonus = session['remain_bonus']
        self._remain_rsu = session['remain_rsu']
        self._rsu = session['rsu']
        
        self._sp_federal_withhold = session['sp_federal_withhold']
        self._sp_state_withhold = session['sp_state_withhold']
        self._sp_federal_rsu_rate = session['sp_federal_rsu_rate']
        self._sp_federal_bonus_rate = session['sp_federal_bonus_rate']
        self._sp_state_rsu_rate = t.state_rsu_withhold_table[(self._state, self._year)]
        self._sp_state_bonus_rate = t.state_bonus_withhold_table[(self._state, self._year)]
        self._sp_num_pay = session['sp_num_pay']
        self._sp_federal_per_pay = session['sp_federal_per_pay']
        self._sp_state_per_pay = session['sp_state_per_pay']
        self._sp_remain_bonus = session['sp_remain_bonus']
        self._sp_remain_rsu = session['sp_remain_rsu']
        self._sp_rsu = session['sp_rsu']

    def get_current_federal_withhold(self):
        return self._federal_withhold + self._sp_federal_withhold

    def get_current_state_withhold(self):
        return self._state_withhold + self._sp_state_withhold

    def get_projected_federal_pay_withhold(self):
        projected_withhold = (self._num_pay * self._federal_per_pay +
                              self._sp_num_pay * self._sp_federal_per_pay +
                              self._remain_bonus * self._federal_bonus_rate +
                              self._sp_remain_bonus * self._sp_federal_bonus_rate)
        return projected_withhold

    def get_projected_federal_rsu_withhold(self):
        projected_withhold = (self._remain_rsu * self._federal_rsu_rate +
                              self._sp_remain_rsu * self._sp_federal_rsu_rate)
        return projected_withhold

    def get_projected_federal_withhold(self):
        return (self.get_current_federal_withhold() +
                self.get_projected_federal_pay_withhold() +
                self.get_projected_federal_rsu_withhold())
        
    def get_projected_state_pay_withhold(self):
        projected_withhold = (self._num_pay * self._state_per_pay +
                              self._sp_num_pay * self._sp_state_per_pay +
                              self._remain_bonus * self._state_bonus_rate +
                              self._sp_remain_bonus * self._sp_state_bonus_rate)
        return projected_withhold

    def get_projected_state_rsu_withhold(self):
        projected_withhold = (self._remain_rsu * self._state_rsu_rate +
                              self._sp_remain_rsu * self._sp_state_rsu_rate)
        return projected_withhold

    def get_projected_state_withhold(self):
        return (self.get_current_state_withhold() +
                self.get_projected_state_pay_withhold() +
                self.get_projected_state_rsu_withhold())
