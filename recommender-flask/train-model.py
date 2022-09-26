import pandas as pd
from pandas.api.types import CategoricalDtype
from scipy import sparse
from implicit.lmf import LogisticMatrixFactorization
import os

model = LogisticMatrixFactorization()
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
model = model.load(os.path.join(THIS_FOLDER, 'LogisticModel.npz'))
df = pd.read_csv(os.path.join(THIS_FOLDER, 'NFT_MINT_EVENTS.csv'))
df = df[['token_new_owner_account_id', 'emitted_by_contract_account_id', 'token_id']]
processed_df = df.groupby(['token_new_owner_account_id', 'emitted_by_contract_account_id']).size().reset_index(name='counts')

most_popular_df = df.groupby(['emitted_by_contract_account_id']).size().reset_index(name='counts')
most_popular_df = most_popular_df.sort_values('counts',ascending=False)

accounts = processed_df["token_new_owner_account_id"].unique()
contracts = processed_df["emitted_by_contract_account_id"].unique()
shape = (len(accounts), len(contracts))

# Create indices for users and movies
accounts_cat = CategoricalDtype(categories=sorted(accounts), ordered=True)
contracts_cat = CategoricalDtype(categories=sorted(contracts), ordered=True)
account_index = processed_df["token_new_owner_account_id"].astype(accounts_cat).cat.codes
contract_index = processed_df["emitted_by_contract_account_id"].astype(contracts_cat).cat.codes

# Conversion via COO matrix
coo = sparse.coo_matrix((processed_df["counts"], (account_index, contract_index)), shape=shape)
csr = coo.tocsr()

lm = LogisticMatrixFactorization(factors=29, learning_rate=1.804, regularization=0.748, iterations=25)
lm.fit(csr)

lm.save('LogisticModelLatest')