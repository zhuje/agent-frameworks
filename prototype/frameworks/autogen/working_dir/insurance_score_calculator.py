# filename: insurance_score_calculator.py
def calculate_insurance_score(driving_record, credit_history, other_factors):
    # Use the provided algorithm to calculate the insurance score
    # Replace the following line with the actual algorithm
    insurance_score = max(1, min(100, 100 - (driving_record * 10) + (credit_history * 5) + other_factors))
    return insurance_score

# Example usage
driving_record = 0  # Assuming 0 accidents
credit_history = 80  # Assuming a credit score of 80
other_factors = 10  # Assuming other factors contribute 10 points
score = calculate_insurance_score(driving_record, credit_history, other_factors)
print("The insurance score is:", score)
