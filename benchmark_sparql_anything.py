import os
import time
from pathlib import Path
from SPARQLWrapper import SPARQLWrapper, POST, JSON
import pandas as pd

query_folder = Path("sparql_anything") / "construct_queries"
ep = "http://localhost:3000/sparql.anything"
def mapping():
    w = SPARQLWrapper(ep)
    start_time = time.time()
    for f in os.listdir(query_folder):
        with open(query_folder / f) as qf:
            q = qf.read()
            w.setMethod(POST)
            w.setReturnFormat(JSON)
            w.setQuery(q)
            print(w.query())

    end_time = time.time()
    took = end_time - start_time
    print(f"Materialization took {round(took, 2)}")


iteration = 1
scaling = 50
errors = 0
perf = []

mapping()
# g.parse("triples.nt")
# g.serialize("maplib_triples.nt", format="nt")

query_path = Path("queries")

for fname in os.listdir(query_path):
    #Q9 causes sigkill - out of memory in python..

    if fname in [f'q{str(i)}.rq' for i in [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18]]:
        with open(query_path / fname) as f:
            q = f.read()
            print(fname.replace(".rq", "\n"))
            start = time.time()
            error = False
            height = -1
            try:
                wr = SPARQLWrapper(ep)
                wr.setQuery(q)
                wr.setTimeout(120)
                wr.setReturnFormat(JSON)
                res = wr.queryAndConvert()
                height = len(res["results"]["bindings"])
            except Exception as e:
                error = True
                print(f"Error {e}")
                errors += 1

            used_time = round(time.time() - start, 2)
            print(f"Took {used_time} seconds")
            perf.append((iteration, fname, used_time, height, error))

print(f"N errors {errors}\n")

df = pd.DataFrame(perf, columns=["iteration", "query", "time", "n", "error"]).sort_values("query")
df.to_csv(f"results_sparql_anything_{scaling}_{iteration}.csv", index=False)

