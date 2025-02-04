import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_insurance_data(num_records=1000):
    np.random.seed(42)
    
    # Generate basic demographic data
    ages = np.random.normal(45, 15, num_records).astype(int)
    ages = np.clip(ages, 18, 85)
    
    genders = np.random.choice(['M', 'F'], num_records)
    
    # Generate health-related data
    bmi_values = np.random.normal(26, 4, num_records)
    bmi_values = np.clip(bmi_values, 16, 45)
    
    smoker = np.random.choice(['Yes', 'No'], num_records, p=[0.2, 0.8])
    
    # Generate lifestyle data
    exercise_frequency = np.random.choice(
        ['Never', 'Occasional', 'Regular', 'Daily'],
        num_records,
        p=[0.2, 0.3, 0.3, 0.2]
    )
    
    occupation_risk = np.random.choice(
        ['Low', 'Medium', 'High'],
        num_records,
        p=[0.7, 0.2, 0.1]
    )
    
    # Generate medical history
    chronic_conditions = np.random.choice(
        ['None', 'Diabetes', 'Hypertension', 'Multiple'],
        num_records,
        p=[0.6, 0.15, 0.15, 0.1]
    )
    
    family_history = np.random.choice(
        ['None', 'Cancer', 'Heart Disease', 'Multiple'],
        num_records,
        p=[0.5, 0.2, 0.2, 0.1]
    )
    
    # Generate financial indicators
    income_brackets = np.random.choice(
        ['0-30k', '30k-60k', '60k-100k', '100k+'],
        num_records,
        p=[0.2, 0.3, 0.3, 0.2]
    )
    
    credit_score = np.random.normal(700, 100, num_records).astype(int)
    credit_score = np.clip(credit_score, 300, 850)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Age': ages,
        'Gender': genders,
        'BMI': bmi_values.round(1),
        'Smoker': smoker,
        'Exercise_Frequency': exercise_frequency,
        'Occupation_Risk': occupation_risk,
        'Chronic_Conditions': chronic_conditions,
        'Family_History': family_history,
        'Income_Bracket': income_brackets,
        'Credit_Score': credit_score
    })
    
    # Add a unique identifier
    data['InsuranceID'] = [f'INS{str(i).zfill(6)}' for i in range(num_records)]
    
    # Calculate a baseline insurance score (simplified version)
    data['BaselineScore'] = (
        100 - data['Age'] * 0.3 +
        (data['Gender'] == 'F') * 5 -
        (data['BMI'] - 25).abs() * 2 -
        (data['Smoker'] == 'Yes') * 20 +
        pd.Categorical(data['Exercise_Frequency'], 
                      categories=['Never', 'Occasional', 'Regular', 'Daily'],
                      ordered=True).codes * 5 -
        pd.Categorical(data['Occupation_Risk'],
                      categories=['Low', 'Medium', 'High'],
                      ordered=True).codes * 10 -
        pd.Categorical(data['Chronic_Conditions'],
                      categories=['None', 'Diabetes', 'Hypertension', 'Multiple'],
                      ordered=True).codes * 8 -
        pd.Categorical(data['Family_History'],
                      categories=['None', 'Cancer', 'Heart Disease', 'Multiple'],
                      ordered=True).codes * 5 +
        (data['Credit_Score'] - 700) * 0.05
    )
    
    # Normalize the score between 0 and 100
    data['BaselineScore'] = (data['BaselineScore'] - data['BaselineScore'].min()) / \
                           (data['BaselineScore'].max() - data['BaselineScore'].min()) * 100
    
    return data

if __name__ == "__main__":
    # Generate sample data
    insurance_data = generate_insurance_data(1000)
    
    # Save to CSV
    insurance_data.to_csv('insurance_applicants.csv', index=False)
    print("Generated insurance data saved to 'insurance_applicants.csv'")