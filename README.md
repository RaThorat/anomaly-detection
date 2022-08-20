# anomaly-detection

The web app is built to detect anomalies in a set of data. 

Input data: The data is encrypted with Python hash codes. The data is temporarily uploaded to the web app. A fake anomaly registry used as an example. This register contains data about companies (chamber of commerce number) that have abused the subsidy in the past.

The criteria have been proposed as; 

whether the applicant information (name of lead party/legal person) appears several times in the dataheet or

whether the applicant's financial data (bank account number) appears several times in the dataheet or

whether more than 100,000 euros was requested when applying or 

whether the Chamber of Commerce number is present in fake anomaly registry

Applications is made in Python with Dash plotly.

Instructions for use: In an integrated development environment (IDE): Open the code in VS code and run the main .py file Visit http://127.0.0.1:8050/ in your web browser.

On the website Dash (xxxxx.pythonanywhere.com) : On the website you see the possibility to upload Excel (given here as an example). As soon as you add your Excel sheet, the analysis starts. On the screen you can see an output file with the identification numbers that meet the criteria. 

You will also see a number of summary graphs.

You can download this output file by clicking the 'Export' button.
