from pulp import *

# Sets
Vehicles = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']  #
Customers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
CustomersAndDepot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

list_a = [0, 16]
list_b = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# Parameter
CapacityTruck = 1000
VolumeTruck = 5.6

Demand = {1: 492, 2: 915, 3: 420, 4: 480, 5: 342, 6: 1000, 7: 320, 8: 170, 9: 313, 10: 120, 11: 60, 12: 60, 13: 300,
          14: 592, 15: 112}
Volume = {1: 1.2, 2: 3, 3: 1.5, 4: 0.75, 5: 0.96, 6: 1.65, 7: 0.96, 8: 0.36, 9: 0.96, 10: 0.36, 11: 0.72, 12: 0.72,
          13: 0.9, 14: 1.83, 15: 0.45}

ServiceTime = {0: 0, 1: 30, 2: 30, 3: 30, 4: 30, 5: 30, 6: 30, 7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30, 13: 30,
               14: 30, 15: 30, 16: 0}
LBTW = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
UBTW = {0: 420, 1: 120, 2: 120, 3: 120, 4: 120, 5: 120, 6: 120, 7: 120, 8: 360, 9: 360, 10: 360, 11: 360, 12: 360,
        13: 360, 14: 360, 15: 360, 16: 420}

Distance = {
    0: {0: 0, 1: 14.1, 2: 10.3, 3: 9.5, 4: 11.3, 5: 17.8, 6: 9.1, 7: 13.0, 8: 2.4, 9: 10.5, 10: 4.7, 11: 8.3, 12: 10.0,
        13: 9.8, 14: 17.5, 15: 15.8, 16: 0},  #
    1: {0: 14.1, 1: 0, 2: 16.6, 3: 11.3, 4: 10.4, 5: 21.2, 6: 14.8, 7: 12.1, 8: 14.0, 9: 4.5, 10: 10.5, 11: 15.7,
        12: 16.1, 13: 16.3, 14: 3.2, 15: 9.7, 16: 14.1},
    2: {0: 10.3, 1: 16.6, 2: 0, 3: 7.9, 4: 10.4, 5: 20.4, 6: 2.2, 7: 12.1, 8: 14.3, 9: 12.1, 10: 8.1, 11: 3.6, 12: 2,
        13: 0.5, 14: 20.3, 15: 17.1, 16: 10.3},
    3: {0: 9.5, 1: 11.3, 2: 7.9, 3: 0, 4: 3.2, 5: 9, 6: 8.4, 7: 4, 8: 9.6, 9: 7, 10: 5.4, 11: 4.5, 12: 7.3, 13: 7.1,
        14: 13.3, 15: 9.8, 16: 9.5},
    4: {0: 11.3, 1: 10.4, 2: 10.4, 3: 3.2, 4: 0, 5: 12.3, 6: 12, 7: 4, 8: 11.5, 9: 5.6, 10: 6.6, 11: 8.9, 12: 11.7,
        13: 11.5, 14: 11.3, 15: 6.7, 16: 11.3},
    5: {0: 17.8, 1: 21.2, 2: 20.4, 3: 9, 4: 12.3, 5: 0, 6: 20.3, 7: 11.4, 8: 23.1, 9: 15, 10: 18.3, 11: 17.3, 12: 20,
        13: 19.8, 14: 19.3, 15: 10.5, 16: 17.8},
    6: {0: 9.1, 1: 14.8, 2: 2.2, 3: 8.4, 4: 12, 5: 20.3, 6: 0, 7: 11.8, 8: 11, 9: 11.8, 10: 6.5, 11: 3.3, 12: 1.6,
        13: 1.8, 14: 17.8, 15: 16.3, 16: 9.1},
    7: {0: 13.0, 1: 12.1, 2: 12.1, 3: 4, 4: 4, 5: 11.4, 6: 11.8, 7: 0, 8: 12, 9: 6.5, 10: 7.2, 11: 9.4, 12: 12.2,
        13: 12, 14: 12.2, 15: 7.1, 16: 13.0},
    8: {0: 2.4, 1: 14.0, 2: 14.3, 3: 9.6, 4: 11.5, 5: 23.1, 6: 11, 7: 12, 8: 0, 9: 13, 10: 7.2, 11: 10.8, 12: 12.6,
        13: 12.4, 14: 19, 15: 18.3, 16: 2.4},
    9: {0: 10.5, 1: 4.5, 2: 12.1, 3: 7, 4: 5.6, 5: 15, 6: 11.8, 7: 6.5, 8: 13, 9: 0, 10: 6.9, 11: 8.9, 12: 11.7,
        13: 11.5, 14: 6.5, 15: 7.7, 16: 10.5},
    10: {0: 4.7, 1: 10.5, 2: 8.1, 3: 5.4, 4: 6.6, 5: 18.3, 6: 6.5, 7: 7.2, 8: 7.2, 9: 6.9, 10: 0, 11: 5.5, 12: 6.7,
         13: 6.5, 14: 13.4, 15: 12, 16: 4.7},
    11: {0: 8.3, 1: 15.7, 2: 3.6, 3: 4.5, 4: 8.9, 5: 17.3, 6: 3.3, 7: 9.4, 8: 10.8, 9: 8.9, 10: 5.5, 11: 0, 12: 2.9,
         13: 2.7, 14: 14.6, 15: 13.1, 16: 8.3},
    12: {0: 10.0, 1: 16.1, 2: 2, 3: 7.3, 4: 11.7, 5: 20, 6: 1.6, 7: 12.2, 8: 12.6, 9: 11.7, 10: 6.7, 11: 2.9, 12: 0,
         13: 1.9, 14: 16.4, 15: 14.9, 16: 10.0},
    13: {0: 9.8, 1: 16.3, 2: 0.5, 3: 7.1, 4: 11.5, 5: 19.8, 6: 1.8, 7: 12, 8: 12.4, 9: 11.5, 10: 6.5, 11: 2.7, 12: 1.9,
         13: 0, 14: 19, 15: 17.5, 16: 9.8},
    14: {0: 17.5, 1: 3.2, 2: 20.3, 3: 13.3, 4: 11.3, 5: 19.3, 6: 17.8, 7: 12.2, 8: 19, 9: 6.5, 10: 13.4, 11: 14.6,
         12: 16.4, 13: 19, 14: 0, 15: 8.5, 16: 7.5},
    15: {0: 15.8, 1: 9.7, 2: 17.1, 3: 9.8, 4: 6.7, 5: 10.5, 6: 16.3, 7: 7.1, 8: 18.3, 9: 7.7, 10: 12, 11: 13.1,
         12: 14.9, 13: 17.5, 14: 8.5, 15: 0, 16: 15.8},
    16: {0: 0, 1: 14.1, 2: 10.3, 3: 9.5, 4: 11.3, 5: 17.8, 6: 9.1, 7: 13.0, 8: 2.4, 9: 10.5, 10: 4.7, 11: 8.3, 12: 10.0,
         13: 9.8, 14: 17.5, 15: 15.8, 16: 0}}

# set problem variable
prob = LpProblem("VRPTW", LpMinimize)

# Dicision Vartiable
Time = LpVariable.dicts("TimeBetweenij",
                        (CustomersAndDepot, CustomersAndDepot),
                        0)

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
#
# Constrains
for i in CustomersAndDepot:
    for k in Vehicles:
        prob += x_vars[k][i][i] == 0

# Each vehicle must leave the depot 0
for k in Vehicles:
    prob += lpSum(x_vars[k][0][j] for j in CustomersAndDepot) == 1

# All vehicle musr arrive at the depot H+1
for k in Vehicles:
    prob += lpSum(x_vars[k][i][16] for i in CustomersAndDepot) == 1

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
        prob += lpSum(x_vars[k][0][j] for k in Vehicles for j in CustomersAndDepot) <= len(Vehicles)

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

# for v in prob.variables():
# print(v.name, "=", v.varValue)

# Print Optimal Solution
print("Total of distance: ", value(prob.objective))
