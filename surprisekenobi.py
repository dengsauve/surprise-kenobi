from typing import Optional, TypedDict
import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi import ResourceOptions


class SurpriseKenobiArgs(TypedDict):
    image_path: pulumi.Input[str]
    """The file path to the image you want to host"""


class SurpriseKenobi(pulumi.ComponentResource):
    endpoint: pulumi.Output[str]
    """The URL where you'll find Kenobi"""

    def __init__(self,
                 name: str,
                 args: Optional[SurpriseKenobiArgs] = None,
                 opts: Optional[ResourceOptions] = None) -> None:
        
        super().__init__('surprise-kenobi:index:SurpriseKenobi', name, {}, opts)

        # Create an Azure Resource Group
        resource_group = resources.ResourceGroup(
            f"{name}-rg",
            opts=ResourceOptions(parent=self))

        # Create an Azure resource (Storage Account)
        account = storage.StorageAccount(
            f"{name}-sa",
            account_name=f"{name}kenobisa",
            resource_group_name=resource_group.name,
            sku={
                "name": storage.SkuName.STANDARD_LRS,
            },
            kind=storage.Kind.STORAGE_V2,
            allow_blob_public_access=True,
            # enableHttpsTrafficOnly=False
            opts=ResourceOptions(parent=resource_group))

        # Create a Blob Container
        container = storage.BlobContainer(
            f"{name}-images-ctr-1",
            account_name=account.name,
            public_access=storage.PublicAccess.BLOB,
            resource_group_name=resource_group.name,
            opts=ResourceOptions(parent=resource_group))

        # Upload the JPEG image as a Blob
        blob = storage.Blob(
            f"{name}-image",
            resource_group_name=resource_group.name,
            account_name=account.name,
            container_name=container.name,
            type=storage.BlobType.BLOCK,
            source=pulumi.asset.FileAsset(args.get("image_path", "assets/helloThere.jpeg")),
            content_type="image/jpeg",
            opts=ResourceOptions(parent=resource_group))

        endpoint = pulumi.Output.concat(
            "https://", account.name, ".blob.core.windows.net/", container.name, "/", blob.name
        )

        self.endpoint = endpoint

        self.register_outputs({
            'endpoint': endpoint
        })