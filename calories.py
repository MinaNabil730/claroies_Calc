import streamlit as st
import plotly.graph_objects as go

# Title of the app
st.title("Interactive Calorie & Macronutrient Calculator")

# Sidebar for user input
st.sidebar.header("User Information")

# User inputs
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, value=70.0, format="%.1f")
height = st.sidebar.number_input("Height (cm)", min_value=0, max_value=250, value=170)
gender = st.sidebar.radio("Gender", ("Male", "Female"))
activity_level = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"])

# BMR Calculation
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# TDEE Calculation
def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Extra active": 1.9
    }
    return bmr * activity_multipliers[activity_level]

# Macronutrient Distribution
def calculate_macros(tdee):
    protein = tdee * 0.3 / 4
    fats = tdee * 0.25 / 9
    carbs = tdee * 0.45 / 4
    return protein, fats, carbs

# Perform calculations
bmr = calculate_bmr(weight, height, age, gender)
tdee = calculate_tdee(bmr, activity_level)
protein, fats, carbs = calculate_macros(tdee)

# Display results
st.header("Your Daily Caloric Needs")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Basal Metabolic Rate (BMR)")
    st.write(f"{bmr:.2f} calories/day")
    
    st.subheader("Total Daily Energy Expenditure (TDEE)")
    st.write(f"{tdee:.2f} calories/day")

with col2:
    st.subheader("Macronutrient Distribution")
    st.write(f"Protein: {protein:.2f} g/day")
    st.write(f"Fats: {fats:.2f} g/day")
    st.write(f"Carbohydrates: {carbs:.2f} g/day")

# Interactive Visualization: Macronutrient Distribution Chart with Plotly
st.subheader("Interactive Macronutrient Distribution Chart")

# Calculate the total calories from macronutrients
total_protein_calories = protein * 4
total_fats_calories = fats * 9
total_carbs_calories = carbs * 4
total_calories = total_protein_calories + total_fats_calories + total_carbs_calories

# Calculate the percentages
percent_protein = (total_protein_calories / total_calories) * 100
percent_fats = (total_fats_calories / total_calories) * 100
percent_carbs = (total_carbs_calories / total_calories) * 100

labels = ['Protein', 'Fats', 'Carbohydrates']
values = [percent_protein, percent_fats, percent_carbs]
colors = ['#ff9999', '#66b3ff', '#99ff99']

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, textinfo='label+percent', marker=dict(colors=colors))])
fig.update_layout(title_text='Macronutrient Distribution')

st.plotly_chart(fig)

# Weight Goal Progress and Suggestions
st.subheader("Your Weight Goal Progress")

# Dynamic input for weight goal
weight_goal = st.slider("Select your goal weight (kg):", min_value=float(weight - 20), max_value=float(weight + 20), value=float(weight), step=0.1)
weight_change_needed = weight - weight_goal

# Calculate weekly caloric adjustment
calories_per_kg = 7700
calories_needed = calories_per_kg * weight_change_needed

# For a more realistic approach, we calculate weekly adjustments
days_to_reach_goal = st.slider("Time to reach goal (weeks):", min_value=1, max_value=52, value=8)
daily_caloric_change = calories_needed / (days_to_reach_goal * 7)  # Divide by total days

st.write(f"To reach your goal weight of {weight_goal:.1f} kg in {days_to_reach_goal} weeks, you need to {'increase' if weight_change_needed < 0 else 'decrease'} your daily caloric intake by approximately {abs(daily_caloric_change):.2f} calories.")

# Final advice
st.write("Adjust your daily caloric intake and macronutrient balance based on your goals to stay on track.")
