# import pandas as pd
#
# df = pd.read_csv("phecode_definitions1.2.csv")
# df = df[["phecode", "phenotype"]]
# df.rename(columns={"phecode": "ontology_id", "phenotype": "name"}, inplace=True)
# print(df.head())
#
# df.to_parquet("phecode_v1.2.parquet")


import bionty as bt

phenotype_bt = bt.Phenotype(source="phe")

print(phenotype_bt.df())
