import pandas as pd
import morph_kgc
import time
import pathlib
import os

iteration = 1
scaling = 50

start = time.time()
db = morph_kgc.materialize_oxigraph("config.ini")
# db.serialize("morph_triples.nt", format="nt")
end = time.time()
print(f"Materialization took {round(end - start, 2)} seconds\n")

errors = 0
perf = []

query_path = pathlib.Path("queries")

for fname in os.listdir(query_path):
    if fname in [f'q{str(i)}.rq' for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18]]:
        with open(query_path / fname) as f:
            q = f.read()
            print(fname.replace(".rq", "\n"))
            start = time.time()
            error = False
            l = -1

            try:
                res = [a for a in db.query(q)]
                l = len(res)
                print(f"Ok {l}")
            except Exception as e:
                print(f"Error {e}")
                errors += 1
                error = True

            used_time = round(time.time() - start, 2)
            print(f"Took {used_time} seconds\n")
            perf.append((iteration, fname, used_time, l, error))

print(f"N errors {errors}\n")

df = pd.DataFrame(perf, columns=["iteration", "query", "time", "n", "error"]).sort_values(["query"])
df.to_csv(f"results_morph_kgc_oxigraph_{scaling}_{iteration}.csv", index=False)
