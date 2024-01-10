Name: Ooi Wei Sheng
ID: 20204891

__________________________________________________________________________________________

Cleaning Simulation:
This project simulates a 2D envitonmrnt with multiple vacuum cleaners working to clean an evironmnet covered in dirt sports. Different strategies is implemented to compare their performance. The environment also incldues prioritised areas that should be cleaned urgently.

__________________________________________________________________________________________

Features:
Different strategies such as baseline system, distributed system and supervised system.
Using Tkinter to display the environment and the movemnets of vaccum cleaner.
Performace such as score, dirt collected, percentage of dirt collected and percentage of time in prioritised area is recorded.

__________________________________________________________________________________________

Dependencies:
Python 3.9.13
tkinter
numpy
openpyxl

___________________________________________________________________________________________

How to run the simulation:
1. Ensure you have Python 3.9.13 installed on your system
2. install the required dependencies:
   pip install tkinter
   pip install numpy
   pip install openpyxl
3. Download the source code
4. Run the main.py file using python
   python main.py

___________________________________________________________________________________________


Project Structure:
main.py: The main entry point of the simulation.
constants.py: Constants used throughout the project.
area.py: Class representing an area in the 2D environment, including prioritized areas.
dirt.py: Class representing a dirt spot in the environment.
dirtFactory.py: Class responsible for creating and distributing dirt spots.
entity.py: Base class for all entities in the environment.
point.py: Class representing a point in the 2D space.
bot.py: Base class for cleaning bots.
basicBot.py: Class for a simple cleaning bot.
statefulBot.py: Class for a cleaning bot with state management.
distributedBot.py: Class for a cleaning bot with distributed behavior.
counter.py: Class for tracking score and other metrics, including prioritized areas cleaned.

___________________________________________________________________________________________

Customising the simulation:
You can customise the simulation by changing the parameters in the 'contant.py' file.

___________________________________________________________________________________________