 # BMI Calculator - The Mirror's Brutally Honest Friend

weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))

bmi = weight / (height ** 2)

print(f"\nYour BMI is: {round(bmi, 2)}")

if bmi < 18.5:
    print("Category: Underweight")
elif bmi <= 24.9:
    print("Category: Normal")
elif bmi <= 29.9:
    print("Category: Overweight")
else:
    print("Category: Obese")