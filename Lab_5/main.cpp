#include <iostream>
#include "Charmander.h"
using namespace std;
int main()
{
    //Charmander first=Charmander();
    vector<string> pokemonType;
    pokemonType.push_back("Fire");

    vector<string> skills;
    skills.push_back("Growl");
    skills.push_back("Scratch");

    cout<<"------Contructor Created------\n";
    Charmander charlie = Charmander("Charlie", 100,4,4, pokemonType , skills);
    //Charmander
    cout<<"\n------Charmander Speak------\n";
    charlie.speak();
    //Pokemon pointer to Charmander
    Pokemon* c1= &charlie;
    cout << "\n------ Speak called from Charmander Pointer------\n";
(*c1).speak();
// Charmander
cout<<"\n------ Charmander Stats ------\n";
charlie.printStats();
}