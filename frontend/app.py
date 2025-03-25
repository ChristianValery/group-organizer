"""
Streamlit frontend for the Seating Arrangement Tool.

This script provides a Streamlit app that allows users to upload an Excel file
containing participant details and compatibility constraints. The app then sends
the file to the FastAPI backend for processing and generates a seating arrangement
based on the constraints provided.

The app displays the seating arrangement and allows users to download the seating
plan in Excel format.

To run the Streamlit app, execute the following command from the `frontend` directory:
```	
    streamlit run app.py
```
"""


import io
import os

import pandas as pd
import streamlit as st
import requests
from streamlit.components.v1 import html


# Get the FastAPI base URL from the environment variable or use the default value
FAST_API_BASE_URL = os.environ.get(
    "FAST_API_BASE_URL", "http://localhost:8000")

# Configure Streamlit page
st.set_page_config(
    page_title='醐 Group organizer / Seating Arrangement Tool',
    layout='wide'
)

# Custom styling
st.markdown(
    """
    <style>
    .center {
        text-align: center;
    }
    .file-uploader {
        width: 600px;
        margin: 20px auto;
    }
    .section-break {
        margin: 3rem 0;
        padding: 2px 0;
        border-top: 1px solid #eee;
        display: block;
        width: 100%;
    }
    .download-btn {
        background-color: #4CAF50 !important;
        color: white !important;
        padding: 12px 24px !important;
        border: none !important;
        border-radius: 5px !important;
        cursor: pointer;
        font-weight: bold !important;
        display: inline-block !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    """
    Main function for the Streamlit app with a sidebar and two pages.
    """
    # Add a custom icon at the top
    html(
        """
        <div style="text-align: center; padding: 20px;">
            <i class="fas fa-chairs" style="font-size: 4rem; color: #4CAF50;"></i>
        </div>
        """,
        width=100,
        height=100,
    )

    # Sidebar section selector
    section = st.sidebar.selectbox(
        "Choose a section", ["How to Use This Tool", "Seating Arrangement Tool"])

    if section == "How to Use This Tool":
        st.title("How to Use This Tool")
        st.markdown("""
        1. 📁 **Prepare Your Data**: Upload an Excel file with names and compatibility constraints.
        2. ⚙️ **Specify Table (Group) Capacity**: Indicate the number of seats per table.
        3. 🔧 **Generate Seating Plan**: Click the **Generate Seating** button to create the arrangement.
        4. 📥 **Download Plan**: Once generated, download the seating plan in Excel format.
        
        Ensure your Excel file has exactly one sheet with the following columns:
        - `name`: People's names
        - `compatible`: Pairs of compatible persons (two names separated by a colon `:`)
        - `incompatible`: Pairs of incompatible persons (two names separated by a slash `/`)
        """)
        with open('files/names.xlsx', 'rb') as f:
            st.download_button(
                label='⬇️ Download a Model File',
                data=f,
                file_name='names.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key='sample_fileBtn'
            )

    elif section == "Seating Arrangement Tool":
        st.title("Seating Arrangement Tool")
        st.write(
            "Upload your Excel file and set the table capacity to generate a seating arrangement.")

        # File Upload
        uploaded_file = st.file_uploader(
            "Upload Excel File",
            type=['xlsx', 'xls'],
            key='file_uploader'
        )

        # Table Capacity
        if 'table_capacity' not in st.session_state:
            st.session_state['table_capacity'] = 4
        table_capacity = st.number_input(
            "Number of Seats per Table",
            min_value=2,
            value=st.session_state['table_capacity'],
            key='capacityInput'
        )
        st.session_state['table_capacity'] = table_capacity

        # Generate Seating Button
        if uploaded_file:
            if st.button("Generate Seating", key='generateBtn'):
                try:
                    df_uploaded = pd.read_excel(uploaded_file)
                    df_uploaded = df_uploaded.fillna("")
                    df_uploaded = df_uploaded.set_index("name")
                    data = {'table_capacity': table_capacity}
                    files = {'file': uploaded_file.getvalue()}
                    with st.spinner("Processing your request..."):
                        response = requests.post(
                            f"{FAST_API_BASE_URL}/upload/",
                            params=data,
                            files=files,
                            timeout=30
                        )
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('status'):
                            session_id = result.get('session_id')
                            st.success("Upload successful!")
                            st.session_state['session_id'] = session_id
                            st.session_state['df_uploaded'] = df_uploaded
                        else:
                            st.error(
                                f"Failed: {result.get('message', 'Unknown error')}")
                            st.write("Please check your data and try again.")
                            st.dataframe(df_uploaded)
                    else:
                        st.error(
                            f"API request failed with status code: {response.status_code}")
                except requests.exceptions.Timeout:
                    st.error("The request has timed out. Please try again.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {str(e)}")

        # Visual separator
        st.markdown("---")

        # Display Seating Arrangement if generated
        if 'session_id' in st.session_state:
            session_id = st.session_state['session_id']
            try:
                with st.spinner("Fetching your seating arrangement..."):
                    response = requests.get(
                        f"{FAST_API_BASE_URL}/download/",
                        params={'session_id': session_id},
                        timeout=30
                    )
                if response.status_code == 200:
                    st.success("Seating plan generated successfully!")
                    seating_file = io.BytesIO(response.content)
                    df_seating = pd.read_excel(seating_file)
                    df_seating["Seats"] = [
                        "Seat " + str(i+1) for i in range(len(df_seating))]
                    df_seating = df_seating.set_index("Seats")
                    df_seating = df_seating.fillna("")
                    st.write("Here is your seating arrangement:")
                    col3, col4 = st.columns([2, 1])
                    with col3:
                        st.dataframe(df_seating)
                    with col4:
                        st.dataframe(st.session_state.get('df_uploaded'))
                    st.download_button(
                        label="⬇️ Download Excel File",
                        data=response.content,
                        file_name=f"seating_arrangement_{session_id}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key='downloadBtn'
                    )
                else:
                    st.error(
                        "Failed to retrieve your seating plan. Please try again.")
            except requests.exceptions.Timeout:
                st.error("The request has timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
