import Client
import Transaction
import Block
import Blockchain

import constants as keys
import random

# Flask
from flask import Flask, jsonify, request
app = Flask(__name__)

# Storage
clients = {}
transactions = []
blockchain = Blockchain.Blockchain()

# Clientes
@app.route('/generate_address', methods = ['GET'])
def generate_address():
    #Creación del cliente
    c = Client.Client()
    
    # Añadimos el cliente
    clients[c.address] = c

    response = { 'address' : c.address }
    return jsonify(response), keys.RESPONSE_OK_CODE

@app.route('/get_balance', methods = ['POST'])
def get_balance():
    response = "Tipo de contenido no soportado"

    # Control del tipo de contenido
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.get_json()

        # Balance
        response = clients[body['address']].balance

    return jsonify(response), keys.RESPONSE_OK_CODE

# Bloques
@app.route('/generate_genesis', methods = ['POST'])
def generate_genesis():
    response = "Tipo de contenido no soportado"
    # Control del tipo de contenido
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.get_json()
        try:
            # Creación de la primera transacción de la cadena
            tx = Transaction.Transaction (
                "Genesis",
                clients[body['sender']],
                keys.INITIAL_BALANCE
            )
            # Control del balance
            if clients[body['sender']].balance == keys.INITIAL_BALANCE:

                # Creación del bloque
                genesis_block = Block.Block()
                genesis_block.previous_block_hash = None
                genesis_block.Nonce = None
                genesis_block.verified_transactions.append(tx)

                # Hash
                digest = hash(genesis_block)
                genesis_block.last_block_hash = digest

                # Añadido del bloque
                blockchain.append_block(genesis_block)

                response = "Bloque genesis creado"
            else:
                response = "Algo falló al crear el bloque genesis"
        except:
            response = "El sender no existe"

    return jsonify(response), keys.RESPONSE_OK_CODE

def create_block():
    
    new_block = Block.Block()

    # Recuperamos el último bloque
    last_block = len(blockchain._blocks) - 1 

    # Añadimos las transacciones al bloque
    for tx in transactions:
        new_block.verified_transactions.append(tx)

    # Recuperamos el hash del último bloque de la cadena
    new_block.previous_block_hash = blockchain._blocks[last_block].last_block_hash
    
    # Creamos el hash del bloque
    digest = hash(new_block)
    new_block.last_block_hash = digest

    # Proceso de minado
    random_number = random.SystemRandom()
    difficulty = random_number.randint(1, keys.MAX_DIFFICULTY)
    
    # Nonce
    new_block.Nonce = new_block.mine(digest, difficulty)
    
    # Añadimos el bloque a la cadena
    blockchain.append_block(new_block)

# Transacciones
@app.route('/get_txs', methods = ['GET'])
def get_txs():
    print("\nTransacciones:\n")
    for tx in transactions:
        Transaction.Transaction.display_transaction(tx)

    return jsonify(""), keys.RESPONSE_OK_CODE

@app.route('/create_tx', methods = ['POST'])
def create_tx():
    response = "Tipo de contenido no soportado"

    # Control del tipo de contenido
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.get_json()

        # Control del bloque génesis
        if blockchain.block_number() > 0:
            try:
                if body['value'] > 0:

                    # Control del balance del sender
                    if body['value'] <= clients[body['sender']].balance:

                        # Creación del bloque
                        if len(transactions) == keys.NUMBER_TX_BLOCK:
                            create_block()
                            del transactions[0:2]

                        # Creación de la transacción
                        tx = Transaction.Transaction(
                            clients[body['sender']],
                            clients[body['recipient']],
                            body['value']
                        )
                        # Firma
                        tx.sign_transaction()

                        # Añadido de la transacción
                        transactions.append(tx)
                        
                        response = "Transacción grabada correctamente"
                    else:
                        response = "Balance insuficiente en la cartera del sender"
                else:
                    response = "El valor a enviar debe ser superior a 0"
            except:
                response = "No existe ese cliente"
        else:
            response = "Bloque génesis no creado"

    return jsonify(response), keys.RESPONSE_OK_CODE

# Blockchain
@app.route('/get_blockchain', methods = ['GET'])
def get_blockchain():
    blockchain.print_blockchain()
    return jsonify(""), keys.RESPONSE_OK_CODE

@app.route('/get_size', methods = ['GET'])
def get_size():
    return jsonify(blockchain.block_number()), keys.RESPONSE_OK_CODE

# Lanzamos la app
app.run(host = '0.0.0.0', port = 5000)