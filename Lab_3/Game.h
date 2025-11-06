#ifndef GAME_H
#define GAME_H

#include <vector>
#include <set>
#include "RPG.h"
using namespace std;

class Game {
public:
    Game();

    void generatePlayers(int n);    // NPC_0..NPC_(n-1)
    int  selectPlayer();            // choose a random alive index
    void battleRound();             // two distinct players fight to a KO
    void endRound(RPG* winner, RPG* loser, int loserIndex);
    void gameLoop();                // repeat rounds until one remains
    void printFinalResults() const; // print everyone

private:
    vector<RPG*> players;           // owns RPG*, delete in ~Game
    set<int>     live_players;      // alive indices into players
};

#endif
