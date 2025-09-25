// array.cpp
#include <cstdio>
#include <iostream>
using namespace std;

/**
 * @brief Prints the elements in the array and their memory locations.
 * @param arr  array of int (decays to pointer when passed to a function)
 * @param size number of elements in arr
 */
void printMemArr(const int arr[], int size) {
    printf("Array — Each int is %zu bytes\n", sizeof(arr[0]));
    for (int i = 0; i < size; i++) {
        printf("Index: %d  Value: %d  Address: %p\n",
               i, arr[i], (const void*)(arr + i));
    }
}

/**
 * @brief Increments all elements in arr by 10 (in place).
 * @param arr  array of int
 * @param size number of elements in arr
 */
void incArrBy10(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] += 10;
    }
}

int main() {
    // create a constant integer called SIZE that is 5
    const int SIZE = 5;

    // create and populate arr with values 100..104
    int arr[SIZE];
    for (int i = 0; i < SIZE; i++) {
        arr[i] = 100 + i;
    }

    printf("Before Increment-------------\n");
    printMemArr(arr, SIZE);

    // change the values
    incArrBy10(arr, SIZE);

    printf("After Increment--------------\n");
    printMemArr(arr, SIZE);

    return 0;
}
