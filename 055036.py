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

    # Dynamic chart rendering based on the selected chart type
    if chart_type == "Pie":
        st.write("### Pie Charts for Shipping Method and Category")
        cols = st.columns(2)
        with cols[0]:
            fig = px.pie(df_uq, names='Shipping_Method', title='Pie Chart of Shipping Method')
            fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
            st.plotly_chart(fig)

        with cols[1]:
            fig = px.pie(df_uq, names='Category', title='Pie Chart of Category')
            fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
            st.plotly_chart(fig)

    elif chart_type == "Bar":
        st.write("### Bar Plot - Import/Export and Payment Terms")

        # Get unique values for color assignment
        import_export_colors = ['#DDA0DD', '#FFA07A']  # Light purple and light salmon for Import and Export
        payment_terms_colors = px.colors.qualitative.Plotly[:len(df_uq['Payment_Terms'].unique())]  # Unique colors for payment terms

        # Bar Plot for Import/Export
        fig = px.bar(df_uq, x='Import_Export', color='Import_Export', title='Bar Plot of Import/Export',
                     color_discrete_sequence=import_export_colors, barmode='group',
                     text='Quantity')  # Add text annotations for Quantity
        fig.update_layout(bargap=0.5, paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

        # Bar Plot for Payment Terms
        fig = px.bar(df_uq, x='Payment_Terms', color='Payment_Terms', title='Bar Plot of Payment Terms',
                     color_discrete_sequence=payment_terms_colors, barmode='group',
                     text='Quantity')  # Add text annotations for Quantity
        fig.update_layout(bargap=0.15, paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Line":
        st.write("### Line Chart for Import and Export Over Time")
        df_uq['Year'] = df_uq['Date'].dt.year  # Extract year from the date
        
        # Aggregate data for imports and exports
        import_export_summary = df_uq.groupby(['Year', 'Import_Export']).agg({'Quantity': 'sum'}).reset_index()

        # Plotly line chart with specific colors
        fig = px.line(import_export_summary, x='Year', y='Quantity', color='Import_Export', 
                      title='Line Chart of Imports and Exports Over Time', markers=True,
                      color_discrete_map={'Import': '#DDA0DD', 'Export': '#FFA07A'}, 
                      text='Quantity')  # Add text annotations for Quantity
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Scatter":
        st.write("### Scatter Plot - Quantity vs Value")
        fig = px.scatter(df_uq, x='Quantity', y='Value', color='Import_Export', 
                         title='Scatter Plot of Quantity vs Value (Imports and Exports)',
                         color_discrete_map={'Import': 'darkblue', 'Export': 'red'})
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Box":
        st.write("### Box Plot - Value Distribution per Shipping Method")
        fig = px.box(df_uq, x='Shipping_Method', y='Value', title="Box Plot of Value Distribution by Shipping Method")
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

    elif chart_type == "Heatmap":
        selected_heatmap_vars = st.sidebar.multiselect('Select Numeric Variables for Heatmap', numeric_options, default=numeric_options)
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
        selected_hist_var = st.sidebar.selectbox('Select Numeric Variable for Histogram', numeric_options)
        st.write(f"### Histogram - {selected_hist_var}")
        fig = px.histogram(df_uq, x=selected_hist_var, nbins=30, title=f'Histogram of {selected_hist_var}', marginal="box")
        fig.update_layout(paper_bgcolor="black", font_color="white", legend_font_color="white", title_font_color="white")
        st.plotly_chart(fig)

except FileNotFoundError:
    st.error(f"File '{file_path}' not found. Please upload the correct dataset.")

