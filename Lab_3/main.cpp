#include <iostream>
#include "RPG.h"
#include "Game.h"
using namespace std;

int main() {
    Game g;
    g.generatePlayers(10);
    g.gameLoop();
    g.printFinalResults();
    return 0;
}
