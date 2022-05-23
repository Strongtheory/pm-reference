from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom


GRAPH_ATTRIBUTES = {
    "fontsize": "45",
    "bgcolor": "transparent"
}

DB_ICON_LOCATION = "./images/dbicon.png"

DB_ICON = Custom("ICON NAME", DB_ICON_LOCATION)


def model():
    with Diagram(
        "Web Service",
        show=False,
        graph_attr=GRAPH_ATTRIBUTES,
        outformat="pdf",
        filename="asis"
    ):
        # Data Source
        with Cluster("Data Source"):
            # Mainframe Block
            with Cluster("Mainframe"):
                pass

            # Open Platform Block
            with Cluster("Open Platform"):
                pass

            # Client Block
            with Cluster("Client"):
                with Cluster("Client"):
                    pass
                pass

            # Cloud Platform Block
            with Cluster("Cloud Platform"):
                with Cluster("SFDC"):
                    pass
                pass

            pass

        # Data Integration
        with Cluster("Data Integration"):
            pass

        # Data Storage & Aggregation
        with Cluster("Data Storage and Aggregation"):
            pass

        # Data Access & Delivery
        with Cluster("Data Access & Delivery"):
            pass

        # Data Consumers
        with Cluster("Data Consumers"):
            pass


if "__main__" == __name__:
    model()
