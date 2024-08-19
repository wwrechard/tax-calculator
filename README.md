# tax-calculator
A simple tax estimation tool for calculating extra withhold needed for your w-4 file to avoid tax penanlty. It specializes for individuals/married couples with RSU incomes. The tool is written using `steamlit` and currently supports __federal__ and __CA__ tax for __Year 2023__ and __Year 2024__.

The software now allows you to save session data to local csv files and load them in the future to continue the tax planning.

## How to install and use 
Please navigate to the target dir and run the following command
```
> git clone git@github.com:wwrechard/tax-calculator.git
> cd tax-calculator
> source script/bootstrap
> streamlit run tax_calculator/main.py
```
It will then start a local service on your mac/pc and pop up the following web page. The service should be accessible by any of your device within the local network

<img width="980" alt="Screenshot 2024-08-19 at 12 28 50 AM" src="https://github.com/user-attachments/assets/9cacd0f8-d52f-4242-b126-ab162ea90744">


## Disclaimer
Please fill in all the necessary fields to get the final tax estimation. There are a few prefilled fields that coded with some common rates (e.g., 22% federal withhold rate for RSU and bonus), please feel free to override. Note that this tool is designed only for withholding estimation purposes. Please consult your CPA for actual tax return filing. 

Happy taxing!



