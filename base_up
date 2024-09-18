import streamlit as st

# Simulated database of tyre characteristics (for simplicity)
tyre_data = {
    "205/55 R16": {"load_index": 91, "max_pressure_psi": 44, "max_pressure_bar": 3.0},
    "225/45 R17": {"load_index": 94, "max_pressure_psi": 50, "max_pressure_bar": 3.5},
    "195/65 R15": {"load_index": 89, "max_pressure_psi": 40, "max_pressure_bar": 2.8},
}

def estimate_tyre_pressure(load_per_tyre, max_load_capacity, max_pressure):
    """
    Calculate the required tyre pressure for a given load.
    
    Parameters:
    - load_per_tyre: The load on each tyre (kg).
    - max_load_capacity: The maximum load capacity of the tyre (kg) based on the tyre's load index.
    - max_pressure: The maximum pressure of the tyre (PSI).
    
    Returns:
    - The required tyre pressure (PSI) for the given load.
    """
    if load_per_tyre > max_load_capacity:
        return None, "The load per tyre exceeds the tyre's maximum load capacity!"
    
    # Calculate the required pressure proportionally
    required_pressure = max_pressure * (load_per_tyre / max_load_capacity)
    
    return required_pressure, None

# Streamlit app
st.title("Tyre Pressure Estimator for Car or Trailer")

# User input: Select vehicle type
vehicle_type = st.selectbox("Select Vehicle Type", ["Car", "Trailer/Caravan"])

# Tyre dimension input
tyre_dimension = st.text_input("Enter Tyre Size (e.g., 205/55 R16)", "205/55 R16")

# Fetch default values based on tyre dimension
if tyre_dimension in tyre_data:
    tyre_info = tyre_data[tyre_dimension]
    default_load_index = tyre_info["load_index"]
    default_max_pressure_psi = tyre_info["max_pressure_psi"]
    default_max_pressure_bar = tyre_info["max_pressure_bar"]
    st.write(f"Default Load Index: {default_load_index}, Max Pressure: {default_max_pressure_psi} PSI / {default_max_pressure_bar} Bar")
else:
    st.write("Tyre size not found, please enter details manually.")
    default_load_index = 91  # Placeholder if not found
    default_max_pressure_psi = 44
    default_max_pressure_bar = 3.0

# User input for pressure units
pressure_unit = st.selectbox("Select Pressure Unit", ["PSI", "Bar"])

# Conversion factor for PSI to Bar
psi_to_bar = 0.0689476

# User input for load index and max pressure, with defaults from tyre data
tyre_load_index = st.number_input("Maximum Load Capacity per Tyre (Load Index)", min_value=50, max_value=150, value=default_load_index)

if pressure_unit == "PSI":
    max_pressure = st.number_input("Maximum Pressure of Tyre (PSI)", min_value=20, max_value=100, value=default_max_pressure_psi)
else:
    max_pressure = st.number_input("Maximum Pressure of Tyre (Bar)", min_value=1.5, max_value=7.0, value=default_max_pressure_bar)
    max_pressure = max_pressure / psi_to_bar  # Convert Bar to PSI internally for calculations

# User input for vehicle weight
vehicle_weight = st.number_input("Total Vehicle Weight (kg)", min_value=500, max_value=10000, value=1400)

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

# Estimate pressures
st.subheader("Estimated Tyre Pressures")

rear_tyre_pressure, rear_error = estimate_tyre_pressure(rear_tyre_load, tyre_load_index * 10, max_pressure)  # Assume load index * 10 = max load capacity in kg
if vehicle_type == "Car":
    front_tyre_pressure, front_error = estimate_tyre_pressure(front_tyre_load, tyre_load_index * 10, max_pressure)

# Convert calculated pressures to the selected unit (if Bar)
if pressure_unit == "Bar":
    if rear_tyre_pressure:
        rear_tyre_pressure = rear_tyre_pressure * psi_to_bar
    if vehicle_type == "Car" and front_tyre_pressure:
        front_tyre_pressure = front_tyre_pressure * psi_to_bar

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
