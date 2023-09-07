# tax-calculator
A simple tax estimation tool for calculating extra withhold needed for your w-4 file to avoid tax penanlty. It specializes for individuals/married couples with RSU incomes. The tool is written using `steamlit` and currently supports __federal__ and __CA__ tax for __Year 2023__.

## How to install and use 
Please navigate to the target dir and run the following command
```
> git clone git@github.com:wwrechard/tax-calculator.git
> cd tax-calculator
> source script/bootstrap
> streamlit run tax_calculator/main.py
```
It will then start a local service on your mac/pc and pop up the following web page. The service should be accessible by any of your device within the local network

<img width="869" alt="Screen Shot 2023-09-06 at 8 39 56 PM" src="https://github.com/wwrechard/tax-calculator/assets/8441202/b54edecb-d487-4cac-8b7d-d684cc4f047b">

## Disclaimer
Please fill in all the fields to get the final tax estimation. Please do note this tool is designed only for withholding estimation. Please consult your CPA for actual tax return filing. 

Happy taxing!



