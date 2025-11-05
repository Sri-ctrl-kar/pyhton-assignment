import statistics
import csv # 💡 Correction 1: Import the csv module

# ----------------------------- Task 1 -----------------------------
def print_welcome():
    print("="*60)
    print("🎓 Welcome to the GradeBook Analyzer 🎓")
    print("="*60)
    print("Choose an option to start:")
    print("1. Manual Entry of Student Data")
    print("2. Import from CSV File")
    print("3. Exit")
    print("="*60)


# ----------------------------- Task 2 -----------------------------
def manual_entry():
    marks = {}
    while True:
        try:
            n = int(input("Enter number of students: "))
            if n < 0:
                print("Number of students cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    for _ in range(n):
        name = input("Enter student name: ").strip()
        while not name:
            name = input("Student name cannot be empty. Enter student name: ").strip()
        
        while True:
            try:
                mark = float(input(f"Enter marks for {name}: "))
                if 0 <= mark <= 100:
                    marks[name] = mark
                    break
                else:
                    print("Marks must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number for marks.")
                
    return marks


def csv_import():
    marks = {}
    file_path = input("Enter CSV file path (e.g., data.csv): ").strip()
    try:
        with open(file_path, 'r') as f:
            # 💡 Correction 2: Correctly use csv.reader
            reader = csv.reader(f) 
            try:
                next(reader)  # skip header if present
            except StopIteration:
                pass # Handle empty file case
                
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    try:
                        mark = float(row[1])
                        # Basic mark validation
                        if 0 <= mark <= 100:
                             marks[name] = mark
                        else:
                             print(f"Skipping {name}: Mark ({mark}) is out of 0-100 range.")
                    except ValueError:
                        print(f"Skipping invalid mark entry for {name}")
                elif row:
                    print(f"Skipping incomplete row: {row}")
                    
        print("✅ CSV file loaded successfully!")
        if not marks:
            print("⚠️ The file was loaded, but no valid student data was found.")
            
    except FileNotFoundError:
        print("❌ File not found. Please check the path and try again.")
    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")
        
    return marks


# ----------------------------- Task 3 -----------------------------
def calculate_average(marks_dict):
    if not marks_dict:
        return 0.00
    return round(sum(marks_dict.values()) / len(marks_dict), 2)


def calculate_median(marks_dict):
    if not marks_dict:
        return 0.00
    return round(statistics.median(list(marks_dict.values())), 2)


def find_max_score(marks_dict):
    if not marks_dict:
        return ("N/A", 0.00)
    return max(marks_dict.items(), key=lambda x: x[1])

def find_min_score(marks_dict):
    if not marks_dict:
        return ("N/A", 0.00)
    return min(marks_dict.items(), key=lambda x: x[1])


# ----------------------------- Task 4 -----------------------------
# 💡 Correction 3: Define the missing assign_grades function
def assign_grades(marks_dict):
    """Assigns letter grades based on the 0-100 score scale."""
    grades = {}
    for name, mark in marks_dict.items():
        if 90 <= mark <= 100:
            grades[name] = 'A+'
        elif 80 <= mark < 90:
            grades[name] = 'A'
        elif 70 <= mark < 80:
            grades[name] = 'B+'
        elif 60 <= mark < 70:
            grades[name] = 'B'
        elif 50 <= mark < 60:
            grades[name] = 'C+'
        elif 40 <= mark < 50:
            grades[name] = 'C'
        elif 33 <= mark < 40:
            grades[name] = 'D+'
        else:
            grades[name] = 'F'
    return grades


def grade_distribution(grades_dict):
    # Using a set to ensure all unique grades are counted, not just A, B, C, D, F
    dist = {}
    for g in grades_dict.values():
        dist[g] = dist.get(g, 0) + 1
        
    print("\n📊 Grade Distribution:")
    # Sort for better display
    sorted_dist = sorted(dist.items(), key=lambda item: item[0], reverse=True) 
    for grade, count in sorted_dist:
        print(f"Grade {grade:<2}: {count} student(s)")


# ----------------------------- Task 5 -----------------------------
def pass_fail_lists(marks_dict):
    # Assuming the pass threshold is 40 based on the grading logic
    passed_students = [name for name, m in marks_dict.items() if m >= 40]
    failed_students = [name for name, m in marks_dict.items() if m < 40]
    
    print("\n✅ Passed Students:", passed_students)
    print("❌ Failed Students:", failed_students)
    print(f"Total Passed: {len(passed_students)} | Total Failed: {len(failed_students)}")


# ----------------------------- Task 6 -----------------------------
def print_results_table(marks_dict, grades_dict):
    if not marks_dict:
        print("\nNo data to display in the results table.")
        return
        
    print("\n===============================================")
    print(f"{'Name':<15}{'Marks':<10}{'Grade':<5}")
    print("-----------------------------------------------")
    for name in sorted(marks_dict.keys()): # Sort by name for readability
        mark = marks_dict.get(name, 'N/A')
        grade = grades_dict.get(name, 'N/A')
        print(f"{name:<15}{mark:<10}{grade:<5}")
    print("===============================================\n")


def main():
    while True:
        print_welcome()
        choice = input("Enter your choice (1-3): ").strip()
        marks = {} # Initialize marks here

        if choice == '1':
            marks = manual_entry()
        elif choice == '2':
            marks = csv_import()
        elif choice == '3':
            print("👋 Exiting GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
            continue

        if not marks:
            print("No valid student data was entered or imported for analysis.")
            continue

        # Perform analysis
        avg = calculate_average(marks)
        median = calculate_median(marks)
        top_student = find_max_score(marks)
        low_student = find_min_score(marks)
        grades = assign_grades(marks) # This now works because assign_grades is defined

        # Display results
        print("\n" + "="*40)
        print("         ANALYSIS RESULTS")
        print("="*40)
        
        print(f"📈 Average Marks: {avg}")
        print(f"📉 Median Marks: {median}")
        print(f"🏆 Highest Score: {top_student[0]} ({top_student[1]})")
        print(f"⚠️ Lowest Score: {low_student[0]} ({low_student[1]})")

        # Grade Distribution and Pass/Fail
        grade_distribution(grades)
        pass_fail_lists(marks)
        
        # Print table
        print_results_table(marks, grades)


        again = input("\nWould you like to analyze another dataset? (y/n): ").lower()
        if again != 'y':
            print("✅ Analysis complete. Thank you for using GradeBook Analyzer!")
            break


# Run the program
if __name__ == "__main__":
    # 💡 Correction 4: Removed the standalone 'while True' grade checker block.
    main()