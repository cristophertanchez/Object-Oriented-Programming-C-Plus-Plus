// RPG.cpp
#include "RPG.h"

// default constructor
RPG::RPG()
    : name("NPC"), hits_taken(0), luck(0.1f), exp(50.0f), level(1) {}

// overloaded constructor
RPG::RPG(string name, int hits_taken, float luck, float exp, int level)
    : name(name), hits_taken(hits_taken), luck(luck), exp(exp), level(level) {}

// mutators
void RPG::setHitsTaken(int new_hits) {
    hits_taken = new_hits;
}

bool RPG::isAlive() const {
    // alive as long as hits_taken is less than MAX_HITS_TAKEN
    return hits_taken < MAX_HITS_TAKEN;
}

// accessors
string RPG::getName() const       { return name; }
int    RPG::getHitsTaken() const  { return hits_taken; }
float  RPG::getLuck() const       { return luck; }
float  RPG::getExp() const        { return exp; }
int    RPG::getLevel() const      { return level; }
