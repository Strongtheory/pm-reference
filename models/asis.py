from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB


GRAPH_ATTRIBUTES = {
    "fontsize": "45",
    "bgcolor": "transparent"
}


def model():
    with Diagram(
        "Web Service",
        show=False,
        graph_attr=GRAPH_ATTRIBUTES,
        outformat="pdf",
        filename="asis"
    ):
        ELB("lb") >> EC2("web") >> RDS("userdb")


if "__main__" == __name__:
    model()
