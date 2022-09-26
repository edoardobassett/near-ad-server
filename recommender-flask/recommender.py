#Load model weights

import pandas as pd
from pandas.api.types import CategoricalDtype
from scipy import sparse
from implicit.lmf import LogisticMatrixFactorization
import numpy as np
import os
import random

class Recommender():
    def __init__(self):
        self.model = LogisticMatrixFactorization()
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.model = self.model.load(os.path.join(THIS_FOLDER, 'LogisticModel.npz'))
        df = pd.read_csv(os.path.join(THIS_FOLDER, 'NFT_MINT_EVENTS.csv'))
        self.df = df[['token_new_owner_account_id', 'emitted_by_contract_account_id', 'token_id']]
        self.processed_df = self.df.groupby(['token_new_owner_account_id', 'emitted_by_contract_account_id']).size().reset_index(name='counts')

        self.most_popular_df = self.df.groupby(['emitted_by_contract_account_id']).size().reset_index(name='counts')
        self.most_popular_df = self.most_popular_df.sort_values('counts',ascending=False)

        self.accounts = self.processed_df["token_new_owner_account_id"].unique()
        self.contracts = self.processed_df["emitted_by_contract_account_id"].unique()
        shape = (len(self.accounts), len(self.contracts))

        # Create indices for users and movies
        self.accounts_cat = CategoricalDtype(categories=sorted(self.accounts), ordered=True)
        self.contracts_cat = CategoricalDtype(categories=sorted(self.contracts), ordered=True)
        self.account_index = self.processed_df["token_new_owner_account_id"].astype(self.accounts_cat).cat.codes
        self.contract_index = self.processed_df["emitted_by_contract_account_id"].astype(self.contracts_cat).cat.codes

        # Conversion via COO matrix
        coo = sparse.coo_matrix((self.processed_df["counts"], (self.account_index, self.contract_index)), shape=shape)
        self.csr = coo.tocsr()
        return

    def recommend(self, account, n_recommendations=10):
        if account not in self.accounts or account is None:
            return random.sample(self.most_popular_df.loc[:,"emitted_by_contract_account_id"].values[:n_recommendations*10].tolist(), n_recommendations)

        #Get account id
        acc_index = np.where(self.accounts == account)[0][0]
        acc_match = self.account_index.iloc[[acc_index]].values[0]

        recommendations = self.model.recommend(acc_match, self.csr[acc_match], N=n_recommendations)[0]

        str_recommendations = []
        for rec in recommendations:
            str_recommendations.append(self.contracts_cat.categories.values[rec])

        return str_recommendations

    def random_wallet(self):
        return self.df.sample().token_new_owner_account_id.values.tolist()[0]


    def similar(self, smart_contract, n):
        if smart_contract not in self.contracts:
            return []

        contract_index = np.where(self.contracts == smart_contract)[0][0]
        acc_match = self.contract_index.iloc[[contract_index]].values[0]
        matches = self.model.similar_items(itemid=acc_match, N=n)[0].tolist()
        str_recommendations = []
        for match in matches:
            str_recommendations.append(self.contracts_cat.categories.values[match])
        return str_recommendations

    def interacted(self, account, smart_contract):
        return smart_contract in self.df.loc[self.df['token_new_owner_account_id'] == account]['emitted_by_contract_account_id'].values


