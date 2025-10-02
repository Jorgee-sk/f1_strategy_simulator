# F1 Strategy Simulator

## 🎯 Objetivo
Este proyecto busca crear un **simulador estratégico de Fórmula 1** que reproduzca el trabajo de un *race strategist* usando inteligencia artificial y modelos matemáticos.  
La meta es minimizar el tiempo total de carrera y/o maximizar la probabilidad de victoria, considerando degradación de neumáticos, eventos dinámicos (Safety Car / Virtual Safety Car, lluvia) y decisiones de rivales.

## 🚦 Características previstas
- **Simulación discreta de carrera**: vuelta a vuelta con estados `{lap, compound, wear, fuel, weather, gaps}`.  
- **Modelado de neumáticos**: degradación no lineal, con fases de caída inicial, meseta y “cliff”.  
- **Eventos dinámicos**: SC y VSC estocásticos con impacto en gaps y ventanas de pit.  
- **Optimización de estrategia**:
  - Programación Dinámica (DP) para políticas reactivas.  
  - Algoritmos Genéticos (GA) para búsqueda global de planes.  
  - Aprendizaje por Refuerzo (RL) para decisiones online.  
- **Rivalidad estratégica**: undercut/overcut y efectos de tráfico.  
- **Monte Carlo**: evaluación de robustez bajo incertidumbre.  
- **Explicabilidad**: curvas de degradación, deltas de undercut, métricas de sensibilidad.

## 📊 Datos
Se emplearán datos históricos de Fórmula 1 (FastF1, Ergast API), incluyendo tiempos por vuelta, compuestos de neumático, duraciones de pit stops y eventos de carrera.

## 🛠️ Stack tecnológico
- **Python**: núcleo de simulación y modelos.  
- **FastF1**: ingestión de datos reales.  
- **NumPy / Pandas / SciPy**: análisis numérico.  
- **scikit-learn**: regresión robusta para calibración.  
- **DEAP**: algoritmos genéticos.  
- **PyTorch + Stable Baselines3**: RL (opcional en fases posteriores).  
- **Streamlit / Plotly**: visualización de estrategias.  
- **Pytest**: testing.  
- **Black + isort + flake8**: estilo y linting.

## 🚀 Roadmap (primeras fases)
1. Configuración del proyecto, ingestión de datos inicial (FastF1) y pipeline reproducible.  
2. Simulador básico vuelta a vuelta con pits y eventos SC/VSC.  
3. Modelado de degradación y calibración con datos reales.  
4. Búsqueda de estrategias con GA y DP.  
5. Interfaz de visualización para comparación de planes.  


## 👨‍💻 Autor
Jorge Galiano García