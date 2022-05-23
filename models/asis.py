from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom


GRAPH_ATTRIBUTES = {
    "layout":"dot",
    "compound":"true",
    "splines":"spline",
}

SQ_ICON_LOCATION = "./images/square.png"
DB_ICON_LOCATION = "./images/dbicon.png"

# DB_ICON = Custom("ICON NAME", DB_ICON_LOCATION)


def model():
    with Diagram(
        "DWH/ETL AsIsモデル",
        show=False,
        graph_attr=GRAPH_ATTRIBUTES,
        outformat="pdf",
        filename="test"
    ):
        with Cluster("Data Source"):
            with Cluster("Mainframe"):
                with Cluster("1"):
                    mf_contents = [
                        Custom("証券", DB_ICON_LOCATION),
                        Custom("顧客", DB_ICON_LOCATION),
                        Custom(". . .", DB_ICON_LOCATION)
                    ]

            with Cluster("Open Platform"):
                with Cluster("2"):
                    op_contents = [
                        Custom("AANET", DB_ICON_LOCATION),
                        Custom("CANET", DB_ICON_LOCATION),
                        Custom("OHP", DB_ICON_LOCATION),
                        Custom(". . .", DB_ICON_LOCATION)
                    ]

            # with Cluster("Client"):
            #     with Cluster("ユーザーデータ"):
            #         # Client[User Data] Block
            #         ud = Custom("ユーザー作成データ", DB_ICON_LOCATION)

            # with Cluster("Cloud Platform"):
            #     with Cluster("SFDC"):
            #         cp_contents = [
            #             Custom("SLM", DB_ICON_LOCATION),
            #             Custom(". . .", DB_ICON_LOCATION)
            #         ]

        with Cluster("Data Integration"):
            # ETL/PC
            etl_pc_sq = Custom("ETL/PowerCenter", SQ_ICON_LOCATION)

            # acc
            acc_sq = Custom(
                "Access Navigator WEB\n ※データ投入機能TERADATA",
                SQ_ICON_LOCATION
            )

            # TDP
            tdp_sq = Custom(
                "TERADATA TDP\n （チャネル接続）",
                SQ_ICON_LOCATION
            )

            # DataSpider
            # dsp_sq = Custom("DataSpider", SQ_ICON_LOCATION)

        Edge()

        mf_contents[1] >> Edge(ltail = "cluster_1") >> etl_pc_sq
        mf_contents[2] >> Edge(ltail = "cluster_1") >> tdp_sq

        op_contents[1] >> Edge(ltail = "cluster_2") >> etl_pc_sq

        # ud >> Edge(style="dotted") >> acc_sq
        # ud >> Edge(style="dotted") >> dsp_sq

        # cp_contents >> etl_pc_sq


if "__main__" == __name__:
    model()
