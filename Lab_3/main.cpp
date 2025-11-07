#include <iostream>
#include "RPG.h"
#include "Game.h"
using namespace std;

int main() {
    
    
    Game g;
    g.generatePlayers(10);
    g.gameLoop();
    g.printFinalResults();

    //Can We paste Game loop into main?
    /* Yes but I would have to make an accessor. 
    ~something like getLivePlayers*/

    return 0;
    

}
