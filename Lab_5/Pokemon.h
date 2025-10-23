#ifndef POKEMON_h
#define POKEMON_h  

#include <string>
#include <vector>
using namespace std;

class Pokemon {
// Contructors
    public:
    Pokemon();
    Pokemon(string name, int hp, int att, int def, vector<string> type);
// Mutators
 virtual void speak();
 virtual void printStats();

//Accessors
protected:
    string name;
    int hp;
    int attack;
    int defense;
    vector<string> type;
};
#endif