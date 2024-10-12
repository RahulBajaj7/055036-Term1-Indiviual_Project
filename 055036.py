import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Apply custom styling (black background for the entire app, white text, and vibrant charts)
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: black;
    }
    section[data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    section[data-testid="stSidebar"] label {
        color: white;
    }
    .stTextInput label, .stSelectbox label, .stMultiSelect label, .stDateInput label, .stHeader, h1, h2 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add the dashboard heading to the header
st.header("Import Export Dashboard")

# Load the dataset into df_uq
file_path = r'C:\Users\rahul\Downloads\Imports_Exports_Dataset.csv'

try:
    df_uq = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime format
    df_uq['Date'] = pd.to_datetime(df_uq['Date'], errors='coerce')  # Convert with coercion to handle invalid dates

    # Chart type for user selections
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Pie", "Bar", "Line", "Scatter", "Box", "Heatmap", "Histogram"])

    # Sidebar for user selections
    st.sidebar.header("Filter Options")

    # Define available filter options
    categorical_options = ['Country', 'Product', 'Import_Export', 'Category', 'Port', 'Shipping_Method', 'Supplier', 'Customer', 'Payment_Terms']
    numeric_options = ['Quantity', 'Value', 'Weight']

    # Apply date filter where applicable
    min_date = df_uq['Date'].min()
    max_date = df_uq['Date'].max()
    date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date])

    # Filter dataset by selected date range (applies to all charts)
    if date_range:
        df_uq = df_uq[(df_uq['Date'] >= pd.Timestamp(date_range[0])) & (df_uq['Date'] <= pd.Timestamp(date_range[1]))]

    # Adjust available filters based on chart type
    if chart_type in ["Pie", "Bar"]:
        # For Pie and Bar charts, show limited categorical options and set all as selected by default
        default_selection = ['Shipping_Method', 'Import_Export', 'Payment_Terms', 'Category'] if chart_type == "Pie" else ['Shipping_Method', 'Import_Export', 'Payment_Terms']
        selected_categorical_var = st.sidebar.multiselect(
            'Select Categorical Variables for Visualization',
            default_selection,  # All filters are selected by default
            default=default_selection
        )

    elif chart_type == "Box":
        # For Box plots, only allow 'Shipping_Method'
        selected_categorical_var = st.sidebar.multiselect(
            'Select Categorical Variables for Visualization',
            ['Shipping_Method'],
            default=['Shipping_Method']
        )

    elif chart_type == "Line":
        # For Line chart, allow date and numeric filters
        selected_numeric_var = st.sidebar.selectbox("Select Variable for Y-axis", ['Quantity', 'Value', 'Weight'])

    elif chart_type == "Scatter":
        # Scatter plot filters for numeric variables
        selected_numeric_x = st.sidebar.selectbox('Select X-axis for Scatter Plot', numeric_options)
        selected_numeric_y = st.sidebar.selectbox('Select Y-axis for Scatter Plot', numeric_options, index=1)

    elif chart_type == "Heatmap":
        # Heatmap allows selection of numeric variables only
        selected_heatmap_vars = st.sidebar.multiselect('Select Numeric Variables for Heatmap', numeric_options, default=numeric_options)

    elif chart_type == "Histogram":
        # Histogram for a single numeric variable
        selected_hist_var = st.sidebar.selectbox('Select Numeric Variable for Histogram', numeric_options)

    # Dynamic chart rendering based on the selected chart type
    if chart_type == "Pie":
        st.write("### Categorical Variables - Pie Charts")
        cols = st.columns(2)
        for i, var in enumerate(selected_categorical_var):
            with cols[i % 2]:  # Display two pie charts side by side
                fig = px.pie(df_uq, names=var, title=f'Pie Chart of {var}')
                fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
                st.plotly_chart(fig)

    elif chart_type == "Bar":
        for var in selected_categorical_var:
            st.write(f"### Bar Plot - {var}")
            fig = px.bar(df_uq, x=var, title=f'Bar Plot of {var}')
            fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
            st.plotly_chart(fig)

    elif chart_type == "Line":
        st.write(f"### Line Chart - {selected_numeric_var} over Time")
        fig = px.line(df_uq, x='Date', y=selected_numeric_var, title=f'Line Chart of {selected_numeric_var} over Time')
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Scatter":
        st.write(f"### Scatter Plot - {selected_numeric_x} vs {selected_numeric_y}")
        fig = px.scatter(df_uq, x=selected_numeric_x, y=selected_numeric_y, title=f'Scatter Plot of {selected_numeric_x} vs {selected_numeric_y}')
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Box":
        st.write("### Box Plot - Value Distribution per Shipping Method")
        fig = px.box(df_uq, x='Shipping_Method', y='Value', title="Box Plot of Value Distribution by Shipping Method")
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Heatmap":
        if selected_heatmap_vars:
            st.write("### Heatmap of Numeric Variables")
            correlation_matrix = df_uq[selected_heatmap_vars].corr()

            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='Viridis',
                colorbar=dict(title="Correlation")
            ))
            fig.update_layout(paper_bgcolor="black", font_color="white", title_font_color="white", title="Heatmap of Selected Variables")
            st.plotly_chart(fig)

    elif chart_type == "Histogram":
        st.write(f"### Histogram - {selected_hist_var}")
        fig = px.histogram(df_uq, x=selected_hist_var, nbins=30, title=f'Histogram of {selected_hist_var}', marginal="box")
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

except FileNotFoundError:
    st.error(f"File '{file_path}' not found. Please upload the correct dataset.")
