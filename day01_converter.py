 # Unit Converter - For when Google is too far away

print("What would you like to convert?")
print("1. Temperature (C/F)")
print("2. Distance (km/miles)")
print("3. Weight (kg/lbs)")

choice = input("\nEnter your choice (1/2/3): ")

if choice == "1":
    direction = input("Convert to (C)elsius or (F)ahrenheit? ").upper()
    value = float(input("Enter the temperature: "))
    if direction == "F":
        result = (value * 9/5) + 32
        print(f"\n{value}°C = {result:.2f}°F")
    elif direction == "C":
        result = (value - 32) * 5/9
        print(f"\n{value}°F = {result:.2f}°C")
    else:
        print("Invalid choice!")

elif choice == "2":
    direction = input("Convert to (K)m or (M)iles? ").upper()
    value = float(input("Enter the distance: "))
    if direction == "M":
        result = value * 0.621371
        print(f"\n{value} km = {result:.2f} miles")
    elif direction == "K":
        result = value * 1.60934
        print(f"\n{value} miles = {result:.2f} km")
    else:
        print("Invalid choice!")

elif choice == "3":
    direction = input("Convert to (K)g or (L)bs? ").upper()
    value = float(input("Enter the weight: "))
    if direction == "L":
        result = value * 2.20462
        print(f"\n{value} kg = {result:.2f} lbs")
    elif direction == "K":
        result = value * 0.453592
        print(f"\n{value} lbs = {result:.2f} kg")
    else:
        print("Invalid choice!")

else:
    print("Invalid choice!")