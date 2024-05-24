import streamlit as st
import pandas as pd
import gdown
import plotly.express as px
import plotly.graph_objects as go


def get_metric_cards(df):
    """ Define all the cards with metrics """
    cards = [
        {'label': 'Number of customers', 'value': len(df['Customer ID'].unique())},
        {'label': 'Total number of items sold', 'value': df['Items Purchased'].sum()},
        {'label': 'Total Revenue (USD)', 'value': round(df['Total Spend'].sum())},
        {'label': 'Average Rating', 'value': round(df['Average Rating'].mean(), 1)},
        {'label': 'Average Days Since Last Purchase', 'value': round(df['Days Since Last Purchase'].mean(), 1)}
    ]
    return cards


def get_gender_pie_chart(df, color_map):
    """ Show Gender distribution in a Pie Chart """
    genders = df['Gender'].unique()
    gender_counts = df['Gender'].value_counts()
    gender_dict = {'Gender': genders, 'Counts': [gender_counts[k] for k in genders]}
    df_gender_counts = pd.DataFrame(gender_dict)
    fig = px.pie(df_gender_counts, values='Counts', names='Gender', color='Gender', color_discrete_map=color_map)
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1,
    ))
    return st.plotly_chart(fig, use_container_width=True)


def get_spend_vs_rating_chart(df, marker_color):
    """ Total Spend vs Average Rating """
    fig = px.scatter(df, x='Average Rating', y='Total Spend', color_discrete_sequence=[marker_color])
    return st.plotly_chart(fig, use_container_width=True)


def get_rating_vs_satisfaction_chart(df, marker_color):
    """ Average Rating vs Satisfaction Level """
    fig = px.scatter(df, x='Satisfaction Level', y='Average Rating', color_discrete_sequence=[marker_color])
    return st.plotly_chart(fig, use_container_width=True)


def get_spend_vs_age_chart(df, color_map):
    """ Total Spend vs Age """
    fig = px.bar(df, x='Age', y='Total Spend', color='Gender', color_discrete_map=color_map)
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1,
    ))
    return st.plotly_chart(fig, use_container_width=True)

def get_rating_chart(df, color_map):
    """ Average Rating by Gender """
    fig = go.Figure(
        data = [  
            go.Histogram(
                x = df[df['Gender'] == 'Male']['Average Rating'],
                name = 'Male',
                marker = dict(
                    color = 'rgba(0,0,0,0)',  # transparent fill
                    line = dict(color=color_map['Male'], width=3)
                )
            ),
            go.Histogram(
                x = df[df['Gender'] == 'Female']['Average Rating'],
                name = 'Female',
                marker = dict(
                    color = 'rgba(0,0,0,0)',  # transparent fill
                    line = dict(color=color_map['Female'], width=3)
                )
            )
        ],
        layout = go.Layout(legend={'traceorder':'reversed'})
    )
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1,
    ))
    fig.update_layout(barmode='overlay')
    fig.update_xaxes(title_text='Average Rating')
    fig.update_yaxes(title_text='Number of Occurences')
    return st.plotly_chart(fig, use_container_width=True)


def get_days_last_purchase_chart(df, color_map):
    """ Days Since Last Purchase by Gender """
    fig = go.Figure(
        data=[  
            go.Histogram(
                x = df[df['Gender'] == 'Male']['Days Since Last Purchase'],
                name = 'Male',
                marker = dict(
                    color = 'rgba(0,0,0,0)',  # transparent fill
                    line = dict(color=color_map['Male'], width=3)
                )
            ),
            go.Histogram(
                x = df[df['Gender'] == 'Female']['Days Since Last Purchase'],
                name = 'Female',
                marker = dict(
                    color = 'rgba(0,0,0,0)',  # transparent fill
                    line = dict(color=color_map['Female'], width=3)
                )
            )
        ],
        layout = go.Layout(legend={'traceorder':'reversed'})
    )
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1,
    ))
    fig.update_layout(barmode='overlay')
    fig.update_xaxes(title_text='Days Since Last Purchase')
    fig.update_yaxes(title_text='Number of Occurences')
    return st.plotly_chart(fig, use_container_width=True)


def get_items_chart(df, color_map):
    fig = go.Figure(
        data=[  
            go.Histogram(
                x = df[df['Gender'] == 'Male']['Items Purchased'],
                name = 'Male',
                marker = dict(
                    color = 'rgba(0,0,0,0)',  # transparent fill
                    line = dict(color=color_map['Male'], width=3)
                )
            ),
            go.Histogram(
                x = df[df['Gender'] == 'Female']['Items Purchased'],
                name='Female',
                marker = dict(
                    color = 'rgba(0,0,0,0)',  # transparent fill
                    line = dict(color=color_map['Female'], width=3)
                )
            )
        ],
        layout = go.Layout(legend={'traceorder':'reversed'})
    )
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1,
    ))
    fig.update_layout(barmode='overlay')
    fig.update_xaxes(title_text='Number of Items Purchased')
    fig.update_yaxes(title_text='Number of Occurences')
    return st.plotly_chart(fig, use_container_width=True)


def get_membership_chart(df, color_map):
    fig = go.Figure(
        data=[  
            go.Histogram(
                x = df[df['Gender'] == 'Male']['Membership Type'],
                name = 'Male',
                marker_color = color_map['Male']
            ),
            go.Histogram(
                x = df[df['Gender'] == 'Female']['Membership Type'],
                name = 'Female',
                marker_color = color_map['Female']
            )
        ],
        layout = go.Layout(legend={'traceorder':'reversed'})
    )
    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1,
    ))
    fig.update_layout(barmode='overlay')
    fig.update_xaxes(title_text='Membership Type')
    fig.update_yaxes(title_text='Number of clients')
    return st.plotly_chart(fig, use_container_width=True)


def main():

    # Download the input file from Google Drive
    download_url = 'https://drive.google.com/uc?id=12h0Dt1rLuxRHtacCMwCkXEKd5iooLYHG'
    output = 'data.csv'
    gdown.download(download_url, output, quiet=True)

    # Load the Excel file
    df = pd.read_csv(output)

    # Define color map for genders
    color_map = {
        'All': '#00CC96',
        'Female': '#000001',
        'Male': '#000002'
    }

    # Display Dashboard's title
    st.title('E-commerce Customer Behaviour')

    # Create columns
    col1, col2 = st.columns(2, gap='medium')

    # Display metric cards in column 1
    with col1:
        st.write("<h2 style='text-align: left;'>Overview</h2>", unsafe_allow_html=True)
        for card in get_metric_cards(df):  # loop over metric cards
            st.metric(**card)

    # Display gender pie chart in column 2
    with col2:
        st.write("<h2 style='text-align: center;'>Gender distribution</h2>", unsafe_allow_html=True)
        get_gender_pie_chart(df, color_map)

    # Show line divider to clearly separate charts relying on st.selectbox()
    st.divider()

    # Let user select gender(s)
    gender_list = ['All', 'Female', 'Male']
    selected_genders = st.selectbox('Select gender(s)', gender_list, index=0)
    if selected_genders != 'All':
        df_selected_genders = df[df['Gender'] == selected_genders]
    else:
        df_selected_genders = df
    color_for_selected_gender = color_map[selected_genders]

    # Create columns
    col1, col2 = st.columns(2, gap='medium')

    # Spend vs rating chart
    with col1:
        title = 'Total spend vs Average rating'
        st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
        get_spend_vs_rating_chart(df_selected_genders, color_for_selected_gender)

    # Average Rating vs Satisfaction Level
    with col2:
        title = 'Average Rating vs Satisfaction Level'
        st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
        get_rating_vs_satisfaction_chart(df_selected_genders, color_for_selected_gender)

    st.divider()

    # Spend vs Age
    title = 'Total spend vs Age by Gender'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    get_spend_vs_age_chart(df, color_map)

    # Rating distribution by gender
    title = 'Rating by Gender'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    get_rating_chart(df, color_map)

    # Days Since Last Purchase distribution by gender
    title = 'Days Since Last Purchase by Gender'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    get_days_last_purchase_chart(df, color_map)

    # Items purchased distribution by gender
    title = 'Number of Items Purchased by Gender'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    get_items_chart(df, color_map)

    # Membership type distribution by gender
    title = 'Membership Type by Gender'
    st.write("<h2 style='text-align: center;'>"+title+"</h2>", unsafe_allow_html=True)
    get_membership_chart(df, color_map)

if __name__ == '__main__':
    main()