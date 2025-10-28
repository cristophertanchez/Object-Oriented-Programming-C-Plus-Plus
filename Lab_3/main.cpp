// main.cpp
#include <iostream>
#include "RPG.h"
using namespace std;

int main() {
    RPG p1("Gandalf", 0, 0.2, 60.0, 1);
    RPG p2; // default NPC
    RPG p3("Saruman", 2, 0.1, 45.0, 2);
     // DISPLAY each player's stats using accessors

    cout << p1.getName() << " Current Stats\n";
    cout << "Hits Taken: " << p1.getHitsTaken()
         << "\t Luck: " << p1.getLuck()
         << "\t Exp: "  << p1.getExp()
         << "\t Level: " << p1.getLevel() << "\n\n";
    cout << p2.getName() << "Current Stats\n";
    cout << "Hits Taken: " << p2.getHitsTaken()
         << "\t Luck: " << p2.getLuck()
         << "\t Exp: "  << p2.getExp()
         << "\t Level: " << p2.getLevel() << "\n\n";

     cout<< p3.getName()<< " Joined the party. Curent Stat: "<<endl;
     cout<< p3.getHitsTaken()<< " hits taken, "
          << p3.getLuck()<< " luck, "
          << p3.getExp()<< " exp, "
          << p3.getLevel()<< " level.\n\n";

    // CALL setHitsTaken(new_hit) on p2
    int new_hit = 3;
    p2.setHitsTaken(new_hit);
    int new_hit_p1 = 1;
     p1.setHitsTaken(new_hit_p1);
     int new_hit_p3 = 2;
     p3.setHitsTaken(new_hit_p3);

    cout << "P2 got slapped " << new_hit << " times" <<"\n";
    cout << "P1 got slapped " << new_hit_p1 << " times" <<"\n";
    cout << "P3 got slapped " << new_hit_p3 << " times" <<"\n";
    cout << "0 did not make it, 1 dude lives \n";
    cout << p1.getName() << " = "<< p1.isAlive() << "\n";
    cout << p2.getName() << " = " << p2.isAlive() << "\n";
    cout << p3.getName() << " = " << p3.isAlive() << "\n";

    return 0;
}
