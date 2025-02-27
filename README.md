# Blast Design Calculator for Open Cast Mines

## Overview
The Blast Design Calculator is a Streamlit web application that helps mining engineers design blast patterns for open cast mines. This tool allows users to input various parameters related to bench geometry, explosive charges, and rock properties to calculate optimal blast design parameters and visualize the blast pattern.

## Features
- **Input Parameter Management**: Easily input and adjust all relevant blast design parameters
- **Real-time Calculations**: Instantly calculate spacing, burden, explosive charge, and powder factor
- **Visual Representations**: View both the blast hole layout (staggered pattern) and detailed blast hole profile
- **Rock Type Recommendations**: Get recommended powder factor ranges based on rock strength
- **Validation and Feedback**: Receive warnings and suggestions when parameters are outside recommended ranges

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
   - **Geometry**: Bench height, hole diameter, sub-drill, and stemming
   - **Explosive**: Base charge, column charge, and delay element
   - **Rock Properties**: Rock strength (which determines recommended powder factor range)

4. Click the "Calculate Blast Design" button to view the results

5. Review the calculated parameters and visualizations:
   - Spacing, burden, and powder factor
   - Blast hole layout (staggered pattern)
   - Detailed blast hole profile

## Parameter Guidelines

### Geometry
- **Bench Height**: Typically 5-20m depending on mining method and equipment
- **Hole Diameter**: Commonly ranges from 75-300mm based on production requirements
- **Sub-drill**: Usually 10-30% of burden distance
- **Stemming**: Typically 20-30% of the bench height

### Explosives
- **Base Charge**: Heavier charge at the bottom of the hole
- **Column Charge**: Distributed throughout the main portion of the hole
- **Delay Element**: Timing between hole detonations (ms)

### Rock Properties
- **Hard Rock**: Powder factor range 0.7-0.8 kg/m³
- **Medium Rock**: Powder factor range 0.4-0.5 kg/m³
- **Soft Rock**: Powder factor range 0.25-0.35 kg/m³
- **Very Soft Rock**: Powder factor range 0.15-0.25 kg/m³

## Customization

You can modify the app.py file to adjust:
- Additional rock strength categories
- Different formulas for calculations
- Visual appearance of plots and UI elements
- Input parameter ranges and default values

## Technical Details

The application uses:
- **Streamlit**: For the web interface
- **Matplotlib**: For generating visualizations
- **Pandas**: For data handling and display
- **NumPy**: For numerical calculations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- This tool is designed for educational and planning purposes
- Always consult with a qualified mining engineer before implementing any blast design in practice
