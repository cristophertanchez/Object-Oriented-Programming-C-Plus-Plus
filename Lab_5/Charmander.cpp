#include <iostream>
#include <stdio.h>
#include "Charmander.h"
/**
 * @brief Construct a new Charmander:: Charmander Object
 * 
 */
Charmander:: Charmander() : Pokemon (){
    type.push_back("Fire");
    skills.push_back("Growl");
    skills.push_back("Scratch");

    cout<<"Default Contructor (Charmander)\n";

}

/**
 * @brief Construct a new Charmander:: Charmander Object
 * 
 * @param name 
 * @param hp 
 * @param att 
 * @param def 
 * @param t  
 */
Charmander::Charmander(string name,int hp, int att, int def, vector<string> t, vector<string> s) {
 Pokemon(name, hp, att, def,t) ;
    type = t;
    skills = s;
    cout<<"Overloaded Contructor (Charmander)\n";
}

/**
 * @brief says what a charmander says
 * 
 */
void Charmander::speak(){
    cout<<"Charmander-Char!\n";
}

/**
 * @brief calls printStats from the parent class (Pokemon) and appends the skills used for Charmander
 * 
 */
void Charmander::printStats(){
    Pokemon::printStats();
    cout<<"Skills: ";
    for(int i=0; i<skills.size();i++){
        cout<<skills[i]<<"\t";
    }
    cout<<endl;
}