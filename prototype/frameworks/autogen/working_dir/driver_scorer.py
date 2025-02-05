# filename: driver_scorer.py
# Calculate the score for the driver
driving_experience = 5 * 5  # 5 points for each year of driving experience
accident_penalty = -5  # -5 points for each accident in the last 3 years
ticket_penalty = -3  # -3 points for each ticket in the last 3 years

accidents = 1
tickets = 1

score = driving_experience + (accident_penalty * accidents) + (ticket_penalty * tickets)
print("The driver's score is:", score)
