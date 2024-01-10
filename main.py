from experiment import Experiment, ExperimentWithDistributedSystem, ExperimentWithSupervisedSystem

import openpyxl
import os

def runExperiments(numberOfBots: int, numberOfRuns: int, experimentType: int, numberOfMoves: int, numberOfDirt: int):
    # Create a new xlsx workbook and sheet
    wb = openpyxl.Workbook()
    sheet = wb.active
    
    if experimentType == 0:
        experiment = ExperimentWithSupervisedSystem()
        print("Supervised system with " + str(numberOfBots)+ " bots")
        sheet.title = "Supervised System"
    elif experimentType == 1:
        experiment = ExperimentWithDistributedSystem()
        print("Distributed system with " + str(numberOfBots)+ " bots")
        sheet.title = "Distributed System"
    else:
        experiment = Experiment()
        print("Baseline system with " + str(numberOfBots)+ " bots")
        sheet.title = "Baseline System"

    avgScore = 0
    avgDirtCollected = 0
    avgPercentageOfDirtCollected = 0
    avgPercentageOfTimeinPriorityArea = 0

    # Add headers to the sheet
    sheet.append(["Run #","Score", "Dirt Collected", "% Dirt Collected", "% Time in Priority Area"])


    print("Run #    |  Score  | Dirt Collected | % Dirt Collected | % Time in Priority Area")
    print("--------------------------------------------------------------------------------")
    # Run the experiment multiple times and add the results to the sheet
    for i in range(numberOfRuns):
        counter = experiment.run(numberOfMoves, numberOfDirt, numberOfBots)
        score = counter.score
        dirtCollected = counter.totalDirtAddedNumber - counter.uncollectedDirtNumber
        percentageOfDirtCollected = (dirtCollected / counter.totalDirtAddedNumber) * 100
        percentageOfTimeinPriorityArea = (counter.existanceOfPriorityAreas / numberOfMoves) * 100
        print(f"{i+1:^8} | {score:^7.2f} | {dirtCollected:^14d} | {percentageOfDirtCollected:^16.2f} | {percentageOfTimeinPriorityArea:^24.2f}")
        avgScore += score
        avgDirtCollected += dirtCollected
        avgPercentageOfDirtCollected += percentageOfDirtCollected
        avgPercentageOfTimeinPriorityArea += percentageOfTimeinPriorityArea
        sheet.append([i+1, round(score, 2), round(dirtCollected, 2), round(percentageOfDirtCollected, 2), round(percentageOfTimeinPriorityArea, 2)])

    avgScore /= numberOfRuns
    avgDirtCollected /= numberOfRuns
    avgPercentageOfDirtCollected /= numberOfRuns
    avgPercentageOfTimeinPriorityArea /= numberOfRuns
    sheet.append(["Average", round(avgScore, 2), round(avgDirtCollected, 2), round(avgPercentageOfDirtCollected, 2), round(avgPercentageOfTimeinPriorityArea, 2)])
    print(f"{'Average ':^6} | {avgScore:^7.2f} | {avgDirtCollected:^14.2f} | {avgPercentageOfDirtCollected:^16.2f} | {avgPercentageOfTimeinPriorityArea:^24.2f} \n")

    # Save the xlsx file
    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)
    wb.save(f"{directory}/{numberOfBots}-bots_{experimentType}.xlsx")

def main():
    numberOfRuns = 10
    numberOfBots = [2, 4, 8, 10] # only 2 4 8 and 10 are supported, check out readme for more info
    numberOfMoves = [1000, 1000, 1000, 1000]
    numberOfDirt = [2000, 3000, 4000, 5000]
    for idx, n in enumerate(numberOfBots):
        runExperiments(n, numberOfRuns, 0, numberOfMoves[idx], numberOfDirt[idx])
        runExperiments(n, numberOfRuns, 1, numberOfMoves[idx], numberOfDirt[idx])
        runExperiments(n, numberOfRuns, 2, numberOfMoves[idx], numberOfDirt[idx])
        
main()
