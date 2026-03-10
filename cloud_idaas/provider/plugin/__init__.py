from cloud_idaas.provider.plugin.alibaba_cloud_plugin_credential_provider import (
    AlibabaCloudPluginCredentialProvider,
)
from cloud_idaas.provider.plugin.audience_scope import AudienceScope

# Version management - keep at the end, skip import sorting
from importlib import metadata  # isort: skip

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # avoids polluting the results of dir(__package__)

__author__ = "AlibabaCloud IDaaS Team"

__all__ = [
    "AlibabaCloudPluginCredentialProvider",
    "AudienceScope",
]
