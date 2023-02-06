#Based on https://github.com/magbak/mbei-experiments/blob/main/ExperimentA/analysis.R
deps <- c("plyr","tidyverse")
packs <- installed.packages()

for (d in deps) {
  if (!(d %in% packs[,"Package"])) {
    install.packages(d)
  }
}
library(plyr)
library(tidyverse)


filename_maplib <- "/home/magbak/repos/maplib_paper_benchmarks/results/maplib_csv_materialization.csv"
filename_morph_oxi <- "/home/magbak/repos/maplib_paper_benchmarks/results/results_morph_kgc_oxigraph_materialization.csv"
filename_morph_rdflib <- "/home/magbak/repos/maplib_paper_benchmarks/results/results_morph_kgc_rdflib_materialization.csv"
filename_sparql_anything <- "/home/magbak/repos/maplib_paper_benchmarks/results/results_sparql_anything_materialization.csv"

df_maplib <- read_csv(filename_maplib)
df_morph_oxi <- read_csv(filename_morph_oxi)
df_morph_rdflib <- read_csv(filename_morph_rdflib)
df_sparql_anything <- read_csv(filename_sparql_anything)
df_sparql_anything

df_maplib <- df_maplib %>% mutate(Solution = "maplib") %>% select(Solution, Scale, Iteration, Time)
df_morph_oxi <- df_morph_oxi %>% mutate(Solution = "M-KGC(O)") %>% select(Solution, Scale, Iteration, Time)
df_morph_rdflib <- df_morph_rdflib %>% mutate(Solution = "M-KGC(R)") %>% select(Solution, Scale, Iteration, Time)
df_sparql_anything <- df_sparql_anything %>% mutate(Solution = "SA") %>% select(Solution, Scale, Iteration, Time)

df <- bind_rows(df_maplib, df_morph_oxi, df_morph_rdflib, df_sparql_anything)
df <- df %>% mutate(Scale=factor(Scale))
df <- df %>% group_by(Scale, Solution) %>% summarise(across(Time, list(sd=sd, mean=mean)), .groups="keep")

fn <- function(x) round(x,2)
df_rounded <- df %>% mutate_all(fn)
print(df_rounded)
cbbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

t1<-theme(                              
  plot.background = element_blank(), 
  #panel.grid.major = element_blank(), 
  #panel.grid.minor = element_blank(), 
  strip.background = element_blank(),
  #panel.border = element_blank(), 
  panel.background = element_blank(),
  axis.line = element_line(size=.4),
  strip.text.x = element_text(size=12),
  legend.position="bottom"
)

mater <- ggplot(df, aes(fill=Solution, x=Scale, y=Time_mean)) + 
  scale_fill_manual(values=cbbPalette) + 
  theme_bw() +
  t1 + 
  geom_bar(stat="identity", position="dodge") +
  geom_errorbar(aes(ymin=Time_mean-Time_sd, ymax=Time_mean+Time_sd), position="dodge") +
  labs(x="Scale", y="Materialization time (seconds)", fill="") +
  theme(text = element_text(size = 12), legend.position = "bottom", legend.direction = "horizontal") +
  expand_limits(y=0) 
mater

ggsave("/home/magbak/Documents/bakke1.png", mater, dpi=600, width =10, height=10, units="cm")

