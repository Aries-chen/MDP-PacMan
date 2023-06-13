# MDP-PacMan
MDP Agent in Pac-Man Game

This project was developed while I was learning about Artificial Intelligence Reasoning and Decision Making. The entire structure has been implemented except for mdpAgents.py, where I write code to help PacMan survive.

* Task: Using Markov Decision Process (MDP) to help PacMan avoids ghosts and pass the game without explicit motion control.

Prior knowledge of Markov Decision Processes is recommended. Note that you can only calculate the actions either by Value Iteration, Policy Iteration or Modified Policy Iteration. After exploring the available methods, I found that the Value Iteration was the best (but you may find the Policy Iteration better).

Value iteration:

![image](https://github.com/Aries-chen/MDP-PacMan/assets/62194666/211a0c60-4e21-421a-a88a-9318029605ce)

* Solution: "Bellman equation + value iteration" was used to find the optimal policy, and "breadth-first search + Manhattan distance" was used to perceive information about hazards and benefits over a range.


(1) evaluate whether your code can win games in smallGrid by running:

```
python pacman.py -q -n 25 MDPAgent -l smallGrid
```

-l is shorthand for -layout. -p is shorthand for -pacman. -n 25 runs 25 games in a row

(2) evaluate whether your code can win games in mediumClassic by running:

```
python pacman.py -q -n 25 MDPAgent -l mediumClassic
```

And -q runs the game without the interface (making it faster). I would suggest removed '-q' when you are debugging.

* Results: Achieved excellence results in both small and medium-sized grids

I think BFS is crucial in saving the PacMan as it allows to sense the enviroment and decide when to approach a scared ghost-eater and when to leave a ghost in a sinful state. 

![image](https://github.com/Aries-chen/MDP-PacMan/assets/62194666/b39c152c-1acb-4bfc-8aa0-94f26c0498af)
