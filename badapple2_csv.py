def badapple2_get_associated_scaffolds(
    smiles_list,
    database="badapple2",
    max_rings=5,
    base_url="https://chiltepin.health.unm.edu/badapple2",
    timeout=60,
):
    import requests

    url = f"{base_url}/api/v1/compound_search/get_associated_scaffolds"
    r = requests.get(
        url,
        params={"SMILES": smiles_list, "database": database, "max_rings": max_rings},
        timeout=timeout,
    )
    return r.json()


def badapple2_get_pscores(
    smiles_list,
    database="badapple2",
    max_rings=5,
    base_url="https://chiltepin.health.unm.edu/badapple2",
    timeout=60,
):
    import numpy as np

    data = badapple2_get_associated_scaffolds(
        smiles_list,
        database=database,
        max_rings=max_rings,
        base_url=base_url,
        timeout=timeout,
    )

    out = {}
    for smi, scaff_list in data.items():
        pscores = [d.get("pscore") for d in scaff_list if d.get("pscore") is not None]
        if len(pscores) == 0:
            print(f"Warning: no valid pscore for {smi} in badapple2_get_pscores")
            out[smi] = np.nan
        else:
            out[smi] = max(pscores)

    return out


def _chunk_list(x, chunk_size):
    return [x[i:i + chunk_size] for i in range(0, len(x), chunk_size)]


def badapple2_add_pscores_to_csv(
    input_csv,
    output_csv,
    smiles_col="smiles",
    output_col="BadApple",
    database="badapple2",
    max_rings=5,
    base_url="https://chiltepin.health.unm.edu/badapple2",
    batch_size=1,
    timeout=60,
    index=False,
):
    import pandas as pd
    import tqdm

    df = pd.read_csv(input_csv)
    smiles_unique = df[smiles_col].dropna().drop_duplicates().tolist()
    smiles_batches = _chunk_list(smiles_unique, batch_size)

    dict_badapple = {}
    for smiles_batch in tqdm.tqdm(smiles_batches):
        dict_badapple.update(
            badapple2_get_pscores(
                smiles_batch,
                database=database,
                max_rings=max_rings,
                base_url=base_url,
                timeout=timeout,
            )
        )

    df[output_col] = df[smiles_col].map(dict_badapple)
    df.to_csv(output_csv, index=index)

    return df
