#matchmaking python script from csv
#formula inspired by "User Recommendation in Reciprocal and Bipartite Social Networks" and previous TikTok MM samples
import mm_formate_data as mm
import mm_comparision as mc
import mm_sql as sql_f
import time


def main():
    filea = "dating_sample.csv"
    matrix = mm.import_csv(filea)
    matrix = mm.modifier(filea, matrix)
    sql_f.aggregate(mc.main_parser(matrix),matrix)
    
if __name__ == "__main__": 
    initial = time.time()
    main()
    print(time.time()-initial)