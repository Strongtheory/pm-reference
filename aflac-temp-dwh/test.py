from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank

from diagrams.k8s.compute import Deployment, Pod

with Diagram("Diagram", show=False):
    with Cluster("First"):
        app_1 = Pod('App 1')
        app_2 = Pod('App 2')
        # app_1_pods = [
        #     Pod('App 1'),
        #     Pod('App 1'),
        #     Pod('App 1')
        # ]

    with Cluster("Second"):
        bapp_1 = Pod('bApp 1')
        bapp_2 = Pod('bApp 2')
        # app_2_pods = [
        #     Pod('App 2'),
        #     Pod('App 2'),
        #     Pod('App 2')
        # ]

    # sample = Blank("Hello World")

    app_1 - Edge(penwidth="0") - app_2
    bapp_1 - Edge(penwidth="0") - bapp_2

    # app_1 >> bapp_1
    # app_1 >> bapp_2
    # app_2 >> bapp_1
    # app_2 >> bapp_2

    # bapp_2 >> sample

    # for pod in app_1_pods:
    #     pod >> app_2_pods

