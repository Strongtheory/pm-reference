from logging import logThreads
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.onprem.analytics import Tableau
from diagrams.custom import Custom

GRAPH_ATTRIBUTES = {
    "layout": "dot",
    "compound": "true",
    # "splines": "spline",
}

COGNOS_ICON = "./images/cognos-icon.png"
SAP_BO_ICON = "./images/sap-bo-icon.png"
BA_SERVER_ICON = "./images/ba-server.png"

USERS_ICON = "./images/users.png"

DWH_CLOUD_SERVER_ICON = "./images/dwh-cloud-db.png"
ETL_CLOUD_SERVER_ICON = "./images/etl-cloud-server.png"

ON_PREMISE_DB_ICON = "./images/on-premise-db.png"
OUTSIDE_DB_ICON = "./images/outside-db.png"


def main():
    with Diagram(
        "ToBe Model",
        show=False,
        graph_attr=GRAPH_ATTRIBUTES,
        outformat="png",
        filename="test",
    ):
        with Cluster("Template"):
            # Data Source
            with Cluster("Data Source"):
                with Cluster("Mainframe (IBM DB2)"):
                    mf_1 = Rack("Securities")
                    mf_2 = Rack("Customer")
                    mf_3 = Rack(". . .")

                with Cluster("Open Platform"):
                    op_1 = Rack("AANET")
                    op_2 = Rack("CANET")
                    op_3 = Rack("OHP")
                    op_4 = Rack(". . .")

                with Cluster("Cloud Platform (SFDC)"):
                    sfdc_1 = Rack("SLM")
                    sfdc_2 = Rack(". . .")

                with Cluster("Client (Flatfiles)"):
                    client_1 = Rack("User Created\nData")

            # Data Integration
            with Cluster("Data Integration"):
                with Cluster("Cloud Environment"):
                    etl_service = Storage("ETL Service")

            # Data Storage & Aggregation
            with Cluster("Data Storage & Aggregation"):
                with Cluster("Cloud Environment"):
                    with Cluster("DWH Service"):
                        with Cluster("Production\nData Area"):
                            prd_dwh_db = Storage("")

                        with Cluster("User processing\ninformation (Sanbox)"):
                            user_created_dwh_db = Storage(
                                "User Created Data\n*About 6000TBL"
                            )

                    with Cluster("JUMP\n(For analysis * business)"):
                        jump_dwh = Storage("JUMP")
                        user_data_jump_dwh = Storage("User Created\nData")

                    with Cluster("ODS (For business)"):
                        ods_dwh = Storage("ODS")

                with Cluster("Other DBMS"):
                    with Cluster("ODS\n(For business)"):
                        other_ods_db = Storage("ODS\n* on-premise,\nSFDC,\nAzure, AWS")

            # Data Access & Delivery
            with Cluster("Data Access & Delivery"):
                with Cluster("Analytical data interface"):
                    cognos_icon = Custom("", COGNOS_ICON)
                    tableau_icon = Tableau("")

                with Cluster("Business application"):
                    sap_bo_icon = Custom("", SAP_BO_ICON)

                    jump_server = Custom("JUMP\n* on-premise", BA_SERVER_ICON)
                    amps_server = Custom("AMPS\n* .NET Application", BA_SERVER_ICON)
                    xanet_server = Custom("xANET\n* on-premise, SFDC", BA_SERVER_ICON)
                    ace_server = Custom("ACE\n* SFDC", BA_SERVER_ICON)
                    other_server = Custom("Other", BA_SERVER_ICON)

            # Data Consumers
            with Cluster("Data Consumers"):
                first_users = Custom(
                    "Staff department\nYusa department,\netc.", USERS_ICON
                )
                second_users = Custom("Sales section\nbranch office", USERS_ICON)
                third_users = Custom("Sales Division\nBranch Agency", USERS_ICON)
                fourth_users = Custom("Call Center", USERS_ICON)

        ## Connections

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

        # Analytical Data Inteface
        cognos_icon - Edge(penwidth="0") - tableau_icon

        # Business Application
        jump_server - Edge(penwidth="0") - sap_bo_icon

        # Data Source -> Data Integration Connections
        mf_3 >> Edge(ltail="cluster_Mainframe (IBM DB2)") >> etl_service

        op_4 >> Edge(ltail="cluster_Open Platform") >> etl_service

        sfdc_2 >> Edge(ltail="cluster_Cloud Platform (SFDC)") >> etl_service

        # Data Source -> Data Storage & Aggregation
        (
            client_1
            >> Edge(ltail="cluster_Client (Flatfiles)", style="dotted")
            >> user_created_dwh_db
        )

        (
            client_1
            >> Edge(ltail="cluster_Client (Flatfiles)", style="dotted")
            >> user_data_jump_dwh
        )

        # Data Integration -> Data Storage & Aggregation
        etl_service >> prd_dwh_db
        etl_service >> jump_dwh
        etl_service >> ods_dwh
        etl_service >> other_ods_db

        # Data Storage & Aggregation -> Data Access & Delivery
        (
            prd_dwh_db
            >> Edge(
                lhead="cluster_Analytical data interface",
                ltail="cluster_Production\nData Area",
            )
            >> cognos_icon
        )
        (
            user_created_dwh_db
            >> Edge(
                lhead="cluster_Analytical data interface",
                ltail="cluster_User processing\ninformation (Sanbox)",
            )
            >> cognos_icon
        )

        # Data Access & Delivery -> Data Consumers
        tableau_icon >> Edge(ltail="cluster_Analytical data interface") >> first_users


if "__main__" == __name__:
    main()
