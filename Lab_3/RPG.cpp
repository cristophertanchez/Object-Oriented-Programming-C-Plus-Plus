// RPG.cpp
#include "RPG.h"

// default constructor
RPG::RPG(){
    this->name=name; 
    this->hits_taken=hits_taken; 
    this-> luck=luck;
    this-> exp=exp; 
    this-> level=level;
}
// overloaded constructor
RPG::RPG(string name, int hits_taken, float luck, float exp, int level)
    {
    this->name=name; 
    this->hits_taken=hits_taken; 
    this->luck=luck; 
    this->exp=exp; 
    this->level=level;
    }
// mutators
void RPG::setHitsTaken(int new_hits) {
    this->hits_taken = new_hits;
}

bool RPG::isAlive() const {
    // alive as long as hits_taken is less than MAX_HITS_TAKEN
    return this->hits_taken < MAX_HITS_TAKEN;
}

// accessors
string RPG::getName() const       { return name; }
int    RPG::getHitsTaken() const  { return hits_taken; }
float  RPG::getLuck() const       { return luck; }
float  RPG::getExp() const        { return exp; }
int    RPG::getLevel() const      { return level; }
