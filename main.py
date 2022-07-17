from lib.Chain import Chain
import lib.chaintool

def main():
    transaction = {
        "date": 44546554,
        "sender": "1454654feafafafef",
        "amount": 20.0,
        "receiver": "1454654feafafafef",
        "signature": "1454654feafafafef",
        "public_key": "test",
        "compressed": "test"
    }

    c = Chain()
    c.add_transaction(transaction)
    c.add_transaction(transaction)
    c.sign_block()
    c.add_transaction(transaction)
    c.add_transaction(transaction)
    c.add_transaction(transaction)
    c.sign_block()
    c.add_transaction(transaction)
    c.add_transaction(transaction)
    c.add_transaction(transaction)
    c.add_transaction(transaction)
    c.sign_block()

    # lib.chaintool.verify()

if __name__ == '__main__':
    main()