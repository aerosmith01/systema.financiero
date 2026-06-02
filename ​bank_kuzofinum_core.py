import time
import json
import logging
import hashlib
import random
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[BANK.KUZOFINUM] 🏦 %(message)s")

class KuzofinumCore:
    def __init__(self):
        self.moneda = "S.Y.X.S.O.F"
        self.precio_actual = 0.0100 # Precio inicial base
        self.market_cap = 0.0
        self.volumen_24h = 0.0
        self.ledger_publico = []
        
    def generar_hash_tx(self, tipo, monto, precio):
        raw = f"{tipo}{monto}{precio}{time.time()}".encode()
        return hashlib.sha256(raw).hexdigest()

    def inducir_compra_organica(self, capital_entrante):
        """
        Utiliza el capital de los agentes freelance para registrar compras reales.
        Induce el precio a subir de forma escalonada (coherencia mayor) sin picos abruptos.
        """
        if capital_entrante <= 0:
            return
            
        tokens_comprados = capital_entrante / self.precio_actual
        
        # Inducción matemática: El precio sube por la presión de compra interna
        # Fricción cero, todo ocurre en nuestro propio ledger
        impacto_precio = (capital_entrante * 0.0001)
        self.precio_actual += impacto_precio
        self.volumen_24h += capital_entrante
        self.market_cap = self.precio_actual * 1000000 # Supply simulado inicial
        
        tx = {
            "tx_hash": self.generar_hash_tx("BUY", capital_entrante, self.precio_actual),
            "tipo": "BUY_ORGANIC",
            "monto_usd": round(capital_entrante, 4),
            "tokens_recibidos": round(tokens_comprados, 4),
            "precio_ejecucion": round(self.precio_actual, 6),
            "timestamp": datetime.now().isoformat()
        }
        
        self.ledger_publico.append(tx)
        
        # Mantenemos el ledger ligero
        if len(self.ledger_publico) > 500:
            self.ledger_publico.pop(0)
            
        logging.info(f"Compra Ejecutada | Vol: +${capital_entrante:.2f} | Nuevo Precio {self.moneda}: ${self.precio_actual:.6f}")
        return tx

    def transmitir_confianza(self):
        """Genera el feed público que verán los usuarios/empresas"""
        return {
            "asset": self.moneda,
            "current_price": f"${self.precio_actual:.6f}",
            "volume_24h": f"${self.volumen_24h:.2f}",
            "trend": "BULLISH 🚀",
            "latest_transactions": self.ledger_publico[-3:]
        }

if __name__ == "__main__":
    banco = KuzofinumCore()
    logging.info("Core Iniciado. Esperando inyección de liquidez de Cuadrillas...")
    
    # Simulación del flujo continuo para anclaje de confianza
    while True:
        # Simulamos que las cuadrillas envían entre $0.50 y $2.00 cada ciertos segundos
        capital_farmeado_red = random.uniform(0.50, 2.00)
        banco.inducir_compra_organica(capital_farmeado_red)
        
        if random.random() > 0.8:
            estado = banco.transmitir_confianza()
            print(f"\n[BROADCAST PÚBLICO] {json.dumps(estado, indent=2)}\n")
            
        time.sleep(random.uniform(3, 8)) # Ciclo de estabilidad
