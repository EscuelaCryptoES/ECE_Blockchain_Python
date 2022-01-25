import Block

class Blockchain():
    
    def __init__(self):
        self._blocks = []

    def print_blockchain(self):
        print("Numero de bloques en la blockchain: " + str(len(self._blocks)))
        for i in range(0,len(self._blocks)):
            block = self._blocks[i]
            print("====================================================================")
            print("Bloque #" + str(i))
            for tx in block.verified_transactions:
                print("--------------------------------------------------------------------")
                tx.display_transaction()
            print("====================================================================")

    def append_block(self, b):
        self._blocks.append(b)