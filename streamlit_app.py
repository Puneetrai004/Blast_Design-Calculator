import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Blast Design Calculator",
    page_icon="💥",
    layout="wide"
)

def main():
    # Custom CSS to improve appearance
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #3498db;
        margin-top: 1rem;
    }
    .info-text {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<p class="main-header">Blast Design Calculator for Open Cast Mines</p>', unsafe_allow_html=True)
    
    # Brief description
    with st.expander("About this application", expanded=False):
        st.markdown("""
        This application helps mining engineers design blast patterns for open cast mines.
        Enter the parameters in the sidebar and click 'Calculate Blast Design' to get the results.
        
        The calculated parameters include:
        - Spacing between blast holes
        - Burden (distance between rows)
        - Explosive charge per hole
        - Powder factor (kg/m³)
        
        The application will also display a visual representation of the blast pattern.
        """)
    
    # Create sidebar for inputs
    with st.sidebar:
        st.markdown('<p class="section-header">Input Parameters</p>', unsafe_allow_html=True)
        
        # Create tabs for different parameter categories
        tab1, tab2, tab3 = st.tabs(["Geometry", "Explosive", "Rock Properties"])
        
        with tab1:
            bench_height = st.number_input("Bench height (m)", min_value=1.0, max_value=30.0, value=10.0, step=0.5)
            hole_diameter = st.number_input("Hole diameter (mm)", min_value=50.0, max_value=400.0, value=150.0, step=5.0)
            sub_drill = st.number_input("Sub-drill (m)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
            stemming = st.number_input("Stemming (m)", min_value=0.5, max_value=10.0, value=3.0, step=0.1)
        
        with tab2:
            base_charge = st.number_input("Base charge (kg)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)
            column_charge = st.number_input("Column charge (kg)", min_value=1.0, max_value=200.0, value=50.0, step=1.0)
            delay_element = st.selectbox("Delay element (ms)", options=[25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500], index=7)
        
        with tab3:
            rock_strength = st.selectbox("Rock strength", ["Hard", "Medium", "Soft", "Very Soft"], index=1)
            
            # Display powder factor range based on rock strength
            powder_factor_ranges = {
                "Hard": (0.7, 0.8),
                "Medium": (0.4, 0.5),
                "Soft": (0.25, 0.35),
                "Very Soft": (0.15, 0.25)
            }
            
            pf_min, pf_max = powder_factor_ranges.get(rock_strength, (0.4, 0.5))
            st.markdown(f'<div class="info-text">Recommended powder factor for {rock_strength.lower()} rock: {pf_min} - {pf_max} kg/m³</div>', unsafe_allow_html=True)
        
        calculate_button = st.button("Calculate Blast Design", type="primary", use_container_width=True)
    
    # Main content area
    if calculate_button:
        # Calculate parameters
        spacing, burden, explosive_charge, powder_factor = calculate_parameters(
            bench_height, hole_diameter, sub_drill, stemming, base_charge, column_charge, pf_min, pf_max)
        
        # Display results in the main area with two columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<p class="section-header">Calculated Parameters</p>', unsafe_allow_html=True)
            
            # Create a DataFrame for calculated parameters
            results_df = pd.DataFrame({
                'Parameter': ['Spacing', 'Burden', 'Hole Depth', 'Explosive Charge per Hole', 'Powder Factor', 'Delay Element'],
                'Value': [f"{spacing:.2f} m", f"{burden:.2f} m", f"{bench_height + sub_drill:.2f} m", 
                          f"{explosive_charge:.2f} kg", f"{powder_factor:.3f} kg/m³", f"{delay_element} ms"]
            })
            
            st.table(results_df)
            
            # Display powder factor status
            if pf_min <= powder_factor <= pf_max:
                st.success(f"✅ Powder factor ({powder_factor:.3f} kg/m³) is within the acceptable range for {rock_strength.lower()} rock.")
            else:
                st.warning(f"⚠️ Warning: Powder factor ({powder_factor:.3f} kg/m³) is outside the recommended range for {rock_strength.lower()} rock ({pf_min} - {pf_max} kg/m³)!")
                
                if powder_factor < pf_min:
                    st.info("Consider increasing the explosive charge or reducing the spacing/burden.")
                else:
                    st.info("Consider decreasing the explosive charge or increasing the spacing/burden.")
        
        with col2:
            st.markdown('<p class="section-header">Blast Hole Layout</p>', unsafe_allow_html=True)
            visualize_blast_pattern(spacing, burden)
            
            # Display blast hole profile
            st.markdown('<p class="section-header">Blast Hole Profile</p>', unsafe_allow_html=True)
            visualize_blast_hole_profile(bench_height, sub_drill, stemming, hole_diameter)
    else:
        # Display placeholder in main area when app starts
        st.info("👈 Enter parameters in the sidebar and click 'Calculate Blast Design' to see results")
        
        # Display sample blast pattern image as placeholder
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="section-header">Sample Blast Pattern</p>', unsafe_allow_html=True)
            visualize_blast_pattern(3.75, 4.5, total_holes=20)
        
        with col2:
            st.markdown('<p class="section-header">Sample Blast Hole Profile</p>', unsafe_allow_html=True)
            visualize_blast_hole_profile(10.0, 2.0, 3.0, 150.0)

def calculate_parameters(bench_height, hole_diameter, sub_drill, stemming, base_charge, column_charge, pf_min, pf_max):
    # Improved formulas based on hole diameter in mm
    burden = hole_diameter / 1000 * 25  # Better approximation
    spacing = burden * 1.25  # Typical spacing-to-burden ratio
    
    # Calculate total explosive charge
    explosive_charge = base_charge + column_charge
    
    # Calculate powder factor
    powder_factor = explosive_charge / (spacing * burden * bench_height)
    
    return spacing, burden, explosive_charge, powder_factor

def visualize_blast_pattern(spacing, burden, total_holes=30):
    # Create a more realistic blast pattern
    rows = 5
    cols = total_holes // rows
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create a staggered pattern for better blasting results
    for i in range(rows):
        offset = (i % 2) * spacing / 2  # Stagger alternate rows
        for j in range(cols):
            ax.scatter(j * spacing + offset, i * burden, color='red', s=100, edgecolor='black')
            ax.text(j * spacing + offset, i * burden, f"{i*cols+j+1}", fontsize=8, 
                   ha='center', va='center', color='white')
    
    # Add legend and details
    ax.set_title("Blast Hole Layout (Staggered Pattern)")
    ax.set_xlabel("Spacing (m)")
    ax.set_ylabel("Burden (m)")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set axis limits
    ax.set_xlim(-spacing/2, (cols-0.5) * spacing + spacing/2)
    ax.set_ylim(-burden/2, (rows-0.5) * burden + burden/2)
    
    # Add scale information
    ax.text(0.02, 0.98, f"Spacing: {spacing:.2f} m\nBurden: {burden:.2f} m", 
           transform=ax.transAxes, va='top', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    st.pyplot(fig)

def visualize_blast_hole_profile(bench_height, sub_drill, stemming, hole_diameter):
    # Create a visual representation of the blast hole profile
    fig, ax = plt.subplots(figsize=(4, 8))
    
    # Calculate total hole depth
    total_depth = bench_height + sub_drill
    
    # Define hole dimensions for visualization
    hole_width = hole_diameter / 1000  # Convert mm to m for scale
    scaled_width = 0.5  # Fixed width for visualization
    
    # Draw hole outline
    ax.plot([-scaled_width/2, -scaled_width/2], [0, -total_depth], 'k-', linewidth=2)
    ax.plot([scaled_width/2, scaled_width/2], [0, -total_depth], 'k-', linewidth=2)
    ax.plot([-scaled_width/2, scaled_width/2], [-total_depth, -total_depth], 'k-', linewidth=2)
    
    # Draw ground level
    ax.plot([-scaled_width*2, scaled_width*2], [0, 0], 'k-', linewidth=3)
    
    # Fill stemming section
    ax.fill_between([-scaled_width/2, scaled_width/2], 0, -stemming, color='tan', alpha=0.7)
    
    # Fill explosive column section
    ax.fill_between([-scaled_width/2, scaled_width/2], -stemming, -total_depth, color='yellow', alpha=0.7)
    
    # Fill sub-drill section
    ax.fill_between([-scaled_width/2, scaled_width/2], -bench_height, -total_depth, color='orange', alpha=0.4)
    
    # Add annotations
    ax.annotate('Stemming', xy=(scaled_width/2 + 0.1, -stemming/2), xytext=(scaled_width + 0.1, -stemming/2),
               arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    ax.annotate('Explosive\nColumn', xy=(scaled_width/2 + 0.1, -(stemming + (bench_height - stemming)/2)),
               xytext=(scaled_width + 0.1, -(stemming + (bench_height - stemming)/2)),
               arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    ax.annotate('Sub-drill', xy=(scaled_width/2 + 0.1, -(bench_height + sub_drill/2)),
               xytext=(scaled_width + 0.1, -(bench_height + sub_drill/2)),
               arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    # Add horizontal line at bench height
    ax.plot([-scaled_width*2, scaled_width*2], [-bench_height, -bench_height], 'k--', linewidth=1)
    ax.annotate('Bench\nHeight', xy=(-scaled_width*1.5, -bench_height/2), ha='center', va='center')
    
    # Add measurements
    ax.text(-scaled_width*1.5, -stemming, f"{stemming} m", va='center', ha='right')
    ax.text(-scaled_width*1.5, -(stemming + (bench_height - stemming)/2), 
           f"{bench_height - stemming} m", va='center', ha='right')
    ax.text(-scaled_width*1.5, -(bench_height + sub_drill/2), f"{sub_drill} m", va='center', ha='right')
    ax.text(0, -total_depth - 0.5, f"Total depth: {total_depth} m | Diameter: {hole_diameter} mm", ha='center')
    
    # Set plot properties
    ax.set_title("Blast Hole Profile")
    ax.set_xlabel("Width")
    ax.set_ylabel("Depth (m)")
    ax.set_xlim(-scaled_width*2, scaled_width*3)
    ax.set_ylim(-total_depth - 1, 1)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Remove x-axis ticks
    ax.set_xticks([])
    
    st.pyplot(fig)

if __name__ == "__main__":
    main()
