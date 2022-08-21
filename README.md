# anomaly-detection-web-app


A web app is built to detect anomalies in a set of grant application. 

Criteria:

The anomalies that are detected; 

whether the name of applicant appears several times in the datasheet or

whether the name of the company appears several times in the datasheet or

whether the bank account number of the company appears several times in the datasheet or

whether more than 100,000 euros was requested or

whether the Chamber of Commerce number is present in the anomaly registry

Input data:

The data (example_input_data.xlsx) is encrypted with Python hash codes. A fake anomaly registry (example_register_data.xlsx) contains applicant information that have abused the grant in the past.

Python code: 

The code is written in Python with Dash plotly. I used following file to start:

https://github.com/RaThorat/proposal_info_Elsevier_Expert_Lookup_02/blob/main/Dashapp_Proposals_info_for_Expert_Lookup.py

I followed instruction videos from charming data for style, bootstrap, decorators etc.:

https://www.youtube.com/watch?v=0mfIK8zxUds&t=13s

https://www.youtube.com/watch?v=vqVwpL4bGKY&list=RDCMUCqBFsuAz41sqWcFjZkqmJqQ&index=4

https://www.youtube.com/watch?v=mTsZL-VmRVE&list=RDCMUCqBFsuAz41sqWcFjZkqmJqQ&index=5

Deployment: 

I tried first with Azure to deploy the web app, however I could not. The problem was the connection between github repository and the azure. After lot of trial I gave up on Azure. I switched to pythonanywhere.com for deploying the web-app on following instruction video from charming data:

https://www.youtube.com/watch?v=WOWVat5BgM4

I highly recommend this video.

Using intructions:

You can either open the code in you IDE, run it and visit http://127.0.0.1:8050/ in your web browser or

visit the webapp on the website rathorat.pythonanywhere.com
 
Once in the web browser, you will see the possibility to upload Excel example_input_data.xlsx. As soon as you upload the excel sheet, the analysis starts. On the screen you can see an output file with the reference numbers that meet the criteria. You will also see a number of summary graphs.
You can download the output file by clicking the 'Export' button.
