# SimpleBadApple

from badapple2_csv import badapple2_add_pscores_to_csv

df = badapple2_add_pscores_to_csv(
    input_csv="collected_abfe.csv",
    output_csv="collected_abfe_with_badapple_nan.csv",
    smiles_col="smiles",
    output_col="BadApple",
    batch_size=1,
)
