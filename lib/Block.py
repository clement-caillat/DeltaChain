import datetime, lib.chaintool, json, os
import hashlib

class Block:
    def __init__(self, PREVIOUS_HASH):
        self.BLOCK_NUMBER = len(os.listdir("ledger"))
        self.PREVIOUS_HASH = PREVIOUS_HASH
        self.PENDING_TRANSACTIONS = []
        self.RAW_TRANSACTIONS = ""

    def add_transaction(self, transaction):
        self.PENDING_TRANSACTIONS.append(transaction)
        self.RAW_TRANSACTIONS += transaction["transaction_raw"] + "."

    def sign_block(self):
        if len(self.PENDING_TRANSACTIONS) != 0:
            if len(self.PENDING_TRANSACTIONS) == 1 and self.PENDING_TRANSACTIONS[0]['sender'] == "DELTACHAINREWARD":
                pass
            else:
                from lib.Chain import DIFFICULTY
                block_order = str(self.BLOCK_NUMBER) + 'x'
                date = datetime.datetime.now().timestamp()
                transactions = self.PENDING_TRANSACTIONS
                raw_transactions = self.RAW_TRANSACTIONS[:-1]
                merkleroot = hashlib.sha256(raw_transactions.encode()).hexdigest()
                previous_hash = self.PREVIOUS_HASH
                reward = 10
                raw = f"{block_order}/{date}/{raw_transactions}/{previous_hash}/{reward}"

                hash = lib.chaintool.mine(raw)

                data = {
                    'block_order': block_order,
                    'date': date,
                    'transactions': transactions,
                    'transaction_block_raw': raw_transactions,
                    'merkleroot': merkleroot,
                    'reward': reward,
                    'block_raw': raw,
                    'previous_hash': previous_hash,
                    'hash': hash
                }

                block_id = block_order + hash
                with open(f"ledger/{block_id}.blk", "w") as b:
                    json.dump(data, b)
                return hash