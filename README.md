# Maplib benchmark
This repository contains benchmark setup and results associated with maplib and belongs to a paper currently submitted for peer review.
Contact me if you need help running the benchmarks. 

## Running
Place csv data generated from GTFS benchmark for given size in "data"-folder.

E.g. FREQUENCIES.csv should be located directly in "data".

The generator can be found here: https://github.com/oeg-upm/gtfs-bench

### SPARQL Anything
First install pandas and SPARQLWrapper (I used 1.5.2 and 2.0.0 respectively).

Download the SPARQL anything server release from https://github.com/SPARQL-Anything/sparql.anything

Start the SPARQL Anything server jar 

Run benchmark_sparql_anything.py 

This runs mapping + queries once. Rerun for each iteration.

For each run, remember to first restart the SPARQL Anything server jar.

### Maplib
Follow instructions to install wheel here: https://github.com/magbak/maplib

I used release 0.3.12 

Run benchmark_maplib.py 

This runs mapping + queries N times (specified in file). 

### Morph-KGC
Run pip install morph-kgc

We used version 2.3.1 

Run benchmark_morph_kgc_oxigraph.py or benchmark_morph_kgc_rdflib.py 

This runs mapping + queries once. Rerun for each iteration. 

## Notes
queries are from https://github.com/oeg-upm/gtfs-bench/tree/master/queries at 9e4dbe3e7c796c68e3ec649a1060bf19f4843f5e

config.ini and mapping.csv.ttl is from https://github.com/oeg-upm/morph-kgc/blob/main/examples/csv/
at 53e25026492f80e49e1f4665dbc7808299b8a3b5

queries in sparql_anything are from: https://github.com/SPARQL-Anything/experiments/tree/main/gtfs at ff62c7a44c4c7ccf52f9232799e4e6ccd147cb0e

