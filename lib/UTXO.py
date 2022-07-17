import os, json

class UTXO:
    def __init__(self, wallet):
        self.WALLET = wallet
        self.AMOUNT = 0
        self.BLOCKS = []

    def wallet_amount(self):
        self.wallet_blocks()
        self.wallet_calculation()


    def wallet_blocks(self):
        blk_list = os.listdir("ledger")
        for blk in blk_list:
            with open(f"ledger/{blk}", 'r') as b:
                block = json.load(b)
                
                for transaction in block['transactions']:
                    if ("sender", self.WALLET) in transaction.items() or ("receiver", self.WALLET) in transaction.items():
                        if not blk in self.BLOCKS:
                            self.BLOCKS.append(blk)

    def wallet_calculation(self):
        for blk in self.BLOCKS:
            with open(f"ledger/{blk}", 'r') as b:
                block = json.load(b)

                for transaction in block['transactions']:
                    if ("sender", self.WALLET) in transaction.items():
                        self.AMOUNT -= int(transaction['amount'])
                    elif ("receiver", self.WALLET) in transaction.items():
                        self.AMOUNT += int(transaction['amount'])
