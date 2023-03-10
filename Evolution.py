import SnakeBot
import SnakeBotFullVision
import numpy as np
import sys

# Second attempt at evolutionary algorithm. This one will save the top 10% snakes from the population and randomly select 2 to pass on their weights



startingGeneration = 0
generationSize = 500
totalGenerations = 5000

generation = 0

newBot = SnakeBot.SnakeBot()

if(startingGeneration == 0):
    newBot.generateRandomWeights()
else:
    weights = np.load(open("weights\\gen"+str(startingGeneration)+".npy", "rb"))
    newBot.in_h1 = weights['inh1']
    newBot.h1_h2 = weights['h1h2']
    newBot.h2_out = weights['h2out']
    newBot.weights=[newBot.in_h1, newBot.h1_h2, newBot.h2_out]

currentWeights = newBot.weights
parent1 = currentWeights
parent2 = currentWeights

allScores = []

while generation <= totalGenerations:

    avg = 0
    median = 0

    allScores = []

    topScores = [-20]
    topWeights = [[currentWeights]]

    for i in range(generationSize):

        score = 0
        newBot.reset()
        newBot.generateRandomWeights()
        newBot.lifetime = 0

        ## Reproduce and mutate a new SnakeBot
        newBot.in_h1, newBot.h1_h2, newBot.h2_out = np.copy(parent1[0]), np.copy(parent1[1]), np.copy(parent1[2])
        x = np.random.randint(1, 3)
        if(x == 2):
            newBot.in_h1 = np.copy(parent2[0])
        x = np.random.randint(1, 3)
        if(x == 2):
            newBot.h1_h2 = np.copy(parent2[1])
        x = np.random.randint(1, 3)
        if(x == 2):
            newBot.h2_out = np.copy(parent2[2])
        newBot.mutate()

        ## Run SnakeBot
        while not newBot.rep.isColliding() and newBot.lifetime < 1000:
            newBot.tick()

        score = newBot.score
        allScores.append(score)

        j = 0
        found = False
        while j < (len(topWeights)) and not found and j <= generationSize / 10:
            if(score > topScores[j]):
                topScores.insert(j, score)
                topWeights.insert(j, [np.copy(newBot.in_h1),np.copy(newBot.h1_h2),np.copy(newBot.h2_out)])
                found = True
            j += 1

        avg += score

    avg /= generationSize
    median = int(allScores[int(generationSize / 2)])

    # Pick 2 random weights from the top x% to go to next generation
    x, y = np.random.randint(0, 10), np.random.randint(0, 10)
    parent1 = topWeights[x]
    parent2 = topWeights[y]

    currentWeights = topWeights[0]

    if generation % 50 == 0:
        np.savez(open("weights\\gen"+str(generation)+".npy", 'wb'), inh1=np.copy(currentWeights[0]), h1h2=np.copy(currentWeights[1]), h2out=np.copy(currentWeights[2]))

    allScores.sort()

    sys.stdout.write("Generation: " + str(generation) + ' \n')
    sys.stdout.write("Best GenScore: " + str(int(topScores[0])) + '   \n')
    sys.stdout.write("Avg Score: " + str(int(avg)) + '     \n')
    sys.stdout.write("Median Score: " + str(int(median)) + '    \r\033[A\033[A\033[A')

    generation += 1
