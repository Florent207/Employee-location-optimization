import pandas as pd
import random
import matplotlib.pyplot as plt

class Employee:
    def __init__(self, id, name, off_days):
        self.id = id
        self.name = name
        self.off_days = off_days
        self.scenarios = []

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

    def __str__(self):
        return f"Employee {self.id}: {self.scenarios}"

# Name of employees and their off days
employees_data = [
    {"id": 1, "name": "Joe", "off_days": [3]},
    {"id": 2, "name": "Fred", "off_days": []},
    {"id": 3, "name": "Sarah", "off_days": []},
    {"id": 4, "name": "Mike", "off_days": []},
    {"id": 5, "name": "Deby", "off_days": []},
    {"id": 6, "name": "June", "off_days": []},
    {"id": 7, "name": "Eve", "off_days": [1]},
    {"id": 8, "name": "Thomas", "off_days": []},
    {"id": 9, "name": "Robert", "off_days": []},
    {"id": 10, "name": "Helene", "off_days": [4]},
    {"id": 11, "name": "Steve", "off_days": [1]},
    {"id": 12, "name": "Alex", "off_days": []},
]

# Creating Employee objects from data
employees = []

for employee_data in employees_data:
    employee = Employee(employee_data["id"], employee_data["name"], employee_data["off_days"])
    employees.append(employee)

# Limit the number of scenarios
max_scenarios = 1

# Scenario generation for each employee
for employee in employees:
    for _ in range(max_scenarios):
        scenario = []
        telework_count = 0
        coworking_count = 0
        day_order = [1, 2, 3, 4, 5]
        random.shuffle(day_order)
        for day in day_order:
            if day in employee.off_days:
                choice = 'off'
            elif telework_count < 1 and day not in employee.off_days:
                choice = 'Telework'
                telework_count += 1
            elif coworking_count < 1 and day not in employee.off_days:
                choice = 'Coworking'
                coworking_count += 1
            else:
                choice = 'Desk'
            scenario.append((day, choice))
        employee.add_scenario(scenario)

# Creating a DataFrame
data = []

for employee in employees:
    for scenario in employee.scenarios:
        for day, assignment in scenario:
            data.append({"Employee": employee.name, "Day": day, "Assignment": assignment})

df = pd.DataFrame(data)

# Creating a dict with scenarios
scenario_data = {i: [] for i in range(max_scenarios)}

for employee in employees:
    for scenario_index, scenario in enumerate(employee.scenarios):
        scenario_row = {"Employee": employee.name}
        for day, assignment in scenario:
            scenario_row[f"Day_{day}"] = assignment
        scenario_data[scenario_index].append(scenario_row)

# Creating DataFrame per scenario
scenario_dfs = []
for scenario_index, scenario_rows in scenario_data.items():
    scenario_df = pd.DataFrame(scenario_rows)
    scenario_dfs.append(scenario_df)

# Number of days present per employee
desk_counts = {employee.name: 0 for employee in employees}

for employee in employees:
    for scenario in employee.scenarios:
        for _, assignment in scenario:
            if assignment == 'Desk':
                desk_counts[employee.name] += 1

for employee_name, desk_count in desk_counts.items():
    print(f"{employee_name} - Number of Desk: {desk_count}")

for scenario_index, scenario_df in enumerate(scenario_dfs):
    print(f"Scenario {scenario_index + 1}:\n{scenario_df}\n")

# Calculate the number of employees in each category per day
daily_assignment_counts = df.groupby(['Day', 'Assignment'])['Employee'].count().unstack(fill_value=0)

# Create bar graphs
plt.figure(figsize=(10, 6))
width = 0.35
days = daily_assignment_counts.index
telework_counts = daily_assignment_counts['Telework']
coworking_counts = daily_assignment_counts['Coworking']
off_counts = daily_assignment_counts['off']
desk_counts = daily_assignment_counts['Desk']

p1 = plt.bar(days, desk_counts, width, color='green', label='Desk')
p2 = plt.bar(days, telework_counts, width, color='blue', bottom=desk_counts, label='Telework')
p3 = plt.bar(days, coworking_counts, width, color='orange', bottom=desk_counts + telework_counts, label='Coworking')
p4 = plt.bar(days, off_counts, width, color='red', bottom=desk_counts + telework_counts + coworking_counts, label='Off')

plt.xlabel('Day')
plt.ylabel('Number of Employees')
plt.title('Employee Assignment by Day')
plt.xticks(days)
plt.legend()
plt.tight_layout()

plt.show()