import streamlit as st

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
st.title("Tyre Pressure Estimator")

# User input
st.header("Enter Tyre Specifications and Vehicle Details")

tyre_load_index = st.number_input("Maximum Load Capacity per Tyre (kg)", min_value=100, max_value=2000, value=615)
max_pressure = st.number_input("Maximum Pressure of Tyre (PSI)", min_value=20, max_value=100, value=44)
vehicle_weight = st.number_input("Total Vehicle Weight (kg)", min_value=500, max_value=10000, value=4000)
load_distribution = st.slider("Load Distribution (% on rear axle)", 0, 100, 60)

# Calculate load per tyre
rear_axle_weight = (load_distribution / 100) * vehicle_weight
front_axle_weight = vehicle_weight - rear_axle_weight

rear_tyre_load = rear_axle_weight / 2  # Assuming 2 rear tyres
front_tyre_load = front_axle_weight / 2  # Assuming 2 front tyres

# Display calculated loads
st.subheader("Tyre Loads")
st.write(f"Rear Tyre Load: {rear_tyre_load:.2f} kg per tyre")
st.write(f"Front Tyre Load: {front_tyre_load:.2f} kg per tyre")

# Estimate pressures
st.subheader("Estimated Tyre Pressures")

rear_tyre_pressure, rear_error = estimate_tyre_pressure(rear_tyre_load, tyre_load_index, max_pressure)
front_tyre_pressure, front_error = estimate_tyre_pressure(front_tyre_load, tyre_load_index, max_pressure)

if rear_error:
    st.error(rear_error)
else:
    st.write(f"Estimated Rear Tyre Pressure: {rear_tyre_pressure:.2f} PSI")

if front_error:
    st.error(front_error)
else:
    st.write(f"Estimated Front Tyre Pressure: {front_tyre_pressure:.2f} PSI")

