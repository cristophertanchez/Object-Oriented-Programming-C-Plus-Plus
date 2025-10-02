// main.cpp
#include <iostream>
#include "RPG.h"
using namespace std;

int main() {
    RPG p1("Gandalf", 0, 0.2f, 60.0f, 1);
    RPG p2; // default NPC

    cout << p1.getName() << " Current Stats\n";
    cout << "Hits Taken: " << p1.getHitsTaken()
         << "\t Luck: " << p1.getLuck()
         << "\t Exp: "  << p1.getExp()
         << "\t Level: " << p1.getLevel() << "\n\n";

    cout << p2.getName() << " Current Stats\n";
    cout << "Hits Taken: " << p2.getHitsTaken()
         << "\t Luck: " << p2.getLuck()
         << "\t Exp: "  << p2.getExp()
         << "\t Level: " << p2.getLevel() << "\n\n";

    // CALL setHitsTaken(new_hit) on p2
    int new_hit = 3;
    p2.setHitsTaken(new_hit);

    cout << "P2 got slapped " << new_hit << " times" <<"\n";
    cout << "0 did not make it, 1 dude lives \n";
    cout << p1.getName() << " = "<< p1.isAlive() << "\n";
    cout << p2.getName() << " = " << p2.isAlive() << "\n";

    return 0;
}
