# dashboard.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import os
import sys
import json
from datetime import datetime

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import project modules
from main_container import MainContainer, BBOX_LAT_MIN, BBOX_LAT_MAX, BBOX_LNG_MIN, BBOX_LNG_MAX
from common_utils.logger_setup import setup_logger

# Setup logger
logger = setup_logger("StreamlitDashboard", log_level="INFO", log_file="logs/dashboard.log")

# Page configuration
st.set_page_config(
    page_title="Real Estate Crawler Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Real Estate Crawler Dashboard")
st.markdown("""
This dashboard visualizes real estate data collected from Zigbang and Dabang platforms.
Use the sidebar to configure the crawler and view the results.
""")

# Sidebar for configuration
st.sidebar.header("Crawler Configuration")

# Bounding box configuration
st.sidebar.subheader("Area Selection")
col1, col2 = st.sidebar.columns(2)
with col1:
    lat_min = st.number_input("Latitude Min", value=BBOX_LAT_MIN, format="%.6f")
    lng_min = st.number_input("Longitude Min", value=BBOX_LNG_MIN, format="%.6f")
with col2:
    lat_max = st.number_input("Latitude Max", value=BBOX_LAT_MAX, format="%.6f")
    lng_max = st.number_input("Longitude Max", value=BBOX_LNG_MAX, format="%.6f")

# Platform selection
platforms = st.sidebar.multiselect(
    "Select Platforms",
    ["Zigbang", "Dabang"],
    default=["Zigbang"]
)

# Property type selection
property_types = st.sidebar.multiselect(
    "Property Types",
    ["villa", "apt", "oneroom", "officetel"],
    default=["villa"]
)

# Run crawler button
if st.sidebar.button("Run Crawler"):
    with st.spinner("Running crawler..."):
        try:
            # Create MainContainer instance
            container = MainContainer()
            
            # Store results
            results = {}
            
            # Run for selected platforms
            if "Zigbang" in platforms:
                for property_type in property_types:
                    st.info(f"Collecting Zigbang {property_type} data...")
                    zigbang_item_ids = container.zigbang_collector.collect_item_ids_by_area(
                        lat_min, lat_max, lng_min, lng_max, item_type=property_type
                    )
                    
                    # Store results
                    if property_type not in results:
                        results[property_type] = {}
                    
                    results[property_type]["Zigbang"] = {
                        "item_ids": zigbang_item_ids,
                        "count": len(zigbang_item_ids)
                    }
                    
                    st.success(f"Found {len(zigbang_item_ids)} Zigbang {property_type} properties")
            
            # Save results to session state
            st.session_state.results = results
            st.session_state.last_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            st.error(f"Error running crawler: {str(e)}")
            logger.error(f"Error running crawler: {str(e)}", exc_info=True)

# Display results
st.header("Crawler Results")

# Check if results exist in session state
if hasattr(st.session_state, 'results') and st.session_state.results:
    st.subheader(f"Last Run: {st.session_state.last_run}")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Summary", "Map View", "Raw Data"])
    
    with tab1:
        # Summary statistics
        st.subheader("Summary Statistics")
        
        # Create summary dataframe
        summary_data = []
        for property_type, platforms_data in st.session_state.results.items():
            for platform, data in platforms_data.items():
                summary_data.append({
                    "Property Type": property_type,
                    "Platform": platform,
                    "Count": data["count"]
                })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            
            # Display summary table
            st.dataframe(summary_df, use_container_width=True)
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            summary_pivot = summary_df.pivot(index="Property Type", columns="Platform", values="Count")
            summary_pivot.plot(kind="bar", ax=ax)
            ax.set_ylabel("Number of Properties")
            ax.set_title("Properties by Type and Platform")
            st.pyplot(fig)
        else:
            st.info("No data available for summary")
    
    with tab2:
        # Map visualization
        st.subheader("Map View")
        
        # Create a map centered at the middle of the bounding box
        center_lat = (lat_min + lat_max) / 2
        center_lng = (lng_min + lng_max) / 2
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=15)
        
        # Add rectangle for the bounding box
        folium.Rectangle(
            bounds=[(lat_min, lng_min), (lat_max, lng_max)],
            color="blue",
            fill=True,
            fill_opacity=0.1,
            tooltip="Search Area"
        ).add_to(m)
        
        # Display the map
        folium_static(m)
        
        st.info("Note: Detailed property locations would be shown here if available from the API")
    
    with tab3:
        # Raw data
        st.subheader("Raw Data")
        
        # Select property type and platform
        property_type_options = list(st.session_state.results.keys())
        if property_type_options:
            selected_property_type = st.selectbox("Select Property Type", property_type_options)
            
            platform_options = list(st.session_state.results[selected_property_type].keys())
            selected_platform = st.selectbox("Select Platform", platform_options)
            
            # Display raw data
            raw_data = st.session_state.results[selected_property_type][selected_platform]
            st.json(raw_data)
        else:
            st.info("No raw data available")

else:
    st.info("No crawler results yet. Configure and run the crawler using the sidebar.")

# Footer
st.markdown("---")
st.markdown("© 2025 Real Estate Crawler Dashboard")