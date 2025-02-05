import streamlit as st
import numpy as np
import pandas as pd

# Size chart as DataFrame
size_chart = pd.DataFrame({
    'Size': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
    'Chest': [(31, 34), (35, 37), (38, 40), (42, 45), (46, 48), (49, 52)],
    'Waist': [(26, 28), (28, 30), (31, 34), (35, 38), (40, 42), (43, 45)],
    'Shoulder_Width': [17.5, 19, 21, 22.5, 24.5, 26.5],
    'Sleeve_Length': [8.5, 9, 10, 10.5, 11, 11.5],
    'Body_Length': [28, 29, 30, 31, 32, 33],
    'Neck': [(14, 14.5), (14, 14.5), (15, 15.5), (16, 16.5), (17, 17.5), (18, 18.5)]
})

# Function to calculate midpoints for range values


def midpoint(range_tuple):
    return (range_tuple[0] + range_tuple[1]) / 2

# Function to predict missing measurements


def predict_measurements(chest):
    shoulder_width = 0.47 * chest  # Adjusted factor for better accuracy
    sleeve_length = 0.32 * chest
    body_length = 25 + (chest / 11)
    neck = 0.42 * chest
    return shoulder_width, sleeve_length, body_length, neck

# Function to find the closest size based on Euclidean distance


def find_closest_size(chest, waist, shoulder_width):
    min_distance = float('inf')
    closest_size = None

    for _, row in size_chart.iterrows():
        chest_mid = midpoint(row['Chest'])
        waist_mid = midpoint(row['Waist'])
        shoulder_width_chart = row['Shoulder_Width']

        # Euclidean distance formula
        distance = np.sqrt(
            (chest - chest_mid) ** 2 +
            (waist - waist_mid) ** 2 +
            (shoulder_width - shoulder_width_chart) ** 2
        )
        if distance < min_distance:
            min_distance = distance
            closest_size = row['Size']

    return closest_size


# Streamlit UI
st.title("👕 Clothing Size Recommender")
st.write("Enter your body measurements to get a recommended clothing size.")

# Sidebar user input
st.sidebar.header("📏 Enter Your Measurements")

# Chest Input
user_chest = st.sidebar.slider(
    "Chest (in inches)", min_value=30, max_value=55, value=42
)

# Waist Input
user_waist = st.sidebar.slider(
    "Waist (in inches)", min_value=25, max_value=50, value=38
)

# Optional input for Shoulder Width
user_shoulder_width = st.sidebar.text_input(
    "Shoulder Width (in inches) [Optional]",
    value=""
)

# Predict missing measurements
if not user_shoulder_width.strip():
    predicted_measurements = predict_measurements(user_chest)
    user_shoulder_width, sleeve_length, body_length, neck = predicted_measurements
    predicted = True
else:
    try:
        user_shoulder_width = float(user_shoulder_width)
        predicted = False
        _, sleeve_length, body_length, neck = predict_measurements(user_chest)
    except ValueError:
        st.sidebar.error("❌ Please enter a valid number for Shoulder Width.")
        st.stop()

# Find recommended size
recommended_size = find_closest_size(
    user_chest, user_waist, user_shoulder_width)

# Display Results
st.subheader("📏 Recommended Size")
st.markdown(f"### 🏷️ Your recommended size is: **{recommended_size}**")

# Show predicted measurements
st.subheader("📊 Predicted Measurements")
predicted_df = pd.DataFrame({
    "Measurement": ["Shoulder Width", "Sleeve Length", "Body Length", "Neck"],
    "Value (inches)": [user_shoulder_width, sleeve_length, body_length, neck],
    "Predicted?": ["Yes" if predicted else "No"] * 4
})
st.table(predicted_df)

# Show Size Chart
st.subheader("📜 Size Chart Reference")
st.dataframe(size_chart)

st.markdown(
    "🔹 Adjust your measurements in the sidebar to get real-time recommendations.")
