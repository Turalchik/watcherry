from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.programming.framework import Vue
from diagrams.programming.framework import Django
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.generic.storage import Storage

with Diagram("Watcherry Deployment", show=True):
    user = User("User")
    frontend = Vue("Vue.js Frontend")  
    backend = Django("Django Backend")     
    docker = Docker("Docker")              
    data = Storage("TSV Files")

    user >> docker
    docker >> frontend
    docker >> backend
    docker >> data


#    user >> frontend >> backend >> data
