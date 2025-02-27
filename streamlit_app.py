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
    .formula-text {
        background-color: #eff8ff;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #3498db;
        font-family: monospace;
        margin: 10px 0;
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
        - Burden (distance from free face)
        - Spacing between blast holes
        - Stemming length
        - Base charge length
        - Sub-drill depth
        - Powder factor (kg/m³)
        
        The application uses industry-standard formulas from sources like Atlas Copco, Konya, Hoek & Bray, and others.
        A visual representation of the blast pattern and hole profile is also provided.
        """)
    
    # Create sidebar for inputs
    with st.sidebar:
        st.markdown('<p class="section-header">Input Parameters</p>', unsafe_allow_html=True)
        
        # Create tabs for different parameter categories
        tab1, tab2, tab3 = st.tabs(["Geometry", "Rock & Explosive", "Formula Selection"])
        
        with tab1:
            bench_height = st.number_input("Bench height (m)", min_value=1.0, max_value=30.0, value=10.0, step=0.5)
            hole_diameter = st.number_input("Hole diameter (mm)", min_value=50.0, max_value=400.0, value=150.0, step=5.0)
            hole_condition = st.radio("Hole condition", ["Dry", "Wet"])
        
        with tab2:
            rock_type = st.selectbox("Rock strength", ["Hard", "Medium", "Soft", "Very Soft"], index=1)
            
            # Add density inputs
            explosive_density = st.number_input("Explosive density (g/cm³)", min_value=0.8, max_value=1.6, value=1.2, step=0.1)
            rock_density = st.number_input("Rock density (g/cm³)", min_value=1.5, max_value=4.0, value=2.6, step=0.1)
            
            # Powder factor range based on rock strength
            powder_factor_ranges = {
                "Hard": (0.7, 0.8),
                "Medium": (0.4, 0.5),
                "Soft": (0.25, 0.35),
                "Very Soft": (0.15, 0.25)
            }
            
            pf_min, pf_max = powder_factor_ranges.get(rock_type, (0.4, 0.5))
            st.markdown(f'<div class="info-text">Recommended powder factor for {rock_type.lower()} rock: {pf_min} - {pf_max} kg/m³</div>', unsafe_allow_html=True)
        
        with tab3:
            burden_formula = st.selectbox("Burden formula", ["Hoek and Bray", "Atlas Copco", "Dick et al", "Adhikari"])
            spacing_pattern = st.selectbox("Spacing pattern", ["Square", "Staggered", "Common"])
            stemming_formula = st.selectbox("Stemming formula", ["Atlas", "Common"])
            sub_drill_formula = st.selectbox("Sub-drill formula", ["Atlas", "Konya", "Hoek & Bray"])
            
        calculate_button = st.button("Calculate Blast Design", type="primary", use_container_width=True)
    
    # Display formulas in expander
    with st.expander("View Formulas Used", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Deck Stemming Formula")
            st.markdown('<div class="formula-text">For Dry Holes: T<sub>d</sub> = 0.5 × D<br>For Wet Holes: T<sub>d</sub> = 1.0 × D</div>', unsafe_allow_html=True)
            
            st.markdown("### Base-Charge Length Formula")
            st.markdown('<div class="formula-text">E<sub>b</sub> = [(0.3 → 0.5) × B] + J</div>', unsafe_allow_html=True)
            
            st.markdown("### Stemming Formulas")
            st.markdown('<div class="formula-text">Atlas: S.L. = (0.7 to 1.3) × B<br>Common: S.L. = (15 to 25) × D</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Powder Factor Formula")
            st.markdown('<div class="formula-text">PF = W<sub>e</sub> / V</div>', unsafe_allow_html=True)
            
            st.markdown("### Burden Formulas")
            st.markdown('<div class="formula-text">Hoek and Bray: B = 45 × D<br>Atlas Copco: B = 19.7 × D<sup>0.99</sup><br>Dick et al: B = (20 to 40) × D<br>Adhikari: B = (0.25 to 0.5) × H</div>', unsafe_allow_html=True)
            
            st.markdown("### Spacing Formulas")
            st.markdown('<div class="formula-text">Square: S = B<br>Staggered: S = 1.15 B<br>Common: S = (1 to 2) × B</div>', unsafe_allow_html=True)
            
            st.markdown("### Sub-Drill Formulas")
            st.markdown('<div class="formula-text">Atlas: Sub-Drill = (0.2 to 0.5) × B<br>Konya: Sub-Drill = 0.3 × B<br>Hoek & Bray: Sub-Drill = (0.2 to 0.3) × B</div>', unsafe_allow_html=True)
    
    # Main content area
    if calculate_button:
        # Calculate parameters
        parameters = calculate_parameters(
            bench_height=bench_height,
            hole_diameter=hole_diameter,
            hole_condition=hole_condition,
            rock_type=rock_type,
            burden_formula=burden_formula,
            spacing_pattern=spacing_pattern,
            stemming_formula=stemming_formula,
            sub_drill_formula=sub_drill_formula,
            explosive_density=explosive_density,
            rock_density=rock_density
        )
        
        # Extract parameters
        burden = parameters['burden']
        spacing = parameters['spacing']
        stemming = parameters['stemming']
        sub_drill = parameters['sub_drill']
        base_charge_length = parameters['base_charge_length']
        column_charge_length = parameters['column_charge_length']
        total_charge = parameters['total_charge']
        powder_factor = parameters['powder_factor']
        total_hole_depth = parameters['total_hole_depth']
        
        # Display results in the main area with two columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<p class="section-header">Calculated Parameters</p>', unsafe_allow_html=True)
            
            # Create a DataFrame for calculated parameters
            results_df = pd.DataFrame({
                'Parameter': ['Burden', 'Spacing', 'Stemming Length', 'Sub-Drill Depth', 'Base Charge Length',
                              'Column Charge Length', 'Total Hole Depth', 'Total Explosive Charge', 'Powder Factor'],
                'Value': [f"{burden:.2f} m", f"{spacing:.2f} m", f"{stemming:.2f} m", f"{sub_drill:.2f} m",
                          f"{base_charge_length:.2f} m", f"{column_charge_length:.2f} m", f"{total_hole_depth:.2f} m",
                          f"{total_charge:.2f} kg", f"{powder_factor:.3f} kg/m³"],
                'Formula Used': [f"{burden_formula}", f"{spacing_pattern} Pattern", f"{stemming_formula}",
                               f"{sub_drill_formula}", "Base Charge Formula", "Calculated", "Sum of Components",
                               "Calculated", "Weight/Volume"]
            })
            
            st.table(results_df)
            
            # Display powder factor status
            pf_min, pf_max = powder_factor_ranges.get(rock_type, (0.4, 0.5))
            if pf_min <= powder_factor <= pf_max:
                st.success(f"✅ Powder factor ({powder_factor:.3f} kg/m³) is within the acceptable range for {rock_type.lower()} rock.")
            else:
                st.warning(f"⚠️ Warning: Powder factor ({powder_factor:.3f} kg/m³) is outside the recommended range for {rock_type.lower()} rock ({pf_min} - {pf_max} kg/m³)!")
                
                if powder_factor < pf_min:
                    st.info("Consider increasing the explosive charge or reducing the spacing/burden.")
                else:
                    st.info("Consider decreasing the explosive charge or increasing the spacing/burden.")
        
        with col2:
            st.markdown('<p class="section-header">Blast Hole Layout</p>', unsafe_allow_html=True)
            visualize_blast_pattern(spacing, burden, spacing_pattern)
            
            # Display blast hole profile
            st.markdown('<p class="section-header">Blast Hole Profile</p>', unsafe_allow_html=True)
            visualize_blast_hole_profile(bench_height, sub_drill, stemming, hole_diameter/1000, 
                                         base_charge_length, column_charge_length)
    else:
        # Display placeholder in main area when app starts
        st.info("👈 Enter parameters in the sidebar and click 'Calculate Blast Design' to see results")
        
        # Display information about the formulas
        st.write("### About the Formulas")
        st.write("""
        This calculator implements industry-standard formulas for blast design from various sources:
        
        - **Burden**: Distance from free face, calculated using formulas from Hoek and Bray, Atlas Copco, Dick et al, or Adhikari
        - **Spacing**: Distance between holes in a row, based on burden and pattern type (Square, Staggered, or Common pattern)
        - **Stemming**: Length of inert material at the top of the hole to confine the explosion
        - **Sub-drill**: Additional drilling below grade to ensure complete breakage
        - **Base Charge**: Higher density explosive at the bottom of the hole
        
        Select your preferred formulas in the sidebar and enter your blast parameters to get started.
        """)

def calculate_parameters(bench_height, hole_diameter, hole_condition, rock_type, 
                         burden_formula, spacing_pattern, stemming_formula, sub_drill_formula,
                         explosive_density, rock_density):
    """Calculate all blast design parameters based on selected formulas"""
    
    # Convert hole diameter to meters for calculations
    hole_diameter_m = hole_diameter / 1000
    
    # Calculate burden based on selected formula
    if burden_formula == "Hoek and Bray":
        burden = 45 * hole_diameter_m
    elif burden_formula == "Atlas Copco":
        burden = 19.7 * (hole_diameter_m ** 0.99)
    elif burden_formula == "Dick et al":
        # Use middle of range (20 to 40) * D
        burden = 30 * hole_diameter_m
    elif burden_formula == "Adhikari":
        # Use middle of range (0.25 to 0.5) * H
        burden = 0.375 * bench_height
    else:
        # Default formula if none selected
        burden = 25 * hole_diameter_m
    
    # Calculate spacing based on selected pattern
    if spacing_pattern == "Square":
        spacing = burden
    elif spacing_pattern == "Staggered":
        spacing = 1.15 * burden
    else:  # Common pattern
        # Use middle of range (1 to 2) * B
        spacing = 1.5 * burden
    
    # Calculate stemming based on selected formula
    if stemming_formula == "Atlas":
        # Use middle of range (0.7 to 1.3) * B
        stemming = 1.0 * burden
    else:  # Common formula
        # Use middle of range (15 to 25) * D
        stemming = 20 * hole_diameter_m
    
    # Calculate sub-drill based on selected formula
    if sub_drill_formula == "Atlas":
        # Use middle of range (0.2 to 0.5) * B
        sub_drill = 0.35 * burden
    elif sub_drill_formula == "Konya":
        sub_drill = 0.3 * burden
    else:  # Hoek & Bray
        # Use middle of range (0.2 to 0.3) * B
        sub_drill = 0.25 * burden
    
    # Calculate base charge length using formula: Eb = [(0.3 → 0.5) × B] + J
    # Use middle of range (0.3 to 0.5) * B
    base_charge_length = 0.4 * burden + sub_drill
    
    # Calculate column charge length (remaining hole length after stemming and base charge)
    total_hole_depth = bench_height + sub_drill
    column_charge_length = total_hole_depth - stemming - base_charge_length
    
    # If column charge length is negative, adjust calculations
    if column_charge_length < 0:
        column_charge_length = 0
        base_charge_length = total_hole_depth - stemming
    
    # Calculate explosive volume and weight
    hole_cross_section = np.pi * (hole_diameter_m/2) ** 2
    base_charge_volume = hole_cross_section * base_charge_length
    column_charge_volume = hole_cross_section * column_charge_length
    
    # Convert explosive density from g/cm³ to kg/m³
    explosive_density_kgm3 = explosive_density * 1000
    
    # Calculate total explosive charge weight
    base_charge = base_charge_volume * explosive_density_kgm3
    column_charge = column_charge_volume * explosive_density_kgm3
    total_charge = base_charge + column_charge
    
    # Calculate volume of rock broken
    rock_volume = burden * spacing * bench_height
    
    # Calculate powder factor (kg of explosive per m³ of rock)
    powder_factor = total_charge / rock_volume
    
    # Return all parameters as a dictionary
    return {
        'burden': burden,
        'spacing': spacing,
        'stemming': stemming,
        'sub_drill': sub_drill,
        'base_charge_length': base_charge_length,
        'column_charge_length': column_charge_length,
        'total_hole_depth': total_hole_depth,
        'total_charge': total_charge,
        'powder_factor': powder_factor
    }

def visualize_blast_pattern(spacing, burden, pattern_type):
    """Create a visual representation of the blast pattern"""
    # Create a blast pattern with 30 holes
    rows = 5
    cols = 6
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create pattern based on type
    for i in range(rows):
        # Add staggered offset for alternate rows if staggered pattern
        offset = (i % 2) * spacing / 2 if pattern_type == "Staggered" else 0
        for j in range(cols):
            ax.scatter(j * spacing + offset, i * burden, color='red', s=100, edgecolor='black')
            ax.text(j * spacing + offset, i * burden, f"{i*cols+j+1}", fontsize=8, 
                   ha='center', va='center', color='white')
    
    # Add pattern type to title
    ax.set_title(f"Blast Hole Layout ({pattern_type} Pattern)")
    ax.set_xlabel("Spacing (m)")
    ax.set_ylabel("Burden (m)")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set axis limits with some padding
    x_max = (cols - 1) * spacing + spacing/2
    if pattern_type == "Staggered":
        x_max += spacing/2  # Add extra space for staggered pattern
    ax.set_xlim(-spacing/2, x_max)
    ax.set_ylim(-burden/2, (rows-0.5) * burden + burden/2)
    
    # Add scale information
    ax.text(0.02, 0.98, f"Spacing: {spacing:.2f} m\nBurden: {burden:.2f} m", 
           transform=ax.transAxes, va='top', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    st.pyplot(fig)

def visualize_blast_hole_profile(bench_height, sub_drill, stemming, hole_diameter, 
                              base_charge_length, column_charge_length):
    """Create a visual representation of the blast hole profile with all components"""
    fig, ax = plt.subplots(figsize=(4, 8))
    
    # Calculate total hole depth
    total_depth = bench_height + sub_drill
    
    # Define hole dimensions for visualization
    scaled_width = 0.5  # Fixed width for visualization
    
    # Draw hole outline
    ax.plot([-scaled_width/2, -scaled_width/2], [0, -total_depth], 'k-', linewidth=2)
    ax.plot([scaled_width/2, scaled_width/2], [0, -total_depth], 'k-', linewidth=2)
    ax.plot([-scaled_width/2, scaled_width/2], [-total_depth, -total_depth], 'k-', linewidth=2)
    
    # Draw ground level
    ax.plot([-scaled_width*2, scaled_width*2], [0, 0], 'k-', linewidth=3)
    
    # Fill stemming section
    ax.fill_between([-scaled_width/2, scaled_width/2], 0, -stemming, color='tan', alpha=0.7)
    
    # Calculate the starting point for base charge (from bottom of hole)
    base_charge_start = total_depth - base_charge_length
    
    # Fill column charge section (if any)
    if column_charge_length > 0:
        ax.fill_between([-scaled_width/2, scaled_width/2], -stemming, -stemming - column_charge_length, color='yellow', alpha=0.7)
    
    # Fill base charge section
    ax.fill_between([-scaled_width/2, scaled_width/2], -base_charge_start, -total_depth, color='orange', alpha=0.7)
    
    # Fill sub-drill section with pattern
    ax.fill_between([-scaled_width/2, scaled_width/2], -bench_height, -total_depth, color='gray', alpha=0.3, hatch='///')
    
    # Add horizontal line at bench height
    ax.plot([-scaled_width*2, scaled_width*2], [-bench_height, -bench_height], 'k--', linewidth=1)
    
    # Add annotations
    ax.annotate('Stemming', xy=(scaled_width/2 + 0.1, -stemming/2), xytext=(scaled_width + 0.1, -stemming/2),
               arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    if column_charge_length > 0:
        ax.annotate('Column\nCharge', xy=(scaled_width/2 + 0.1, -stemming - column_charge_length/2),
                  xytext=(scaled_width + 0.1, -stemming - column_charge_length/2),
                  arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    ax.annotate('Base\nCharge', xy=(scaled_width/2 + 0.1, -(base_charge_start + (total_depth - base_charge_start)/2)),
               xytext=(scaled_width + 0.1, -(base_charge_start + (total_depth - base_charge_start)/2)),
               arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    ax.annotate('Sub-drill', xy=(scaled_width/2 + 0.1, -(bench_height + sub_drill/2)),
               xytext=(scaled_width + 0.1, -(bench_height + sub_drill/2)),
               arrowprops=dict(arrowstyle='->', color='black'), va='center')
    
    ax.annotate('Bench\nHeight', xy=(-scaled_width*1.5, -bench_height/2), ha='center', va='center')
    
    # Add measurements
    ax.text(-scaled_width*1.5, -stemming/2, f"{stemming:.2f} m", va='center', ha='right')
    
    if column_charge_length > 0:
        ax.text(-scaled_width*1.5, -stemming - column_charge_length/2, f"{column_charge_length:.2f} m", va='center', ha='right')
    
    ax.text(-scaled_width*1.5, -(base_charge_start + (total_depth - base_charge_start)/2), 
           f"{base_charge_length:.2f} m", va='center', ha='right')
    
    ax.text(-scaled_width*1.5, -(bench_height + sub_drill/2), f"{sub_drill:.2f} m", va='center', ha='right')
    
    # Add total depth and diameter information
    ax.text(0, -total_depth - 0.5, 
           f"Total depth: {total_depth:.2f} m | Diameter: {hole_diameter*1000:.0f} mm", 
           ha='center')
    
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
