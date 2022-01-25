import Client
import Transaction
import Block
import Blockchain

import constants as keys
from flask import Flask, jsonify, request

app = Flask(__name__)

clients = {}
transactions = []
blockchain = Blockchain.Blockchain()

@app.route('/generate', methods = ['GET'])
def generate():
    c = Client.Client()
    clients[c.address] = c

    response = { 'address' : c.address }
    print(clients)

    return jsonify(response), keys.RESPONSE_OK_CODE

@app.route('/get_blockchain', methods = ['GET'])
def get_blockchain():
    response = ""
    blockchain.print_blockchain()
    return jsonify(response), keys.RESPONSE_OK_CODE

@app.route('/generate_genesis', methods = ['POST'])
def generate_genesis():
    response = "Tipo de contenido no soportado"
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.get_json()
        try:
            print("Sender: " + str(clients[body['sender']]))
            tx = Transaction.Transaction (
                "Genesis",
                clients[body['sender']],
                keys.INITIAL_BALANCE
            )
            if clients[body['sender']].balance == keys.INITIAL_BALANCE:
                # crear el primer bloque
                genesis_block = Block.Block()
                genesis_block.previous_block_hash = None
                genesis_block.Nonce = None
                genesis_block.verified_transactions.append(tx)
                digest = hash(genesis_block)
                print(digest)
                genesis_block.last_block_hash = digest
                blockchain.append_block(genesis_block)
                response = "Bloque genesis creado"
            else:
                response = "Algo falló al crear el bloque genesis"
        except:
            response = "El sender no existe"

    return jsonify(response), keys.RESPONSE_OK_CODE

@app.route('/get_txs', methods = ['GET'])
def get_txs():
    response = "Lista de transacciones pendiente de programar"
    print("\nTransacciones:\n")
    print ("------------------------------------------------------------------------")
    for tx in transactions:
        Transaction.Transaction.display_transaction(tx)

    return jsonify(response), keys.RESPONSE_OK_CODE

@app.route('/get_balance', methods = ['POST'])
def get_balance():
    response = "Tipo de contenido no soportado"
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.get_json()
        response = clients[body['address']].balance

    return jsonify(response), keys.RESPONSE_OK_CODE


@app.route('/create_tx', methods = ['POST'])
def create_tx():
    response = "Tipo de contenido no soportado"
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.get_json()
        try:
            print("Sender " + str(clients[body['sender']]))
            print("Recipient " + str(clients[body['recipient']]))
            if body['value'] > 0:
                print("Value " + str(body['value']))
                if body['value'] <= clients[body['sender']].balance:
                    if len(transactions) == keys.NUMBER_TX_BLOCK:
                        create_block()
                        del transactions[0:2]

                    tx = Transaction.Transaction(
                        clients[body['sender']],
                        clients[body['recipient']],
                        body['value']
                    )
                    tx.sign_transaction()
                    transactions.append(tx)
                    response = "Transacción grabada correctamente"
                else:
                    response = "Balance insuficiente en la cartera del sender"
            else:
                response = "El valor a enviar debe ser superior a 0"
        except:
            response = "No existe ese cliente"

    return jsonify(response), keys.RESPONSE_OK_CODE

def create_block():
    new_block = Block.Block()
    last_block = len(blockchain._blocks) - 1

    for tx in transactions:
        new_block.verified_transactions.append(tx)

    # crea el bloque
    new_block.previous_block_hash = blockchain._blocks[last_block].last_block_hash
    print(new_block.previous_block_hash)

    # TODO mining
    new_block.Nonce = None

    digest = hash(new_block)
    new_block.last_block_hash = digest
    blockchain.append_block(new_block)

# Launch of the app
app.run(host = '0.0.0.0', port = 5000)