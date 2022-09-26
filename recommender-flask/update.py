import pandas as pd
import os

class Updater():
    def __init__(self):
        #Read latest CSV file
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_csv(os.path.join(THIS_FOLDER, 'NFT_MINT_EVENTS.csv'))
        self.df = df[['token_new_owner_account_id', 'emitted_by_contract_account_id', 'token_id']]
        #emitted_at_block_timestamp	emitted_by_contract_account_id	token_id	event_kind	token_old_owner_account_id	token_new_owner_account_id	event_memo
        return

    def add_row(self, emitted_by_contract_account_id, token_id, token_new_owner_account_id):
        #Add row to CSV
        #Save file
        if isinstance(emitted_by_contract_account_id, str) and isinstance(token_new_owner_account_id, str):
            return False
        new_row = {'token_new_owner_account_id':token_new_owner_account_id, 'emitted_by_contract_account_id':emitted_by_contract_account_id, 'token_id':token_id}
        #append row to the dataframe
        self.df = self.df.append(new_row, ignore_index=True)
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

        self.df.to_csv(os.path.join(THIS_FOLDER, 'NFT_MINT_EVENTS.csv'), index=False)

        return True


