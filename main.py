from lib.Chain import Chain
import lib.chaintool

def main():
    transaction = {'date': 1658022629.147636, 'sender': '18gKozDA79PSFcwGFA3wQm8nhMC228d5dG', 'amount': '20', 'receiver': '18gKozDA79PSFcwGFA3wQm8nhMC228d5dG', 'signature': '9b465bbef27392b5a7738c72d41b4ee25a8853fe4d9047009b0994e1576b18ef4a9e6240e2c716ba35932b2f5ac90ba7', 'public_key': '4d2705e6c25e1fff8da8f13b1640bb38b6f7f7ee45696ff2ae4445b42add72b030e02612a232414df389fcd11d0e7d44', 'transaction_raw': '1658022629.147636.18gKozDA79PSFcwGFA3wQm8nhMC228d5dG.4d2705e6c25e1fff8da8f13b1640bb38b6f7f7ee45696ff2ae4445b42add72b030e02612a232414df389fcd11d0e7d44.20.18gKozDA79PSFcwGFA3wQm8nhMC228d5dG', 'transaction_hash': '9502443f13237e2c95e571b80764af353d541ebc68677b22a6c1b79b53605766'}

    # c = Chain()
    # c.add_transaction(transaction)
    # c.add_transaction(transaction)
    # c.add_transaction(transaction)
    # c.sign_block()
    # c.add_transaction(transaction)
    # c.add_transaction(transaction)
    # c.sign_block()

    lib.chaintool.verify()

if __name__ == '__main__':
    main()