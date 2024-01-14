import numpy as np

#Define environment (check discord for the grid im using)
envRows = 5
envCols = 5

#3d array for q-table
q_values = np.zeros((envRows, envCols, 4))

#Define actions
#0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

#Define rewards 
rewards = np.full((envRows, envCols), -999)

roads = {}
roads[0] = [i for i in range(5)]
roads[1] = [0, 2]
roads[2] = [0, 1, 2, 3]
roads[3] = [0, 3]
roads[4] = [i for i in range(4)]

#Set rewards for road squares
for row_index in range(0, 5):
  for column_index in roads[row_index]:
    rewards[row_index, column_index] = -1.


rewards[4,2] = 100 #Goal square
rewards[0,2] = -10 #intersection square
rewards[4,0] = -10
#Print matrix
for row in rewards:
  print(row)



#Function that determines if a square isn't a road
def isNotRoad(currentRow, currentCol):
    #Check if reward is -1 or not
    if rewards[currentRow, currentCol] == -1.:
        return False
    else:
        return True
    
    
#Function to choose random road square
def get_starting_location():
    currentRow = np.random.randint(envRows)
    currentCol = np.random.randint(envCols)
    
    #Keep going until random location is on a road square
    while isNotRoad(currentRow, currentCol):
        currentRow = np.random.randint(envRows)
        currentCol = np.random.randint(envCols)
    return currentRow, currentCol


#Function to choose next action        
def get_next_action(currentRow, currentCol, epsilon):
    if np.random.random() < epsilon:
        return np.argmax(q_values[currentRow, currentCol])
    else:
        return np.random.randint(4)

#Function to get the next square location
def get_next_square(currentRow, currentCol, action):
    newRow = currentRow
    newCol = currentCol

    #Check if moves are valid
    if actions[action] == 'up'and currentRow > 0:
        newRow -= 1
    elif actions[action] == 'right' and currentCol < envCols - 1:
        newCol += 1
    elif actions[action] == 'down' and currentRow < envRows - 1:
        newRow += 1
    elif actions[action] == 'left' and currentCol > 0:
        newCol -= 1
    return newRow, newCol


#Function to find shortest path
def get_shortest_path(startRow, startCol):
    if isNotRoad(startRow, startCol):
        return []
    else:
        currentRow = startRow
        currentCol = startCol
        shortestPath = []
        shortestPath.append([currentRow, currentCol])
        
        while not isNotRoad(currentRow, currentCol):
            # Pass a smaller epsilon value for exploration
            action = get_next_action(currentRow, currentCol, 1.)
            currentRow, currentCol = get_next_square(currentRow, currentCol, action)
            shortestPath.append([currentRow, currentCol]) 
        return shortestPath
    


#TRAINING

#Define training parameters
epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.9


#run through 100 episodes
for episode in range(100):
    row, col = get_starting_location()

    while not isNotRoad(row, col):
        action = get_next_action(row, col, epsilon)
        
        oldRow, oldCol = row, col
        row, col = get_next_square(row, col, action)
        
        reward = rewards[row, col]
        old_qvalue = q_values[oldRow, oldCol, action]
        temporal_diff = reward + (discount_factor * np.max(q_values[row, col])) - old_qvalue
        
        new_qvalue = old_qvalue + (learning_rate * temporal_diff)
        q_values[oldRow, oldCol, action] = new_qvalue
    
print("Finished Training")


#Test output, start at 0,0
print("Start at 0,0, goal at 4,2")
print("Shortest path")
print(get_shortest_path(0,0))