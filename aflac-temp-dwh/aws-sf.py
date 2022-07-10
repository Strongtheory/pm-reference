from logging import logThreads
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.onprem.analytics import Tableau
from diagrams.custom import Custom

from diagrams.aws.network import DirectConnect
from diagrams.aws.general import GenericFirewall

GRAPH_ATTRIBUTES = {
    "layout": "dot",
    "compound": "true",
    # "splines": "spline",
}


def main():
    with Diagram(
        "AWS Snowflake Modell",
        show=False,
        graph_attr=GRAPH_ATTRIBUTES,
        outformat="png",
        filename="base",
    ):
        with Cluster("AWS Environment"):
            # Data Source
            with Cluster("Data Source"):
                with Cluster("Mainframe (IBM DB2)"):
                    mf_1 = Storage("Securities")
                    mf_2 = Storage("Customer")
                    mf_3 = Storage(". . .")

                with Cluster("Open Platform"):
                    op_1 = Storage("AANET")
                    op_2 = Storage("CANET")
                    op_3 = Storage("OHP")
                    op_4 = Storage(". . .")

                with Cluster("Cloud Platform (SFDC)"):
                    sfdc_1 = Storage("SLM")
                    sfdc_2 = Storage(". . .")

                with Cluster("Client (Flatfiles)"):
                    client_1 = Storage("User Created\nData")

        # Format Connection

        # Mainframe
        mf_1 - Edge(penwidth="0") - mf_2 - Edge(penwidth="0") - mf_3

        # Open Platform
        (
            op_1
            - Edge(penwidth="0")
            - op_2
            - Edge(penwidth="0")
            - op_3
            - Edge(penwidth="0")
            - op_4
        )

        # Cloud Platform
        sfdc_1 - Edge(penwidth="0") - sfdc_2


if "__main__" == __name__:
    main()
