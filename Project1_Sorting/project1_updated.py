"""
Math 590
Project 1
Fall 2019

Partner 1:
Partner 2:
Date:
"""

"""
SelectionSort
"""
def SelectionSort(listToSort):
    for i in range(len(listToSort)-1):
        min_index = i
        for j in range(i+1,len(listToSort)):
            if listToSort[j] < listToSort[min_index]:
                min_index = j        
        temp = listToSort[i]
        listToSort[i] = listToSort[min_index]
        listToSort[min_index] = temp 
    return listToSort

"""
InsertionSort
"""
def InsertionSort(listToSort):
    for i in range(len(listToSort)):
        j = i - 1
        value = listToSort[i]
        while j >= 0 and value < listToSort[j]:
            temp = listToSort[j+1]
            listToSort[j+1] = listToSort[j]
            listToSort[j] = temp
            j = j - 1
    return listToSort

"""
BubbleSort
"""
def BubbleSort(listToSort):
    swapped = 1
    n = len(listToSort)
    while(swapped):
        swapped = 0
        for i in range(1, n):
            if listToSort[i-1] > listToSort[i]:
                temp = listToSort[i]
                listToSort[i] = listToSort[i-1]
                listToSort[i-1] = temp
                swapped = 1
        n = n-1
    return listToSort

"""
MergeSort
"""
def MergeSort(listToSort):
    if len(listToSort) > 1:
        mid = len(listToSort)//2
        left = listToSort[:mid]
        right = listToSort[mid:]
        MergeSort(left)
        MergeSort(right)
        i = j = k = 0
        while i < len(left) and j < len(right) : 
            if left[i] < right[j]:
                listToSort[k] = left[i]
                i = i + 1
            else:
                listToSort[k] = right[j]
                j = j + 1
            k = k + 1
        while i < len(left):
                listToSort[k] = left[i]
                i = i + 1
                k = k + 1        
        while j < len(right):
                listToSort[k] = right[j]
                j = j + 1
                k = k + 1
    return listToSort

"""
QuickSort

Sort a list with the call QuickSort(listToSort),
or additionally specify i and j.
"""


def QuickSort(listToSort, i=0, j=None):
    # Set default value for j if None.
    if j == None:
        j = len(listToSort)
    
    if j <= 1:
        return
    
    front = left_init = i
    rear = right_init = i + j - 1
    pivot = listToSort[(front+rear)//2]
    
    while front <= rear:
        while front <= rear and listToSort[front] < pivot:
            front = front + 1
        while front <= rear and listToSort[rear] > pivot:
            rear = rear - 1
        if front <= rear:
            listToSort[front],listToSort[rear] = listToSort[rear],listToSort[front]
            front = front + 1
            rear = rear - 1
    
    QuickSort(listToSort, left_init, rear - left_init+1)
    QuickSort(listToSort, front, right_init - front+1)


"""
Importing the testing code after function defs to ensure same references.
"""
from project1tests_updated import *

"""
Main function.
"""
if __name__ == "__main__":
    print('Testing Selection Sort')
    print()
    testingSuite(SelectionSort)
    print()
    print('Testing Insertion Sort')
    print()
    testingSuite(InsertionSort)
    print()
    print('Testing Bubble Sort')
    print()
    testingSuite(BubbleSort)
    print()
    print('Testing Merge Sort')
    print()
    testingSuite(MergeSort)
    print()
    print('Testing Quick Sort')
    print()
    testingSuite(QuickSort)
    print()
    print('DEFAULT measureTime')
    print()
    measureTime()
