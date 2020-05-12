import csv
import pandas as pd
import concurrent.futures

#import and read survey csv
def import_csv(filea):
    matrix = pd.read_csv(filea, index_col=0, squeeze=True).to_dict()
    return matrix

#change the gender into a 1/0. reduces ttl and eases comparision
def correct_gender(matrix):
    for k,v in matrix["Gender"].items():
        if v == "M": 
            matrix["Gender"][k] = 0
        if v == "F":
            matrix["Gender"][k] = 1
    return matrix["Gender"]

#change desired gender into 1/0 to reduce ttl and ease comparision
def correct_lf(matrix):
    for k,v in matrix["LF"].items():
        if v == "M": 
            matrix["LF"][k] = 0
        if v == "F":
            matrix["LF"][k] = 1
    return matrix["LF"]

#change if one is drug friendly or not into 1/0 to reduce ttl and ease comparision
def drug_pref(matrix):
    for k,v in matrix["Drugs"].items():
        if v == "Yes": 
            matrix["Drugs"][k] = 0
        if v == "No":
            matrix["Drugs"][k] = 2
        if v == "Mixed":
            matrix["Drugs"][k] = 1
    return matrix["Drugs"]

#changes if someone NEEDS the other person to have similar hobbies to them or not for the match to work
#this is largely for investigative purposes, since its hard to generalize hobbies
def similar_hobbies(matrix):
    for k,v in matrix["Similar_hobbies"].items():
        if v == "Yes": 
            matrix["Similar_hobbies"][k] = 0
        if v == "No":
            matrix["Similar_hobbies"][k] = 1
    return matrix["Similar_hobbies"]

def party_tendency(matrix):
    for k,v in matrix["Party"].items():
        if v == "Yes": 
            matrix["Party"][k] = 0
        if v == "No":
            matrix["Party"][k] = 2
        if v == "Mixed":
            matrix["Party"][k] = 1
    return matrix["Party"]

def extra_intravert(matrix):
    for k,v in matrix["Vert"].items():
        if v == "Extra": 
            matrix["Vert"][k] = 0
        if v == "Intra":
            matrix["Vert"][k] = 1
    return matrix["Vert"]
#multithread processes. program is natively ran on a 8ct/8t cpu so take advantage of all 8ct/t minimizes ttl by 60% or so 
def modifier(filea, matrix):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        c_gender = executor.submit(correct_gender, matrix).result()
        d_pref = executor.submit(drug_pref,matrix).result()
        s_hobbies = executor.submit(similar_hobbies,matrix).result()
        lf = executor.submit(correct_lf,matrix).result()
        parties = executor.submit(party_tendency,matrix).result()
        e_i_vert = executor.submit(extra_intravert,matrix).result()
        matrix["Gender"] = c_gender
        matrix["Drugs"] = d_pref
        matrix["Similar_hobbies"] = s_hobbies
        matrix["LF"] = lf
        matrix["Party"] = parties
        matrix["Vert"] = e_i_vert
    return matrix