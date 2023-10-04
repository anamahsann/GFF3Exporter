# GFF3Exporter

Your task is to write a GFF3 feature exporter. A user should be able to run your script like this:
$ export_gff3_feature.py --source_gff=/path/to/some.gff3 --type=gene --attribute=ID --value=YAR003W

There are 4 arguments here that correspond to values in the GFF3 columns. In this case, your script 
should read the path to a GFF3 file, find any gene (column 3) which has an ID=YAR003W (column 9). 
When it finds this, it should use the coordinates for that feature (columns 4, 5 and 7) and the FASTA 
sequence at the end of the document to return its FASTA sequence.
Your script should work regardless of the parameter values passed, warning the user if no features were 
found that matched their query. (It should also check and warn if more than one feature matches the 
query.)

The output should just be printed on STDOUT (no writing to a file is necessary.)
