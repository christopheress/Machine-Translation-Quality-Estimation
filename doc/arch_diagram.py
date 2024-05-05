from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker
from diagrams.custom import Custom

with Diagram("Technische MTQE Infrastruktur", show=False, direction="TB"):
    user = User("Benutzer")

    with Cluster("Docker Compose Services"):
        with Cluster("Streamlit Frontend App", graph_attr={"fontsize": "20", "fontname": "Sans-Serif"}):
            frontend = Docker("Streamlit App\nPort: 8501")
            preprocessing = Custom("Datenvorverarbeitung", "icons/data-preprocessing.png")
            model_processing = Custom("MTQE Modell Verarbeitung", "icons/model-processing-icon.png")
            analysis = Custom("MTQE Analyse", "icons/analysis-icon.png")
            frontend >> preprocessing >> model_processing >> analysis

        with Cluster("API Services", graph_attr={"fontsize": "20", "fontname": "Sans-Serif"}):
            transquest = Docker("TransQuest\nPort: 8001")
            openai_gpt = Docker("OpenAI GPT\nPort: 8002")
            cometkiwi = Docker("CometKiwi\nPort: 8003")

            model_processing >> transquest
            model_processing >> openai_gpt
            model_processing >> cometkiwi

    user >> frontend

