import streamlit as st
import pandas as pd
import gdown
import plotly.express as px
import plotly.graph_objects as go

# Download the input file from Google Drive
download_url = 'https://drive.google.com/uc?id=12h0Dt1rLuxRHtacCMwCkXEKd5iooLYHG'
output = 'data.csv'
gdown.download(download_url, output, quiet=False)

# Load the Excel file
df = pd.read_csv(output)

# Display Dashboard's title
st.title('E-commerce Customer Behaviour')

# Create columns
col1, col2 = st.columns(2, gap='medium')

# Display gender pic chart in column 1
with col1:
    genders = df['Gender'].unique()
    gender_counts = df['Gender'].value_counts()
    gender_dict = {'Gender': genders, 'Counts': [gender_counts[k] for k in genders]}
    df_gender_counts = pd.DataFrame(gender_dict)
    pie_chart__gender = px.pie(df_gender_counts, values='Counts', names='Gender', color='Gender')
    st.write("<h2 style='text-align: center;'>Gender distribution</h2>", unsafe_allow_html=True)
    st.plotly_chart(pie_chart__gender, use_container_width=True)

# Display cards in column 2
with col2:
    # st.write('Total spend vs Average rating by Gender')
    st.metric(label='Number of customers', value=len(df['Customer ID'].unique()))
    st.metric(label='Total number of items sold', value=df['Items Purchased'].sum())
    st.metric(label='Total Revenue (USD)', value=round(df['Total Spend'].sum()))
    st.metric(label='Average Rating', value=round(df['Average Rating'].mean(), 1))
    st.metric(label='Average Days Since Last Purchase', value=round(df['Days Since Last Purchase'].mean(), 1))

st.divider()

# Let user select gender(s)
gender_list = ['All', 'Female', 'Male']
selected_genders = st.selectbox('Select gender(s)', gender_list, index=0)
if selected_genders != 'All':
    df_selected_genders = df[df['Gender'] == selected_genders]
else:
    df_selected_genders = df

# Create columns
col1, col2 = st.columns(2, gap='medium')

# Spend vs rating chart
with col1:
    title = 'Total spend vs Average rating'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    scatter_plot__spend_vs_rating = px.scatter(df_selected_genders, x='Average Rating', y='Total Spend')
    st.plotly_chart(scatter_plot__spend_vs_rating, use_container_width=True)

# Average Rating vs Satisfaction Level
with col2:
    title = 'Average Rating vs Satisfaction Level'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    scatter_plot__rating_vs_satisfaction = px.scatter(df_selected_genders, x='Satisfaction Level', y='Average Rating')
    st.plotly_chart(scatter_plot__rating_vs_satisfaction, use_container_width=True)

st.divider()

# Spend vs Age
title = 'Total spend vs Age by Gender'
st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
bar_chart__spend_vs_age = px.bar(df, x='Age', y='Total Spend', barmode='group', color='Gender')
st.plotly_chart(bar_chart__spend_vs_age, use_container_width=True)

# Rating distribution by gender
title = 'Rating by Gender'
st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
fig = go.Figure(
    data=[  
        go.Histogram(x=df[df['Gender'] == 'Male']['Average Rating'], name='Male', marker_color='blue'),
        go.Histogram(x=df[df['Gender'] == 'Female']['Average Rating'], name='Female')
    ]
)
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
fig.update_xaxes(title_text='Average Rating')
fig.update_yaxes(title_text='Number of Occurences')
st.plotly_chart(fig, use_container_width=True)

# Days Since Last Purchase distribution by gender
title = 'Days Since Last Purchase by Gender'
st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
fig = go.Figure(
    data=[  
        go.Histogram(x=df[df['Gender'] == 'Male']['Days Since Last Purchase'], name='Male', marker_color='blue'),
        go.Histogram(x=df[df['Gender'] == 'Female']['Days Since Last Purchase'], name='Female')
    ]
)
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
fig.update_xaxes(title_text='Days Since Last Purchase')
fig.update_yaxes(title_text='Number of Occurences')
st.plotly_chart(fig, use_container_width=True)

# Items purchased distribution by gender
title = 'Number of Items Purchased by Gender'
st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
fig = go.Figure(
    data=[  
        go.Histogram(x=df[df['Gender'] == 'Male']['Items Purchased'], name='Male', marker_color='blue'),
        go.Histogram(x=df[df['Gender'] == 'Female']['Items Purchased'], name='Female')
    ]
)
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
fig.update_xaxes(title_text='Number of Items Purchased')
fig.update_yaxes(title_text='Number of Occurences')
st.plotly_chart(fig, use_container_width=True)

# Membership type distribution by gender
title = 'Membership Type by Gender'
st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
fig = go.Figure(
    data=[  
        go.Histogram(x=df[df['Gender'] == 'Male']['Membership Type'], name='Male', marker_color='blue'),
        go.Histogram(x=df[df['Gender'] == 'Female']['Membership Type'], name='Female')
    ]
)
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
fig.update_xaxes(title_text='Membership Type')
fig.update_yaxes(title_text='Number of clients')
st.plotly_chart(fig, use_container_width=True)