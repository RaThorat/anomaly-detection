# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
from numpy import NaN
os.getcwd()
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# to check if we have to display figures yet
loaded_a_file = False

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Anomaly Dashboard",
                    className='text-center text-primary mb-4'),

        ],  # width={'size':4, 'offset':0, 'order':1},
            xs=12, sm=12, md=12, lg=4, xl=4
        ),
        dbc.Col([
            html.P("Check you input data by uploading here:",
                   style={"textDecoration": "underline"}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True),
        ],
            xs=12, sm=12, md=12, lg=4, xl=4
        ),
    ], justify='center'),  # Horizontal:start,center,end,between,around
    dbc.Row([
        dbc.Col([
            html.P("Most applicants",
                   style={"textDecoration": "underline"}),
            dcc.Graph(id='output-data-graph'),
        ],  # width={'size':4, 'offset':0, 'order':3},
            xs=12, sm=12, md=12, lg=4, xl=4
        ),
        dbc.Col([
            html.P("Largest applicants",
                   style={"textDecoration": "underline"}),
            dcc.Graph(id='output-data-graph2'),
        ],  # width={'size':4, 'offset':0, 'order':3},
            xs=12, sm=12, md=12, lg=4, xl=4
        ),
        dbc.Col([
            html.P("Top 5 match in register data",
                   style={"textDecoration": "underline"}),
            dcc.Graph(id='output-data-graph3'),
        ],  # width={'size':4, 'offset':0, 'order':3},
            xs=12, sm=12, md=12, lg=4, xl=4
        ),
    ], justify='start'),
    dbc.Row(
        dbc.Col(
            html.Div(id='output-data-upload'),
            width=12)
    ),

], fluid=True)


#function removes empty rows for better readability
def remove_emptyrows(dataframe):
    row_list = dataframe.index.values
    empty_rows = []

    for row in dataframe.index:
        row_as_list = dataframe.iloc[row, 1:].values.flatten().tolist()
        row_as_list = list(filter(None, row_as_list))

        if len(row_as_list) == 0:
            empty_rows.append(row)

    # Delete Rows by Index numbers
    dataframe = dataframe.drop(dataframe.index[(empty_rows)])

    return dataframe


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

        global loaded_a_file
        loaded_a_file = True

        
        #Obsolete code to change the path below:
        # It is not needed anymore because of gloabl variable loaded_a_file
        # The path is changed to local URL because external URL was giving errors
        # But it is given here for additional information. 
        # RT: path to .xlsx added so that the file can be found from a folder in the web app
        #THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        #my_file = os.path.join(THIS_FOLDER, 'nep_MenO_data.xlsx')
        #df_register = pd.read_excel(my_file)
        
        
        df_register = pd.read_excel("Example_register_data.xlsx")
        df['Grant_requested'] = df['Grant_requested'].astype(str)
        df['Grant_requested'] = df['Grant_requested'].str.replace('.', '').str.replace(',', '.').str.replace('€','').astype('float')
        df['Company repeated in'] = None
        df['CoC_number repeated in'] = None
        df['More than 100,000 euros requested?'] = None
        df['IBAN_number repeated in'] = None
        df['Applicant repeated in'] = None
        #new column with CoC_number in register named in register
        df['CoC_number in register named'] = None

        l = len(df.index)
        register_l = len(df_register.index) #added meno

        for j in range(0,l):
            penv=df['Applicant'][j]
            ref=[]
            for k in range(0,l):
                if k!=j:
                    if penv==df['Applicant'][k]:
                        ref.append(df['Reference'][k])
            df['Applicant repeated in'][j]='\n'.join(ref)

        for j in range(0,l):
            penv=df['Company'][j]
            ref=[]
            for k in range(0,l):
                if k!=j:
                    if penv==df['Company'][k]:
                        ref.append(df['Reference'][k])
            df['Company repeated in'][j]='\n'.join(ref)

        for j in range(0,l):
            penv=df['CoC_number'][j]
            ref=[]
            for k in range(0,l):
                if k!=j:
                    if penv==df['CoC_number'][k]:
                        ref.append(df['Reference'][k])
            df['CoC_number repeated in'][j]='\n'.join(ref)

            # check if CoC_number is also in register
            for m in range(0, register_l):
                register_coc = df_register['CoC_number'][m]
                # CoC_number of input data is in register?
                if register_coc == penv:
                    ref.append(df['Reference'][k])
                    df['CoC_number in register named'][j] = '\n'.join(ref)

        for j in range(0,l):
            penv=df['IBAN_number'][j]
            ref=[]
            for k in range(0,l):
                if k!=j:
                    if penv==df['IBAN_number'][k]:
                        ref.append(df['Reference'][k])
            df['IBAN_number repeated in'][j]='\n'.join(ref)

        for j in range(0,l):
            if df['Grant_requested'][j] > 100000:
                df['More than 100,000 euros requested?'][j]='Yes'
            else:
                #Otherwise ugly nan value, leave it empty for better cleanup
                df['More than 100,000 euros requested?'][j] = None




        #added CoC_number in register
        df = df.reindex(columns=['Reference','Company repeated in', 'CoC_number repeated in', 'More than 100,000 euros requested?','IBAN_number repeated in', 'Applicant repeated in', 'CoC_number in register named'])

        # Loop to remove rows with no values
        df = remove_emptyrows(df)
        global globaldf
        globaldf = df

        #rslt_df = df[(df['Applicant'].str.contains('ABCD'))]
            #& (df['More than 100,000 euros requested?'] ==NaN)
            #& (df['IBAN_number repeated in'] ==NaN)
            #& (df['CoC_number repeated in']==NaN)
            #& (df['Applicant repeated in']==NaN)
            #& (df['Company repeated in'] ==NaN)]

        rslt_df= df[df.apply(lambda x: any(x.str.contains('ABCD')),axis=1)]



    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=rslt_df.to_dict('records'),
            export_format='xlsx',
            columns=[{'name': i, 'id': i} for i in rslt_df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:2] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# should be linked now to output of upload form
@app.callback(
    Output('output-data-graph', 'figure'),
    Input('output-data-upload', 'children'))
def output_graph(graphs):
    if loaded_a_file == True:
        dff = globaldf
        # drops the weird empty fields that are not NaN or None and can't be removed by dropna()..
        dfff = dff[dff['Company repeated in'].astype(str).str.startswith('ABCD')]
        # lists only top 15
        # dfff = pd.Categorical(dfff['Company repeated in'])
        dfff = dfff.groupby(['Company repeated in']).size().to_frame().sort_values([0],ascending=False).head(5).reset_index()
        # change to go.figure() and use layout with tickertype to only display whole numbers
        fig = px.histogram(dfff, x='Company repeated in', title='Top 5 repeated applicants', nbins=1)
        return fig
    else:
        # empty figure with nothing in it
        fig = go.Figure(go.Scatter(x=[], y=[]))
        fig.update_layout(template=None)
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        return fig


# should be linked now to output of upload form
@app.callback(
    Output('output-data-graph2', 'figure'),
    Input('output-data-upload', 'children'))
def output_graph2(graphs):
    if loaded_a_file == True:
        dff = globaldf
        dfff = dff
        dfff["More than 100,000 euros requested?"].fillna("No", inplace=True)
        fig = px.pie(dfff, names='More than 100,000 euros requested?', title='More than 100,000 euros requested?',
                     hole=.1)
        # subplot code but incomplete -> subplot with df['Grant_requested'] hoogte
        ##label = dfff["More than 100,000 euros requested?"].value_counts().index
        ##value = dfff["More than 100,000 euros requested?"].value_counts().values
        ##trace = go.Pie(labels=label, values=value)
        ##data = [trace]
        ##fig = make_subplots(rows=2, cols=1)
        ##fig.add_trace(
        ##    go.Figure(data=data),
        ##    row=1, col=1)
        ##fig.add_trace(
        ##    go.Figure(data=data),
        ##    row=2, col=1)
        return fig
    else:
        # empty figure with nothing in it
        fig = go.Figure(go.Scatter(x=[], y=[]))
        fig.update_layout(template=None)
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        return fig


# should be linked now to output of upload form
@app.callback(
    Output('output-data-graph3', 'figure'),
    Input('output-data-upload', 'children'))
def output_graph3(graphs):
    if loaded_a_file == True:
        dff = globaldf
        # drops the weird empty fields that are not NaN or None and can't be removed by dropna()..
        # dfff2 = dff[dff['CoC_number in register named'].astype(str).str.startswith('ABCD')]
        #dfff2 = dff['CoC_number in register named']
        fig = go.Figure(go.Scatter(x=[], y = []))
        return fig
    else:
        # empty figure with nothing in it
        fig = go.Figure(go.Scatter(x=[], y=[]))
        fig.update_layout(template=None)
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
