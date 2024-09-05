import plotly.express as px
import plotly.graph_objects as go
import dash_table
import pandas as pd
from dash import Dash,dcc,html,Input,Output

data=pd.read_csv('INX_Future_Inc_Employee_Performance_CDS_Project2_Data_V1.8 (1) (2).csv')
# Select only the numeric columns for correlation
numeric_data = data.select_dtypes(include=['number'])

app = Dash(__name__)

app.layout = html.Div([
     dash_table.DataTable(data=data.to_dict('records'),page_size=10),
    html.H4('EMPLOYEE_DATA'),
    html.P('Select Graphs'),
    dcc.Dropdown(
        id='selection',
        options=[
            {'label': "EmpDepartment VS PerformanceRating", 'value': "EmpDepartmentVSPerformanceRating"},
            {'label': "Histogram of TotalWorkExperienceInYears", 'value': "HistogramofTotalWorkExperienceInYears"},
            {'label': "Correlation Heatmap", 'value': "CorrelationHeatmap"},
            {'label': "ExperienceYearsAtThisCompany VS PerformanceRating", 'value': "ExperienceYearsAtThisCompanyVSPerformanceRating"},
            {'label': "Average performance rating by department", 'value': "averageperformanceratingbydepartment"},
            {'label': "Distribution of gender in the Organization", 'value': "DistributionofgenderintheOrganization"},
            {'label': "Distribution of Performance Ratings by Job Role", 'value': "DistributionofPerformanceRatingsbyJobRole"},
            {'label': "Distribution of Age", 'value': "DistributionofAge"},
        ],
        value='EmpDepartmentVSPerformanceRating',
    ),
dcc.Loading(dcc.Graph(id='graph'),type='cube')

])

@app.callback(
    Output("graph", "figure"),
    Input('selection', 'value'),
)
def display_animated_graph(selection):
    if selection == "EmpDepartmentVSPerformanceRating":
        fig = px.bar(data, x='EmpDepartment', color="EmpDepartment", y="PerformanceRating")
        return fig
    elif selection == "HistogramofTotalWorkExperienceInYears":
        fig = px.histogram(data, x='TotalWorkExperienceInYears', title='Histogram of TotalWorkExperienceInYears')
        fig.update_layout(xaxis_title='TotalWorkExperienceInYears', yaxis_title='Count')
        return fig
    elif selection == "CorrelationHeatmap":
        corr_matrix = numeric_data.corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.index,
            y=corr_matrix.columns,
            colorscale='Viridis'))
        fig.update_layout(title='Correlation Heatmap')
        return fig
    elif selection == "ExperienceYearsAtThisCompanyVSPerformanceRating":
        scatter_fig = px.scatter(data, x="ExperienceYearsAtThisCompany", y="PerformanceRating", color="EmpDepartment",
                         title="Scatter Plot of Experience Years vs. Performance Rating")
        scatter_fig.update_layout(xaxis_title="Experience Years at Company", yaxis_title="Performance Rating")
        return scatter_fig
    elif selection == "averageperformanceratingbydepartment":
        bar_fig = px.bar(data.groupby("EmpDepartment")["PerformanceRating"].mean().reset_index(),
        x="EmpDepartment", y="PerformanceRating",
        title="Average Performance Rating by Department")
        bar_fig.update_layout(xaxis_title="Department", yaxis_title="Average Performance Rating")
        return bar_fig
    elif selection == "DistributionofgenderintheOrganization":
        gender_pie_fig = px.pie(data, names="Gender", title="Gender Distribution in the Organization")
        return gender_pie_fig
    elif selection == "DistributionofPerformanceRatingsbyJobRole":
        box_fig = px.box(data, x="EmpJobRole", y="PerformanceRating",
                 title="Performance Rating Distribution by Job Role")
        box_fig.update_layout(xaxis_title="Job Role", yaxis_title="Performance Rating")
        return box_fig
    elif selection == "DistributionofAge":
        age_hist_fig = px.histogram(data, x="Age", nbins=20, title="Age Distribution")
        return age_hist_fig
    

if __name__ == '__main__':
    app.run_server(debug=True,port=8051)