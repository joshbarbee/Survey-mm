The task process is as follows:
- 
1. data is taken from a google survey form, imported into csv form
2. edited by the mm_formate_data equation
3. the data is then edited into a matrice using concurrency to minimize time usage
4. then imported into the comparision file
5. weighs strict factors first, then runs any eligible canidates on a moderate/loose factor scale
6.  uses a custom made algorithm to compare two lists, analyzing where they differ. requires both lists to be the same length and contain same elements
7.  then sends it to a mysql server hosted on an aws vm, which connects to a webserver via flask
