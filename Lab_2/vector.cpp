// vector.cpp
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;

/**
 * @brief prints the elements in the vector and their memory locations
 *
 * @param v vector of integers (const reference to avoid copying)
 */
void printMemVec(const vector<int>& v){
    printf("Vector — size=%zu capacity=%zu (Each int is %zu bytes)\n",
           v.size(), v.capacity(), sizeof(v[0]));
    for(size_t i = 0; i < v.size(); i++){
        // &v[i] is the address of the i-th element inside the contiguous buffer
        printf("Value: %d at Memory Location: %p\n", v[i], (const void*)(&v[i]));
    }
}

/**
 * @brief increments all of the elements in v by 10
 *
 * @param v reference to a vector of integers (modifies in place)
 */
void incVecBy10(vector<int>& v){
    for(size_t i = 0; i < v.size(); i++){
        v[i] += 10;
    }
}

int main(){
    // create a constant integer called SIZE that is of value 5
    const int SIZE = 5;

    // create a vector of integers called vec that can hold up to 5 elements
    vector<int> vec;
    vec.reserve(SIZE);

    // use a for loop to populate vec with the values 100 to 104
    for(int i = 0; i < SIZE; i++){
        vec.push_back(100 + i);
    }

    printf("Before Increment-------------\n");
    printMemVec(vec);

    // call incVecBy10(...) on vec
    incVecBy10(vec);

    printf("After Increment--------------\n");
    printMemVec(vec);

    // remove last element of vec (pop_back)
    vec.pop_back();

    printf("After Pop--------------------\n");
    printMemVec(vec);

    // append 101 and 102 at the end of vec
    vec.push_back(101);
    vec.push_back(102);

    printf("After Push-------------------\n");
    printMemVec(vec);

    return 0;
}
