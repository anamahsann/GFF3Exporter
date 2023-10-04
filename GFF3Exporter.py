#!/usr/bin/env python3

# encoding: utf8
# author: Anam Ahsan

import argparse
import os
import sys
import re

def main():
    parser = argparse.ArgumentParser( description= 'The GFF3 file to parse')

    ##Arguments to gather from GFF3 file 

    parser.add_argument('-i', '--input_file', type=str, required=True, help= 'Path to an input file to be read' )
    parser.add_argument('-t', '--type', type=str, required=True, help='Type in column 3' )
    parser.add_argument('-a', '--attribute', type=str, required=True, help='Attribute in column 9' )
    parser.add_argument('-v', '--value', type=str, required=True, help='Value in column 9' )

    args = parser.parse_args()

    #Variables to indicate location in file 
    in_fasta_section = False
    thematch = False
    #Variables to store extracted information from file 
    numofid = 0
    seqid = ''
    attval = '' 
    start = 0
    end = 0
    strand = ''
    idtag = ''
    sequence = ''

    #iIterate through file, line by line
    for line in open(args.input_file):

        line = line.rstrip()

        #Check if in FASTA section or not
        if line.startswith('##FASTA'):
             in_fasta_section = True         

        #If not in FASTA section, extract data according to type, attribute and value
        if in_fasta_section == False:
            cols = line.split("\t")
            if len(cols) == 9:
                types = cols[2]
                attr = cols[8]
                if types == args.type:
                    features = attr.split(";")
                    #If data is found, print information and store coordinates for sequence 
                    if args.attribute in features[0] and args.value in features[0]:
                        seqid = cols[0]
                        attval = features[0] 
                        start = int(cols[3])
                        end = int(cols[4])
                        strand = cols[6]
                        #Print type, attribute and value that match arguments  
                        sys.stdout.write(">{0}:{1}".format(types, attval))
                        sys.stdout.write("\n")
                        numofid += 1 #counts how many matches in file 
                        continue
                #If data not found, continue parsing file     
                else:
                    continue
                
        #If in FASTA section,find sequence according to ID         
        if in_fasta_section == True:
            #search for sequence 
            m = re.match(">(\S+)\s*", line.rstrip())
            if m:
                idtag = m.groups()
                #If match is found, change section variable to true
                if seqid in idtag:
                    thematch = True
                    continue
                else:
                    thematch = False 
        #Extract and store lines of sequence to new variable 
        if thematch == True: 
            sequence += line.rstrip()
            continue
        
    #Print sequence according to coordinates and strand
    if len(sequence) > 0:
        if strand == '+':
            sys.stdout.write(sequence[start:end])
            sys.stdout.write("\n")
        else:
           sys.stdout.write(sequence[end:start])
           sys.stdout.write("\n")
           
    #Let user know if know matches are found
    if len(seqid) < 1:
        sys.stdout.write("No features match the query")
        sys.stdout.write("\n")

    #Let user know if more than one match found 
    if numofid > 1:
        sys.stdout.write("There is more than one match for this query, provide more specification")
        sys.stdout.write("\n")
            
if __name__ == '__main__':
    main()
