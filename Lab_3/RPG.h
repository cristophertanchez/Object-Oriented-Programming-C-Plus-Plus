// RPG.h
#ifndef RPG_H
#define RPG_H

#include <string>
using std::string;

const int   INVENTORY_SIZE = 10;
const float HIT_FACTOR     = 0.05;
const int   MAX_HITS_TAKEN = 3;

class RPG {
public:
    // constructors
    RPG();
    RPG(string name, int hits_taken, float luck, float exp, int level);

    // mutators
    bool isAlive() const;
    void setHitsTaken(int new_hits);

    // accessors
    string getName()    const;
    int    getHitsTaken() const;
    float  getLuck()    const;
    float  getExp()     const;
    int    getLevel()   const;

private:
    string name = "NPC ";
    int    hits_taken;
    float  luck;
    float  exp;
    int    level;
};

#endif
