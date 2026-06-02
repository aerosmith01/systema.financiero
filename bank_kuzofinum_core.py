import os
import time
import json
import logging
from datetime import datetime
from web3 import Web3

logging.basicConfig(level=logging.INFO, format="[BANK.KUZOFINUM] 🏦 %(message)s")

class KuzofinumCoreWeb3:
    def __init__(self):
        self.moneda = "S.Y.X.S.O.F"
        
        # Conexión a la Blockchain (Ej. Polygon/Arbitrum para latencia 0 y gas bajo)
        self.rpc_url = os.getenv("RPC_URL", "https://polygon-rpc.com")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Direcciones y Credenciales de Producción
        self.contrato_syxsof_address = os.getenv("SYXSOF_CONTRACT_ADDRESS", "")
        self.billetera_banco = os.getenv("BANK_WALLET_ADDRESS", "")
        self.llave_privada = os.getenv("BANK_PRIVATE_KEY", "")
        
        # ABI Básico para interactuar con el contrato de S.Y.X.S.O.F.
        self.abi = [
            {"constant": False, "inputs": [{"name": "montoInyeccion", "type": "uint256"}], "name": "comprarEInflar", "outputs": [], "type": "function"},
            {"constant": True, "inputs": [], "name": "precioActual", "outputs": [{"name": "", "type": "uint256"}], "type": "function"}
        ]
        
        if self.w3.is_connected():
            logging.info("Conectado a la Blockchain exitosamente. Red lista para inflar S.Y.X.S.O.F.")
        else:
            logging.warning("Sin conexión a la Blockchain. Revisa tu RPC_URL.")

    def verificar_precio_onchain(self):
        """Consulta el precio real de S.Y.X.S.O.F. directamente en el contrato"""
        if not self.contrato_syxsof_address:
            return 0.0
            
        contrato = self.w3.eth.contract(address=self.contrato_syxsof_address, abi=self.abi)
        try:
            # Llama a la función de lectura del contrato
            precio_wei = contrato.functions.precioActual().call()
            return self.w3.from_wei(precio_wei, 'ether')
        except Exception as e:
            logging.error(f"Error leyendo precio On-Chain: {e}")
            return 0.0

    def ejecutar_compra_blockchain(self, capital_farmeado_usd):
        """
        Toma el capital farmeado, firma la transacción y la inyecta al contrato
        inteligente para subir el precio de S.Y.X.S.O.F. en producción.
        """
        if not self.w3.is_connected() or not self.llave_privada:
            logging.warning("Modo Simulación: Credenciales Web3 no configuradas.")
            return {"status": "simulado", "monto": capital_farmeado_usd}

        # Conversión del capital farmeado a Wei (asumiendo que el gas/compra se paga en el token nativo de la red)
        # En producción, aquí calculamos la equivalencia USD -> MATIC/ETH
        monto_inyeccion_wei = self.w3.to_wei(capital_farmeado_usd, 'ether') # Simplificación para la inyección

        contrato = self.w3.eth.contract(address=self.contrato_syxsof_address, abi=self.abi)
        
        try:
            # Construcción de la transacción
            nonce = self.w3.eth.get_transaction_count(self.billetera_banco)
            tx = contrato.functions.comprarEInflar(monto_inyeccion_wei).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 250000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'value': monto_inyeccion_wei # El capital real que infla el pool
            })

            # Firma criptográfica (fricción 0, ejecución directa)
            tx_firmada = self.w3.eth.account.sign_transaction(tx, private_key=self.llave_privada)
            
            # Envío a la red
            tx_hash = self.w3.eth.send_raw_transaction(tx_firmada.rawTransaction)
            
            logging.info(f"¡Compra On-Chain Ejecutada! Hash: {self.w3.to_hex(tx_hash)}")
            
            return {
                "status": "on_chain_success",
                "tx_hash": self.w3.to_hex(tx_hash),
                "capital_inyectado": capital_farmeado_usd,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Falla en la inyección blockchain: {e}")
            return {"status": "error", "detalle": str(e)}

    def procesar_flujo_cuadrilla(self, ingresos_cuadrilla):
        """Método integrador que se llamará desde el SOFI v4.0"""
        logging.info(f"Recibiendo liquidez de la cuadrilla: ${ingresos_cuadrilla}")
        precio_antes = self.verificar_precio_onchain()
        
        resultado_tx = self.ejecutar_compra_blockchain(ingresos_cuadrilla)
        
        if resultado_tx["status"] == "on_chain_success":
            precio_despues = self.verificar_precio_onchain()
            logging.info(f"S.Y.X.S.O.F. Inflado. Precio subió de {precio_antes} a {precio_despues}")
            
        return resultado_tx
