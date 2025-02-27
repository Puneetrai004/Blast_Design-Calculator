# Blast Design Calculator for Open Cast Mines

## Overview
The Blast Design Calculator is a Streamlit web application that helps mining engineers design blast patterns for open cast mines. This tool implements industry-standard formulas from sources such as Atlas Copco, Konya, Hoek & Bray, and others to calculate optimal blast design parameters and visualize the blast pattern.

## Features
- **Multiple Formula Selection**: Choose from various industry-standard formulas for burden, spacing, stemming, and sub-drill calculations
- **Comprehensive Inputs**: Input parameters for hole geometry, rock properties, and explosive characteristics
- **Real-time Calculations**: Instantly calculate all blast design parameters based on selected formulas
- **Visual Representations**: View both the blast hole layout (square/staggered pattern) and detailed blast hole profile
- **Rock Type Recommendations**: Get recommended powder factor ranges based on rock strength
- **Validation and Feedback**: Receive warnings and suggestions when parameters are outside recommended ranges

## Implemented Formulas

### Burden Calculation
- **Hoek and Bray**: B = 45 × D
- **Atlas Copco**: B = 19.7 × D^0.99
- **Dick et al**: B = (20 to 40) × D
- **Adhikari**: B = (0.25 to 0.5) × H

Where:
- B = Burden (m)
- D = Hole diameter (m)
- H = Bench height (m)

### Spacing Calculation
- **Square Pattern**: S = B
- **Staggered Pattern**: S = 1.15 × B
- **Common Pattern**: S = (1 to 2) × B

Where:
- S = Spacing (m)
- B = Burden (m)

### Stemming Length
- **Atlas Formula**: S.L. = (0.7 to 1.3) × B
- **Common Formula**: S.L. = (15 to 25) × D

Where:
- S.L. = Stemming Length (m)
- B = Burden (m)
- D = Hole diameter (m)

### Sub-Drill Calculation
- **Atlas Formula**: Sub-Drill = (0.2 to 0.5) × B
- **Konya Formula**: Sub-Drill = 0.3 × B
- **Hoek & Bray Formula**: Sub-Drill = (0.2 to 0.3) × B

Where:
- B = Burden (m)

### Base-Charge Length Formula
- E_b = [(0.3 → 0.5) × B] + J

Where:
- E_b = Length of base charge (m)
- B = Burden (m)
- J = Sub-drilling depth (m)

### Powder Factor Formula
- PF = W_e / V

Where:
- PF = Powder factor (kg/m³)
- W_e = Total weight of explosives used (kg)
- V = Total volume of rock generated (m³)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. Clone this repository or download the source code:
   ```
   git clone https://github.com/yourusername/blast-design-calculator.git
   cd blast-design-calculator
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in your terminal (typically http://localhost:8501)

3. Use the sidebar to input your blast design parameters:
   - **Geometry**: Bench height, hole diameter, hole condition (dry/wet)
   - **Rock & Explosive**: Rock strength, explosive density, rock density
   - **Formula Selection**: Choose specific formulas for burden, spacing, stemming, and sub-drill

4. Click the "Calculate Blast Design" button to view the results

5. Review the calculated parameters and visualizations:
   - Burden, spacing, stemming length, sub-drill depth
   - Base charge and column charge lengths
   - Powder factor
   - Blast hole layout (pattern visualization)
   - Detailed blast hole profile showing all components

## Parameter Guidelines

### Geometry
- **Bench Height**: Typically 5-20m depending on mining method and equipment
- **Hole Diameter**: Commonly ranges from 75-300mm based on production requirements

### Rock Properties
- **Hard Rock**: Powder factor range 0.7-0.8 kg/m³
- **Medium Rock**: Powder factor range 0.4-0.5 kg/m³
- **Soft Rock**: Powder factor range 0.25-0.35 kg/m³
- **Very Soft Rock**: Powder factor range 0.15-0.25 kg/m³

### Explosive Properties
- **Explosive Density**: Typically 0.8-1.6 g/cm³ depending on explosive type

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References

The formulas implemented in this application are based on established blast design methodologies from the following sources:
- Atlas Copco Rock Drilling Methods
- Konya, C.J. and Walter, E.J., Surface Blast Design
- Hoek, E. and Bray, J.W., Rock Slope Engineering
- Dick, R.A., Fletcher, L.R., and D'Andrea, D.V., Explosives and Blasting Procedures Manual
- Adhikari, G.R., Studies on Flyrock at Limestone Quarries

## Disclaimer

This tool is designed for educational and planning purposes only. Always consult with a qualified mining engineer before implementing any blast design in practice. The application developers assume no liability for any damages resulting from use of this software.
