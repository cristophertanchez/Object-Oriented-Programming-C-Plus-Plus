#include "RPG.h"
#include <iostream>
#include <random>
using namespace std;

static mt19937 RNG(random_device{}());
//default constructor
RPG::RPG()
    : name("NPC"), hits_taken(0), luck(0.1), exp(0.0), level(1) {}
//overloaded constructor
RPG::RPG(string n, int h, float l, float e, int lv)
    : name(n), hits_taken(h), luck(l), exp(e), level(lv) {}
//deconstructor to save memory
RPG::~RPG() {}

//Mutators
void RPG::setHitsTaken(int new_hits) { hits_taken = new_hits; }
void RPG::setName(const string& new_name) { name = new_name; }

bool RPG::isAlive() const { return hits_taken < MAX_HITS_TAKEN; }

void RPG::updateExpLevel() {
    exp += 50.0;
    if (exp >= 100.0) {
        exp = 0.0;
        level += 1;
        luck += 0.1;
    }
}

void RPG::attack(RPG* opponent) {
    uniform_real_distribution<float> dis(0.0, 1.0);  // float in [0,1)
    float r = dis(RNG);

    // higher opponent luck ⇒ harder to land a hit
    bool hit = (r > (HIT_FACTOR * opponent->getLuck()));
    if (hit) {
        opponent->setHitsTaken(opponent->getHitsTaken() + 1);
    }
}

void RPG::printStats() const {
    cout << "Name: " << name
         << "   Hits Taken: " << hits_taken
         << "   Luck: " << luck
         << "   Exp: " << exp
         << "   Level: " << level
         << "   Status: " << (isAlive() ? "Alive" : "Dead")
         << '\n';
}

// accessors
string RPG::getName() const      { return name; }
int    RPG::getHitsTaken() const { return hits_taken; }
float  RPG::getLuck() const      { return luck; }
float  RPG::getExp() const       { return exp; }
int    RPG::getLevel() const     { return level; }
