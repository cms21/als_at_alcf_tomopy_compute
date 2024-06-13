import os
import globus_sdk

from globus_sdk import (
    ClientCredentialsAuthorizer,
    ConfidentialAppAuthClient,
)

from globus_sdk.scopes import GCSCollectionScopeBuilder, MutableScope
from globus_sdk.tokenstorage import SimpleJSONFileAdapter

MY_FILE_ADAPTER = SimpleJSONFileAdapter(os.path.expanduser("~/.sdk-manage-flow.json"))

TRANSFER_ACTION_PROVIDER_SCOPE_STRING = (
    "https://auth.globus.org/scopes/actions.globus.org/transfer/transfer"
)


GLOBUS_CLIENT_ID = os.getenv("GLOBUS_CLIENT_ID")
GLOBUS_CLIENT_SECRET = os.getenv("GLOBUS_CLIENT_SECRET")




def do_login_flow(scopes, native_client):
    native_client.oauth2_start_flow(requested_scopes=scopes,
                                    refresh_tokens=True)
    authorize_url = native_client.oauth2_get_authorize_url()
    print(f"Please go to this URL and login:\n\n{authorize_url}\n")
    auth_code = input("Please enter the code here: ").strip()
    tokens = native_client.oauth2_exchange_code_for_tokens(auth_code)
    return tokens



def get_manage_flow_authorizer(client_id):
    # native_client = globus_sdk.NativeAppAuthClient(client_id)
    confidential_client = globus_sdk.ConfidentialAppAuthClient(
        client_id=GLOBUS_CLIENT_ID, client_secret=GLOBUS_CLIENT_SECRET
    )
    # resource_server = globus_sdk.FlowsClient.resource_server
    all_scopes = [
        globus_sdk.FlowsClient.scopes.manage_flows,
        globus_sdk.FlowsClient.scopes.run_status,
    ]
    return globus_sdk.ClientCredentialsAuthorizer(
        confidential_client,
        all_scopes)


def get_flows_client():
    # native_client = globus_sdk.NativeAppAuthClient(client_id)
    confidential_client = globus_sdk.ConfidentialAppAuthClient(
        client_id=GLOBUS_CLIENT_ID, client_secret=GLOBUS_CLIENT_SECRET
    )
    
    # resource_server = globus_sdk.FlowsClient.resource_server
    all_scopes = [
        globus_sdk.FlowsClient.scopes.manage_flows,
        globus_sdk.FlowsClient.scopes.run_status,
    ]
    authorizer = globus_sdk.ClientCredentialsAuthorizer(
        confidential_client,
        all_scopes)
    return globus_sdk.FlowsClient(authorizer=authorizer)


def get_specific_flow_client(flow_id, collection_ids=None):
    confidential_client = globus_sdk.ConfidentialAppAuthClient(
        client_id=GLOBUS_CLIENT_ID, client_secret=GLOBUS_CLIENT_SECRET
    )
    all_scopes = globus_sdk.SpecificFlowClient(flow_id).scopes
    all_scopes = all_scopes.make_mutable("user")
    assert collection_ids, "Why don't we have a collection id??"

    # Build a scope that will give the flow
    # access to specific mapped collections on your behalf
    transfer_scope = globus_sdk.TransferClient.scopes.make_mutable("all")
    transfer_action_provider_scope = MutableScope(
        TRANSFER_ACTION_PROVIDER_SCOPE_STRING
    )

    # If you declared and mapped collections above,
    # add them to the transfer scope
    for collection_id in collection_ids:
        gcs_data_access_scope = GCSCollectionScopeBuilder(
            collection_id
        ).make_mutable(
            "data_access",
            optional=True,
        )
        transfer_scope.add_dependency(gcs_data_access_scope)

    transfer_action_provider_scope.add_dependency(transfer_scope)
    all_scopes.add_dependency(transfer_action_provider_scope)
    authorizer = globus_sdk.ClientCredentialsAuthorizer(
            confidential_client,
            all_scopes)

    return globus_sdk.SpecificFlowClient(flow_id, authorizer=authorizer)
