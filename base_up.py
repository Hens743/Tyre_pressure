import streamlit as st

# Load index data from the image
load_index_table = {
    90: 600, 91: 615, 92: 630, 93: 650, 94: 670, 95: 690, 96: 710, 97: 730, 98: 750, 99: 775, 100: 800, 101: 825,
    102: 850, 103: 875, 104: 900, 105: 925, 106: 950, 107: 975, 108: 1000, 109: 1030, 110: 1060, 111: 1090, 112: 1120, 
    113: 1150, 114: 1180, 115: 1215, 116: 1250, 117: 1285, 118: 1320, 119: 1360, 120: 1400, 121: 1450, 122: 1500, 
    123: 1550, 124: 1600, 125: 1650
}

def estimate_tyre_pressure(load_per_tyre, max_load_capacity, reference_pressure):
    """
    Calculate the required tyre pressure for a given load based on reference values.
    
    Parameters:
    - load_per_tyre: The load on each tyre (kg).
    - max_load_capacity: The maximum load capacity of the tyre (kg).
    - reference_pressure: The reference tyre pressure (Bar).
    
    Returns:
    - The required tyre pressure (Bar) for the given load.
    """
    if load_per_tyre > max_load_capacity:
        return None, "The load per tyre exceeds the tyre's maximum load capacity!"
    
    # Calculate the required pressure proportionally
    required_pressure = reference_pressure * (load_per_tyre / max_load_capacity)
    
    return required_pressure, None

# Streamlit app
st.title("Tyre Pressure Estimator with Real Load Index Data")

# User input: Select vehicle type
vehicle_type = st.selectbox("Select Vehicle Type", ["Car", "Trailer/Caravan"])

# Tyre dimension input
tyre_dimension = st.text_input("Enter Tyre Size (e.g., 195/55 R15)", "195/55 R15")

# Tyre load index input
load_index = st.selectbox("Select Tyre Load Index", list(load_index_table.keys()), index=1)

# Maximum load capacity based on selected load index
max_load_capacity = load_index_table[load_index]

# User input for pressure units
pressure_unit = st.selectbox("Select Pressure Unit", ["Bar", "PSI"])

# Conversion factor for PSI to Bar
psi_to_bar = 0.0689476

# Default reference pressures for the given tyre (in Bar)
reference_front_pressure = 2.0  # Front tyre pressure for this vehicle spec (Bar)
reference_rear_pressure = 2.2   # Rear tyre pressure for this vehicle spec (Bar)

# Kerb weight and max weight input
kerb_weight = st.number_input("Kerb Weight (kg)", min_value=1000, max_value=2000, value=1088)
max_weight = st.number_input("Maximum Weight (kg)", min_value=1500, max_value=2000, value=1639)

# Calculate load distribution for front and rear
vehicle_weight = st.slider("Vehicle Weight to Calculate (kg)", min_value=int(kerb_weight), max_value=int(max_weight), value=int(kerb_weight))

if vehicle_type == "Car":
    load_distribution = st.slider("Load Distribution (% on rear axle)", 0, 100, 60)
else:
    load_distribution = st.slider("Load Distribution (% on rear tyres for Trailer/Caravan)", 0, 100, 50)

# Calculate load per tyre
rear_axle_weight = (load_distribution / 100) * vehicle_weight
front_axle_weight = vehicle_weight - rear_axle_weight

if vehicle_type == "Car":
    rear_tyre_load = rear_axle_weight / 2  # Assuming 2 rear tyres
    front_tyre_load = front_axle_weight / 2  # Assuming 2 front tyres
else:
    rear_tyre_load = rear_axle_weight / 2  # Assuming 2 rear tyres (typical for trailers)
    front_tyre_load = None  # Trailers/caravans usually don't have front axle tyres

# Display calculated loads
st.subheader("Tyre Loads")
st.write(f"Rear Tyre Load: {rear_tyre_load:.2f} kg per tyre")

if vehicle_type == "Car":
    st.write(f"Front Tyre Load: {front_tyre_load:.2f} kg per tyre")

# Estimate pressures based on reference values (2.0 bar front, 2.2 bar rear for this spec)
st.subheader("Estimated Tyre Pressures")

# Calculate rear tyre pressure
rear_tyre_pressure, rear_error = estimate_tyre_pressure(rear_tyre_load, max_load_capacity, reference_rear_pressure)

# Calculate front tyre pressure if it's a car
if vehicle_type == "Car":
    front_tyre_pressure, front_error = estimate_tyre_pressure(front_tyre_load, max_load_capacity, reference_front_pressure)

# Convert calculated pressures to the selected unit (if PSI)
if pressure_unit == "PSI":
    if rear_tyre_pressure:
        rear_tyre_pressure = rear_tyre_pressure / psi_to_bar
    if vehicle_type == "Car" and front_tyre_pressure:
        front_tyre_pressure = front_tyre_pressure / psi_to_bar

# Display rear tyre pressure
if rear_error:
    st.error(rear_error)
else:
    if pressure_unit == "PSI":
        st.write(f"Estimated Rear Tyre Pressure: {rear_tyre_pressure:.2f} PSI")
    else:
        st.write(f"Estimated Rear Tyre Pressure: {rear_tyre_pressure:.2f} Bar")

# Display front tyre pressure for cars
if vehicle_type == "Car":
    if front_error:
        st.error(front_error)
    else:
        if pressure_unit == "PSI":
            st.write(f"Estimated Front Tyre Pressure: {front_tyre_pressure:.2f} PSI")
        else:
            st.write(f"Estimated Front Tyre Pressure: {front_tyre_pressure:.2f} Bar")
