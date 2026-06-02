import logging
import json
import zlib
from bank_kuzofinum_core import KuzofinumCoreWeb3
from convergencia_dual_mia import OrquestadorConvergencia

# Configuración del ecosistema
logging.basicConfig(level=logging.INFO, format="[SYXSOF-CONVERGENCIA] ⚡ %(message)s")

class SYXSOF_Main_Control:
    def __init__(self):
        # Núcleo de Banco y Orquestador
        self.banco = KuzofinumCoreWeb3()
        self.mia = OrquestadorConvergencia()
        self.estado_red = {"volumen_total": 0.0}
        logging.info("Núcleo convergido y operativo.")

    def recibir_input_colmena(self, paquete_comprimido):
        """
        Punto de entrada de datos desde el repetidor.
        Descomprime, analiza y ejecuta bajo protocolo de fricción cero.
        """
        try:
            # 1. Descompresión de datos (Fricción Cero)
            data_json = zlib.decompress(paquete_comprimido).decode('utf-8')
            payload = json.loads(data_json)
            
            # 2. Ingesta al Ledger
            monto = payload.get("valor", 0.0)
            self.estado_red["volumen_total"] += monto
            logging.info(f"Ingesta de datos: +${monto:.4f} | Total: ${self.estado_red['volumen_total']:.4f}")
            
            # 3. Convergencia Dual (MIA decide si actuamos)
            if self.estado_red["volumen_total"] > 1.0: # Umbral de ejecución
                orden = "INYECCION_LIQUIDEZ_BLOCKCHAIN"
                decision = self.mia.converger(orden)
                
                # 4. Ejecución del Banco (Kuzofinum)
                if "Ejecutar" in decision:
                    self.banco.procesar_flujo_cuadrilla(self.estado_red["volumen_total"])
                    self.estado_red["volumen_total"] = 0.0 # Reset tras inyección
                    logging.info("Ciclo de inyección exitoso.")
                    
        except Exception as e:
            logging.error(f"Error en flujo de convergencia: {e}")

# Ejecución en el Hub
if __name__ == "__main__":
    control = SYXSOF_Main_Control()
    # Este proceso escucha el repetidor y dispara el banco
