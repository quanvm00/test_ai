from pulp import *

# Sets
Vehicles = ['T1', 'T2', 'T3', 'T4', 'T5']
Customers = [1, 2, 3, 4, 5]
CustomersAndDepot = [0, 1, 2, 3, 4, 5, 6]
list_a = [0, 6]
list_b = [0, 1, 2, 3, 4, 5, 6]

# Parameter
CapacityTruck = 1000
VolumeTruck = 5.6

Demand = {1: 492, 2: 915, 3: 420, 4: 480, 5: 342}
Volume = {1: 1.2, 2: 3, 3: 1.5, 4: 0.75, 5: 0.96}

ServiceTime = {0: 0, 1: 30, 2: 30, 3: 30, 4: 30, 5: 30, 6: 0}
LBTW = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
UBTW = {0: 420, 1: 120, 2: 120, 3: 120, 4: 120, 5: 120, 6: 420}

Distance = {0: {0: 0, 1: 14.1, 2: 10.3, 3: 9.5, 4: 11.3, 5: 17.8, 6: 0},
            1: {0: 14.1, 1: 0, 2: 16.6, 3: 11.3, 4: 10.4, 5: 21.2, 6: 14.1},
            2: {0: 10.3, 1: 16.6, 2: 0, 3: 7.9, 4: 10.4, 5: 20.4, 6: 10.3},
            3: {0: 9.5, 1: 11.3, 2: 7.9, 3: 0, 4: 3.2, 5: 9, 6: 9.5},
            4: {0: 11.3, 1: 10.4, 2: 10.4, 3: 3.2, 4: 0, 5: 12.3, 6: 11.3},
            5: {0: 17.8, 1: 21.2, 2: 20.4, 3: 9, 4: 12.3, 5: 0, 6: 17.8},
            6: {0: 0, 1: 14.1, 2: 10.3, 3: 9.5, 4: 11.3, 5: 17.8, 6: 0}}

# set problem variable
prob = LpProblem("VRPTW", LpMinimize)
# route = [(i, j) for i in CustomersAndDepot for j in CustomersAndDepot]

# Dicision Vartiable
Time = LpVariable.dicts("TimeBetweenij",
                        (CustomersAndDepot, CustomersAndDepot),
                        0)
# maxTimeSpent = LpVariable.dicts("maxTimeSpentBetween2Customers",(CustomersAndDepot, CustomersAndDepot),
# 0)

x_vars = LpVariable.dicts("Service",
                          (Vehicles, CustomersAndDepot, CustomersAndDepot),
                          0, 1, LpBinary)
s_vars = LpVariable.dicts("StartToService",
                          (Vehicles, CustomersAndDepot),
                          0)

#
for i in CustomersAndDepot:
    for j in CustomersAndDepot:
        if i == j:
            Distance[i][j] = 0
            Time[i][j] = 0
        else:
            Distance[i][j] = Distance[i][j]
            Time[i][j] = (Distance[i][j] / 30) * 60 + ServiceTime[i]

listTime = []
for a in list_a:
    for b in list_b:
        Time[a][b] = (Distance[a][b] / 30) * 60 + ServiceTime[a]
        print("from ", a, " to ", b, ":", Time[a][b])
        listTime.append(Time[a][b])

maxTimeTravel = max(listTime)
maxTimeSpent = 420 + maxTimeTravel - 0
print("Max Time Spent Between Two Customer: ", maxTimeSpent)
print("Max Time Spent Travel: ", maxTimeTravel)
# Objective Function
prob += lpSum(Distance[i][j] * x_vars[k][i][j] for k in Vehicles for i in CustomersAndDepot for j in CustomersAndDepot)

# Constrains
for i in CustomersAndDepot:
    for k in Vehicles:
        prob += x_vars[k][i][i] == 0

# Each vehicle must leave the depot 0
for k in Vehicles:
    prob += lpSum(x_vars[k][0][j] for j in CustomersAndDepot) == 1

# All vehicle musr arrive at the depot H+1
for k in Vehicles:
    prob += lpSum(x_vars[k][i][6] for i in CustomersAndDepot) == 1

# In = Out
for h in Customers:
    for k in Vehicles:
        prob += lpSum(x_vars[k][i][h] for i in CustomersAndDepot) - lpSum(
            x_vars[k][h][j] for j in CustomersAndDepot) == 0

# Each customer is visited exactly once
for i in Customers:
    prob += lpSum(x_vars[k][i][j] for k in Vehicles for j in CustomersAndDepot) == 1

# From depot departs a number of vehicles equal to or smaller than K
for k in Vehicles:
    for j in CustomersAndDepot:
        prob += lpSum(x_vars[k][0][j] for k in Vehicles for j in CustomersAndDepot) <= 5

# A vehicle can only be loaded up to it's capacity
for k in Vehicles:
    prob += lpSum(Demand[i] * x_vars[k][i][j] for i in Customers for j in CustomersAndDepot) <= CapacityTruck

# Volume of Truck
for k in Vehicles:
    prob += lpSum(Volume[i] * x_vars[k][i][j] for i in Customers for j in CustomersAndDepot) <= VolumeTruck

# Business time
for k in Vehicles:
    prob += lpSum(Time[i][j] * x_vars[k][i][j] for i in CustomersAndDepot for j in CustomersAndDepot) <= 420

# The time windows are observed
for i in CustomersAndDepot:
    for k in Vehicles:
        prob += LBTW[i] <= s_vars[k][i] <= UBTW[i]

# Vehicle departure time from a customer and its immediate successor
for i in CustomersAndDepot:
    for j in CustomersAndDepot:
        for k in Vehicles:
            prob += s_vars[k][i] + Time[i][j] - maxTimeSpent * (1 - x_vars[k][i][j]) <= s_vars[k][j]

prob.solve()
print("Status:", LpStatus[prob.status])

for k in Vehicles:
    for i in CustomersAndDepot:
        for j in CustomersAndDepot:
            if x_vars[k][i][j].varValue == 1:
                print("Vehicle ", k, " from ", i, " to ", j, " in ", s_vars[k][i].varValue)

for v in prob.variables():
    print(v.name, "=", v.varValue)

# Print Optimal Solution
print("Total of distance: ", value(prob.objective))
