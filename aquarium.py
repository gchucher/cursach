import asyncio
import random



async def temperature(CurrentTemp):
    while True:
        TempChange = random.randint(0, 5)
        TempSign = random.randint(0, 1)
        if TempSign == 1:
            CurrentTemp += TempChange
        else:
            CurrentTemp -= TempChange
        if CurrentTemp < 0:
            CurrentTemp = 0

        if CurrentTemp > 100:
            CurrentTemp = 100

        print('temperature ', CurrentTemp)
        await asyncio.sleep(1)

async def water_level(CurrentLevel):
    while True:
        LevelChange = random.randint(0, 5)
        LevelSign = random.randint(0, 1)
        if LevelSign == 1:
            CurrentLevel += LevelChange
        else:
            CurrentLevel -= LevelChange

        if CurrentLevel < 0:
            CurrentLevel = 0

        if CurrentLevel > 100:
            CurrentLevel = 100

        print('water level ', CurrentLevel)
        await asyncio.sleep(1)

async def pollution(CurrentPollution):
    while True:
        PollutionChange = random.randint(0, 5)
        PollutionSign = random.randint(0, 1)

        if PollutionSign == 1:
            CurrentPollution += PollutionChange
        else:
            CurrentPollution -= PollutionChange

        if CurrentPollution < 0:
            CurrentPollution = 0

        if CurrentPollution > 100:
            CurrentPollution = 100

        print('pollution', CurrentPollution)
        await asyncio.sleep(1)
