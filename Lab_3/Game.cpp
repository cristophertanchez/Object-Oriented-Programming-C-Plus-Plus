#include "Game.h"
#include <iostream>
#include <random>
using namespace std;

static mt19937 GRNG(random_device{}());

Game::Game() {}

void Game::generatePlayers(int n) {
    for ( int i = 0; i < n; ++i) {
        players.push_back(new RPG());

        string new_name = "NPC_" + to_string(i);
        players[i]->setName(new_name);
        live_players.insert(i);
    }
}

int Game::selectPlayer() {
random_device rd;
mt19937 gen(rd());
uniform_int_distribution<> dis(0, live_players.size() - 1);

int rand_index = dis(gen);

    set<int>::iterator it = live_players.begin(); 
    advance(it, rand_index);
    int selected_index = *it; 
    return selected_index;
}

void Game::endRound(RPG* winner, RPG* loser, int loserIndex) {
    winner->setHitsTaken(0);
    live_players.erase(loserIndex);
    winner->updateExpLevel();
    cout << winner->getName() << " won against " << loser->getName() << "\n\n";
}

void Game::battleRound() {
    // ensure two different fighters
    int idx1 = selectPlayer();
    int idx2 = selectPlayer();
    while (idx2 == idx1) {
        idx2 = selectPlayer();
    }

    RPG* p1 = players[idx1];
    RPG* p2 = players[idx2];

    // alternate attacks until one is KO'd
    while (p1->isAlive() && p2->isAlive()) {
        p1->attack(p2);
        if (!p2->isAlive()) break;
        p2->attack(p1);
    }

    if (p1->isAlive()) {
        endRound(p1, p2, idx2);
    } else {
        endRound(p2, p1, idx1);
    }
}

void Game::gameLoop() {
    while (live_players.size() > 1) {
        battleRound();
    }
}

void Game::printFinalResults() const {
    for (const RPG* p : players) {
        p->printStats();
    }
}
