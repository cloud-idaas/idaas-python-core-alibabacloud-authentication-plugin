# cloud-idaas-core-alibabacloud-authentication-plugin

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-Beta-orange)](https://pypi.org/project/cloud-idaas-core-alibabacloud-authentication-plugin/)

Authentication plugin for IDaaS (Identity as a Service) core SDK, providing Alibaba Cloud EIAM integration for machine-to-machine authentication.

## Features

- **Alibaba Cloud EIAM Integration**: Seamlessly integrates with Alibaba Cloud EIAM service for OAuth2 token generation
- **Plugin Architecture**: Implements the `PluginCredentialProvider` interface from `cloud-idaas-core`
- **Automatic Registration**: Auto-registers as a plugin via entry points configuration

## Requirements

- Python >= 3.9
- Dependencies:
  - cloud-idaas-core >= 0.0.2b0
  - alibabacloud_eiam20211201 >= 2.13.2

## Installation

```bash
pip install cloud-idaas-core-alibabacloud-authentication-plugin
```

## Quick Start

### 1. Configuration File

Create a configuration file `~/.cloud_idaas/client_config.json`:

```json
{
    "idaasInstanceId": "your-idaas-instance-id",
    "clientId": "your-client-id",
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PLUGIN",
        "pluginName": "alibabacloudPluginCredentialProvider"
    }
}
```

### 2. Use in code

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory

# Initialize (automatically loads configuration file)
IDaaSCredentialProviderFactory.init()

# Get credential provider
credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider()

# Get access token
access_token = credential_provider.get_bearer_token()
print(f"Access Token: {access_token}")
```

## Configuration Details

### Complete Configuration Example

```json
{
    "idaasInstanceId": "idaas_xxx",
    "clientId": "app_xxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PLUGIN",
        "pluginName": "alibabacloudPluginCredentialProvider"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### Configuration Items

| Configuration Item | Type | Required | Description |
|-------------------|------|----------|-------------|
| idaasInstanceId | string | Yes | IDaaS instance ID |
| clientId | string | Yes | Client ID for authentication |
| issuer | string | Yes | OAuth2 issuer URL |
| tokenEndpoint | string | Yes | OAuth2 token endpoint URL |
| scope | string | No | Requested scope  |
| openApiEndpoint | string | Yes | Alibaba Cloud EIAM OpenAPI endpoint |
| authnConfiguration | object | Yes | Authentication configuration |
| httpConfiguration | object | No | HTTP client configuration |

### Plugin Configuration

To use this plugin, set the `authnMethod` to `PLUGIN` and specify the plugin name:

```json
{
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PLUGIN",
        "pluginName": "alibabacloudPluginCredentialProvider"
    }
}
```

## Support and Feedback

- **Email**: cloudidaas@list.alibaba-inc.com
- **Issues**: Please submit an Issue for questions or suggestions

## License

This project is licensed under the [Apache License 2.0](LICENSE).