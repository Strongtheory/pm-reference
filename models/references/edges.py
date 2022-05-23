from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

from diagrams.custom import Custom


with Diagram(name="Advanced Web Service with On-Premise (colored)", show=False):
    ingress = Nginx("ingress")

    metrics = Prometheus("metric")
    metrics << Edge(color="firebrick", style="dashed") << Grafana("monitoring")

    with Diagram("Custom", show=False, filename="custom_local", direction="LR"):
        cc_heart = Custom("Creative Commons", "./my_resources/cc_heart.black.png")
        cc_attribution = Custom("Credit must be given to the creator", "./my_resources/cc_attribution.png")

        cc_sa = Custom("Adaptations must be shared\n under the same terms", "./my_resources/cc_sa.png")
        cc_nd = Custom("No derivatives or adaptations\n of the work are permitted", "./my_resources/cc_nd.png")
        cc_zero = Custom("Public Domain Dedication", "./my_resources/cc_zero.png")

        with Cluster("Non Commercial"):
            non_commercial = [
                Custom("Y", "./my_resources/cc_nc-jp.png") -
                Custom("E", "./my_resources/cc_nc-eu.png") -
                Custom("S", "./my_resources/cc_nc.png")
            ]

        cc_heart >> cc_attribution
        cc_heart >> non_commercial
        cc_heart >> cc_sa
        cc_heart >> cc_nd
        cc_heart >> cc_zero

    with Cluster("Service Cluster"):
        grpcsvc = [
            Server("grpc1"),
            Server("grpc2"),
            Server("grpc3")]

    with Cluster("Sessions HA"):
        primary = Redis("session")
        primary \
            - Edge(color="brown", style="dashed") \
            - Redis("replica") \
            << Edge(label="collect") \
            << metrics
        grpcsvc >> Edge(color="brown") >> primary

    with Cluster("Database HA"):
        primary = PostgreSQL("users")
        primary \
            - Edge(color="brown", style="dotted") \
            - PostgreSQL("replica") \
            << Edge(label="collect") \
            << metrics
        grpcsvc >> Edge(color="black") >> primary

    aggregator = Fluentd("logging")
    aggregator \
        >> Edge(label="parse") \
        >> Kafka("stream") \
        >> Edge(color="black", style="bold") \
        >> Spark("analytics")

    ingress \
        >> Edge(color="darkgreen") \
        << grpcsvc \
        >> Edge(color="darkorange") \
        >> aggregator
