# anomaly-detection

The web app is built to detect anomalies in a set of data. 

Input data: The data (example_input_data.xlsx) is encrypted with Python hash codes. A fake anomaly registry (example_register_data.xlsx) contains data that have abused the subsidy in the past.

The anomalies that are detected; 

whether the applicant information (name of lead party/legal person) appears several times in the datasheet or

whether the applicant's financial data (bank account number) appears several times in the datasheet or

whether more than 100,000 euros was requested when applying or 

whether the Chamber of Commerce number is present in fake anomaly registry


Applications is made in Python with Dash plotly.

Instructions for use: In an integrated development environment (IDE): Open the code in VS code and run the main .py file Visit http://127.0.0.1:8050/ in your web browser.

On the website Dash (xxxxx.pythonanywhere.com) : On the website you see the possibility to upload Excel example_input_data.xlsx). As soon as you add your Excel sheet, the analysis starts. On the screen you can see an output file with the reference numbers that meet the criteria. 

You will also see a number of summary graphs.

You can download this output file by clicking the 'Export' button.
