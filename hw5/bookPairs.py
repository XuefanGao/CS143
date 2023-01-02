from pyspark import SparkContext
from itertools import combinations
sc = SparkContext("local", "bookPairs")
lines = sc.textFile("/home/cs143/data/goodreads.dat")

# return list
def find_combo(str):
    index = str.index(':')
    substr = str[index+1:]
    id_list = substr.split(",")
    int_list = []
    for i in id_list:
        int_list.append(int(i))
    res = list(combinations(int_list, 2))
    ordered = list(map(lambda sub: (sub[1], sub[0]) if sub[1] < sub[0] else sub, res))
    return list(set(ordered))


pair = lines.flatMap(lambda line: find_combo(line))
pair = pair.map(lambda word: (word, 1))
pair_count = pair.reduceByKey(lambda a, b: a+b)
pair_count = pair_count.filter(lambda a: a[1]>20)

pair_count.saveAsTextFile("/home/cs143/output1")
