from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.onprem.analytics import Tableau
from diagrams.custom import Custom

from diagrams.aws.general import GenericDatabase, GenericFirewall

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

            # Data Integration
            with Cluster("Data Integration"):
                with Cluster("Cloud Environment"):
                    etl_service = GenericFirewall("ETL Service")

            # Data Storage & Aggregation
            with Cluster("Data Storage & Aggregation"):
                with Cluster("Cloud Environment"):
                    with Cluster("DWH Service"):
                        with Cluster("Production\nData Area"):
                            prd_dwh_db = GenericDatabase("")

                        with Cluster("User processing\ninformation (Sanbox)"):
                            user_created_dwh_db = GenericDatabase(
                                "User Created Data\n*About 6000TBL"
                            )

                    with Cluster("JUMP\n(For analysis * business)"):
                        jump_dwh = GenericDatabase("JUMP")
                        user_data_jump_dwh = GenericDatabase("User Created\nData")

                    with Cluster("ODS (For business)"):
                        ods_dwh = GenericDatabase("ODS")

                with Cluster("Other DBMS"):
                    with Cluster("ODS\n(For business)"):
                        other_ods_db = GenericDatabase("ODS\n* on-premise,\nSFDC,\nAzure, AWS")

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
        # (
        #     amps_server
        #     - Edge(penwidth="0")
        #     - xanet_server
        #     - Edge(penwidth="0")
        #     - ace_server
        #     - Edge(penwidth="0")
        #     - other_server
        # )

        # Data Consumers
        # first_users - Edge(penwidth="0") - second_users
        # third_users - Edge(penwidth="0") - fourth_users

        # Data Source -> Data Integration Connections
        mf_3 >> Edge(ltail="cluster_Mainframe (IBM DB2)", minlen="4") >> etl_service

        op_4 >> Edge(ltail="cluster_Open Platform", minlen="4") >> etl_service

        sfdc_2 >> Edge(ltail="cluster_Cloud Platform (SFDC)", minlen="4") >> etl_service

        # Data Source -> Data Storage & Aggregation
        (
            client_1
            >> Edge(ltail="cluster_Client (Flatfiles)", style="dotted", minlen="4")
            >> user_created_dwh_db
        )

        (
            client_1
            >> Edge(ltail="cluster_Client (Flatfiles)", style="dotted", minlen="4")
            >> user_data_jump_dwh
        )

        # Data Integration -> Data Storage & Aggregation
        etl_service >> Edge(minlen="4") >> prd_dwh_db
        etl_service >> Edge(minlen="4") >> jump_dwh
        etl_service >> Edge(minlen="4") >> ods_dwh
        etl_service >> Edge(minlen="4") >> other_ods_db

        # Data Storage & Aggregation -> Data Access & Delivery
        (
            prd_dwh_db
            >> Edge(
                lhead="cluster_Analytical data interface",
                ltail="cluster_Production\nData Area",
                minlen="4",
            )
            >> cognos_icon
        )
        prd_dwh_db >> Edge(minlen="4") >> amps_server
        prd_dwh_db >> Edge(minlen="4") >> xanet_server

        (
            user_created_dwh_db
            >> Edge(
                lhead="cluster_Analytical data interface",
                ltail="cluster_User processing\ninformation (Sanbox)",
                minlen="4",
            )
            >> cognos_icon
        )

        jump_dwh >> Edge(minlen="4") >> jump_server
        jump_dwh >> Edge(minlen="4") >> amps_server

        ods_dwh >> Edge(minlen="4") >> xanet_server

        other_ods_db >> Edge(minlen="4") >> amps_server
        other_ods_db >> Edge(minlen="4") >> xanet_server
        other_ods_db >> Edge(minlen="4") >> ace_server
        other_ods_db >> Edge(minlen="4") >> other_server

        # Data Access & Delivery -> Data Consumers
        (
            tableau_icon
            >> Edge(ltail="cluster_Analytical data interface", minlen="4")
            >> first_users
        )

        jump_server >> Edge(minlen="4") >> second_users
        amps_server >> Edge(minlen="4") >> second_users

        xanet_server >> Edge(minlen="4") >> third_users

        other_server >> Edge(minlen="4") >> first_users
        other_server >> Edge(minlen="4") >> second_users
        other_server >> Edge(minlen="4") >> third_users
        other_server >> Edge(minlen="4") >> fourth_users


if "__main__" == __name__:
    main()
