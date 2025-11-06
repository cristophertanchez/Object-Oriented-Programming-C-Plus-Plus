#ifndef RPG_H
#define RPG_H

#include <string>
using namespace std;

const float HIT_FACTOR     = 0.05;  // affects chance to hit (vs opponent luck)
const int   MAX_HITS_TAKEN = 3;      // 3 hits = KO

class RPG {
public:
    RPG();  // default NPC
    RPG(string name, int hits_taken, float luck, float exp, int level);
    ~RPG();

    // actions
    void  attack(RPG* opponent);   // attempt to hit opponent
    void  printStats() const;      // pretty-print stats
    void  updateExpLevel();        // +50 exp, level up at 100 (then exp -> 0, luck += 0.1)

    // mutators
    void  setHitsTaken(int new_hits);
    void  setName(const string& new_name);

    // accessors
    bool  isAlive() const;
    string getName() const;
    int    getHitsTaken() const;
    float  getLuck() const;
    float  getExp() const;
    int    getLevel() const;

private:
    string name;
    int    hits_taken;
    float  luck;
    float  exp;
    int    level;
};

#endif
