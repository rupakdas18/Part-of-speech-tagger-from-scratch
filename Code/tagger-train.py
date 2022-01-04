# -*- coding: utf-8 -*-
"""
Program Name: Tag You're It!
Author: Rupak Kumar Das
Course: CS 5242
Date: 11/08/21
"""
"""
Program Details: This traning function determine p(tag|word) for every word type in the training data.
                It outputs these probabilities to a file named 'tagger-train-probs.txt'.
                
Code Usage: The user should follow below format in a commandline 
            tagger-train.py pos-train.txt  > tagger-train-prob.txt 
            where, tagger-train.py = Name of the program
                   pos-train.txt = Name of the training file
                   tagger-train-prob.txt = output probability file
                   
Program Algorithm: (training)
            1) For each line of the training file
                1.1) add to a dictionary where key = (word,tag), value = frequecy of the (word,tag)
                1.2) add to another dictionary where key = word, value = frequency of that word

            2) for each key of the dictionary
                2.1) add to a dictionary where key = (word,tag), value = probability (count of (word,tag)/count of word)
            3) Print that file      
      
Mode 0 Accuracy: 92.1177671406448 %
Mode 1 Accuracy: 93.34612135717303 %

"""

# Import Libraries
import argparse
import sys

# 1.1) add to a dictionary where key = (word,tag), value = frequecy of the (word,tag)
def add_dic(word,tag):
    # Add (word,tag) in a dictionary. where (word,tag) is a tuple
    word_tag = tuple([word,tag]) # creating a word,tag tuple
    
    if word_tag in word_tag_dic:
        word_tag_dic[word_tag] = word_tag_dic[word_tag] + 1        
    else:
        word_tag_dic[word_tag] = 1
        
#1.2) add to another dictionary where key = word, value = frequency of that word        
    # Add word in a dictionary    
    if word in word_dic:
        word_dic[word] = word_dic[word] + 1        
    else:
        word_dic[word] = 1
    

# Open the file and separate the word and tag
def openfile(fileName):
    
    with open (fileName, encoding='utf-8') as file:        
        for line in file:
            line = line.rstrip() # To remove the new line
            x = line.rfind('/') # Separate the word and tag. It also handles the '1/2' or 'Dutch/Shell' case
            word = line[0:x] 
            #word = word.lower()
            tag = line[x+1:]
            add_dic(word,tag)

# 2.1) add to a dictionary where key = (word,tag), value = probability (count of (word,tag)/count of word)           
def find_probability():
    for key in word_tag_dic:
        word = key[0] # First value of the tuple is the word
        prob_dic[key] = word_tag_dic[key]/word_dic[word] # finding and adding probability
        
# 3) Print that file  
def write_file():
    sorted_dic = dict(sorted(prob_dic.items(), key=lambda item: item[1])) # sort dictionary based on frequency
    #Write the dictionary in this format: 'probability tag word'
    for key in sorted_dic:
        print(sorted_dic[key],key[1],key[0])
        

word_tag_dic = {} # to store word-tag pair and count
word_dic = {} # To store word
prob_dic = {} # To store worg-tag pair and probability

if __name__ == "__main__":
    
    print("This is a program developed by Rupak Kumar Das. It tags the POS for a given number of words")
    # Parser to create command line arguments.
    parser = argparse.ArgumentParser(description='A POS tagger Program training.') # This is the description
    parser.add_argument('FileName', type = str,help='The name of the file')  # Input File selection
    args = parser.parse_args()
    output_file = 'tagger-train-prob.txt'
    sys.stdout = open(output_file, "w", encoding = 'utf8') # Open output file to write
    if args.FileName:
        fileName = args.FileName
        openfile(fileName)
        find_probability()
        write_file()
        
    sys.stdout.close() # close the output file