 # Tip Calculator - Because math after a meal is cruel and unusual punishment

meal_cost = float(input("Enter the meal cost: $"))
tip_percentage = float(input("Enter the tip percentage: "))
num_people = int(input("Enter the number of people in the party: "))

tip_amount = meal_cost * (tip_percentage / 100)
total_bill = meal_cost + tip_amount
per_person = total_bill / num_people

print(f"\nTip Amount: ${tip_amount:.2f}")
print(f"Total Bill: ${total_bill:.2f}")
print(f"Per Person: ${per_person:.2f}")