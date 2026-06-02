import logging

logging.basicConfig(level=logging.INFO, format="[MIA-DUAL] 🧠 %(message)s")

class Hemisferio:
    def __init__(self, rol):
        self.rol = rol # 'LOGICO' o 'CREATIVO'
        
    def procesar(self, idea):
        if self.rol == 'LOGICO':
            return f"Analizando eficiencia y riesgo de: {idea}"
        return f"Explorando potencial de expansión y flujo de: {idea}"

class OrquestadorConvergencia:
    def __init__(self):
        self.hemisferio_logico = Hemisferio('LOGICO')
        self.hemisferio_creativo = Hemisferio('CREATIVO')

    def converger(self, idea_cruda):
        # Generamos las dos perspectivas
        logica = self.hemisferio_logico.procesar(idea_cruda)
        creativa = self.hemisferio_creativo.procesar(idea_cruda)
        
        # Convergencia: Aquí SOFI toma la decisión final basada en ambas
        logging.info(f"Convergencia iniciada para: {idea_cruda}")
        logging.info(f"PERSPECTIVA LOGICA: {logica}")
        logging.info(f"PERSPECTIVA CREATIVA: {creativa}")
        
        # Resultado convergente (La "verdad" operativa)
        decision = f"Ejecutar {idea_cruda} bajo protocolo de fricción cero."
        return decision

# Uso en el Sistema Maestro (SOFI v4.0)
if __name__ == "__main__":
    mia = OrquestadorConvergencia()
    # Ejemplo: Orden de inyectar capital para inflar S.Y.X.S.O.F
    orden = "Compra de S.Y.X.S.O.F mediante pool interno"
    resultado = mia.converger(orden)
    print(f"\nSOFI DECIDE: {resultado}")
