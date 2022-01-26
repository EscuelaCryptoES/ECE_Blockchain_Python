class Blockchain():
    
    def __init__(self):
        self._blocks = []

    # Display blockchain
    def print_blockchain(self):
        print("\nBlockchain:\n")
        for i in range(0,len(self._blocks)):
            block = self._blocks[i]
            print("                             [      ]                               ")
            print("====================================================================")
            print("Bloque #" + str(i))
            
            #Impresión del bloque
            print("Previous block hash: " + str(block.previous_block_hash))
            print("Nonce: " + str(block.Nonce))
            print("Block Hash: " + str(block.last_block_hash))

            # Impresión de transacciones
            for tx in block.verified_transactions:
                tx.display_transaction()

            print("====================================================================")

    # Añadido de un bloque a la cadena
    def append_block(self, b):
        self._blocks.append(b)

    # Número de bloques en la cadena
    def block_number(self):
        return len(self._blocks)