# Section 1: Who are you?
name     = input("Enter your name: ")
city     = input("Enter your city: ")
age      = int(input("Enter your age: "))
fav_language = input("Enter favorite prog language: ")
target_field = input("Enter target field in AI: ")
# Section 2: Course Info
course     = "AI & Python Masterclass"
day_number = 1
total_days = 90
committed  = True

# Section 3: Calculations
days_done      = day_number
days_remaining = total_days - days_done
pct_complete   = (days_done / total_days) * 100
age_at_finish  = age # same year - course is 3 months

# Section 4: Output
print()
print("=" * 50)
print(f" {course}")
print("=" * 50)
print(f"  Student:      {name}")
print(f"  City:         {city}")
print(f"  Age:          {age}")
print(f"  Favorite Language {fav_language}")
print(f" Target Field  {target_field}")
print(f"  Day:          {day_number} of {total_days}")
print(f"  Progress:     {pct_complete:.2f}%")
print(f"  Days remaining: {days_remaining}")
print(f"  Committed:    {committed}")
print(f"=" * 50)
print(f"  Let's go, {name}. The machine is waiting.")
print("=" * 50)

