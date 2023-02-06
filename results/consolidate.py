import polars as pl

maplib_dfs = []
for i in [5,10,50,100]:
    df = pl.scan_csv(f"results_maplib_{i}.csv")
    df = df.with_column(pl.lit(i).alias("scaling"))
    df = df.with_column(pl.col("query").str.replace(".rq", "").str.replace("q", "Q"))
    df = df.with_column(pl.lit("maplib").alias("solution"))
    maplib_dfs.append(df)

morph_kgc_oxigraph_dfs = []
for i in [5, 10]:
    for j in range(1,11):
        df = pl.scan_csv(f"results_morph_kgc_oxigraph_{i}_{j}.csv")
        df = df.with_column(pl.lit(i).alias("scaling"))
        df = df.with_column(pl.col("query").str.replace(".rq", "").str.replace("q", "Q"))
        df = df.with_column(pl.lit("M-KGC(O)").alias("solution"))
        df = df.filter(pl.col("query") != "Q10")
        morph_kgc_oxigraph_dfs.append(df)

morph_kgc_rdflib_dfs = []
for i in [5]:
    df = pl.scan_csv(f"results_morph_kgc_rdflib_{i}.csv")
    df = df.with_column(pl.lit(i).alias("scaling"))
    df = df.with_column(pl.col("query").str.replace(".rq", "").str.replace("q", "Q"))
    df = df.with_column(pl.lit("M-KGC(R)").alias("solution"))
    df = df.filter(pl.col("query") != "Q10")
    morph_kgc_rdflib_dfs.append(df)

sparql_anything_dfs = []
for i in [5, 10]:
    for j in range(1,11):
        df = pl.scan_csv(f"results_sparql_anything_{i}_{j}.csv")
        df = df.with_column(pl.lit(i).alias("scaling"))
        df = df.with_column(pl.col("query").str.replace(".rq", "").str.replace("q", "Q"))
        df = df.with_column(pl.lit("SA").alias("solution"))
        sparql_anything_dfs.append(df)


dfs = pl.concat(maplib_dfs + morph_kgc_oxigraph_dfs + morph_kgc_rdflib_dfs + sparql_anything_dfs).collect().groupby(["solution", "query", "scaling"]).agg([
    pl.col("time").mean().alias("mean_time").round(2),
    pl.col("time").std().alias("std").round(2)
]).with_columns([
    pl.col("query").str.replace("Q", "").cast(pl.Int32).alias("query_no"),
    #(pl.col("mean_time") + "(" + pl.col("std") + ")").alias("mean_time_std")
]).sort(["query_no","scaling", "solution"]).pivot(index=["query", "scaling"], values=["mean_time"], columns="solution")
print(dfs.to_pandas().to_latex(index=False).replace("NaN", "-"))
dfs.write_csv("results_all.csv")
