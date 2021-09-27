# Q-voter model

Script written in Python to visualize/simulate the q-voter model on square net.
User can choose from two models: conformity & anticonformity or conformity & independence
Shows live animation of model and plots mean of opinion in time.

## How to run the app
Simply run in console `python q_voter_simulation.py`.
It's also important to download the icon and put in the same folder as app for it to work properly
(or comment the 287 line in q_voter_simulation.py ➡ `# window.iconbitmap(default='q_icon.ico')`).

## Instruction 
In the app you have to enter the net size (qive N, where net is of size NxN).
Rest of parameters can be changed accordingly to ones preferences.
Pressing "START" button will start the simulation with selected parameters (new window should pop up).
Pause and start buttons can be used to pause and resume simulation.
"END" button ends simulation and closes pop up window with simulation.
After closing a pop up window, new parameters can be choosen and new simulation started.

## About the model 
- as the model is on square net, voters on edges don't have 4 neighbour.
- initial concentration of positive opinion is the percent of voters that have positive opinion (= 1).

## Further reading 
- [Voter model](https://en.wikipedia.org/wiki/Voter_model)
- [Q-voter model](http://www.if.pwr.wroc.pl/~katarzynaweron/lectures/final-poster-MECO-38-d.pdf)

## Author
[Edyta Łabędzka](https://github.com/3dytalabedzka)