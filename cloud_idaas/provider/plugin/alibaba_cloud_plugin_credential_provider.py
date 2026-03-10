import logging

from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_eiam20211201.client import Client
from alibabacloud_eiam20211201.models import (
    GenerateOauthTokenRequest,
    GenerateOauthTokenResponse,
)
from alibabacloud_tea_openapi.models import Config
from Tea.exceptions import TeaException

from cloud_idaas.core import (
    ClientException,
    ConfigException,
    CredentialException,
    ErrorCode,
    IDaaSCredentialProviderFactory,
    IDaaSTokenResponse,
    PluginCredentialProvider,
    ScopeUtil,
    ServerException,
)
from cloud_idaas.provider.plugin.audience_scope import AudienceScope

logger = logging.getLogger(__name__)


class AlibabaCloudPluginCredentialProvider(PluginCredentialProvider):
    def get_idaas_credential(self, scope: str) -> IDaaSTokenResponse:
        audience_scope = self._convert_scope(scope)
        credential = CredentialClient()
        config = Config()
        config.endpoint = IDaaSCredentialProviderFactory.get_openapi_endpoint()
        config.credential = credential

        try:
            client = Client(config)
            request = GenerateOauthTokenRequest()
            request.instance_id = IDaaSCredentialProviderFactory.get_idaas_instance_id()
            request.application_id = IDaaSCredentialProviderFactory.get_client_id()
            request.audience = audience_scope.audience
            request.scope_values = audience_scope.scope_values

            response: GenerateOauthTokenResponse = client.generate_oauth_token(request)
            token_response = response.body.token_response
            return self._convert_idaas_token_response(token_response)
        except TeaException as e:
            status_code = e.status_code
            code = e.code
            message = e.message
            request_id = e.data.get("RequestId") if e.data else None

            if status_code and 400 <= status_code < 500:
                logger.error("Client Error: code=%s, message=%s, request_id=%s", code, message, request_id)
                raise ClientException(code, message, request_id) from e
            elif status_code and status_code >= 500:
                logger.error("Server Error: code=%s, message=%s, request_id=%s", code, message, request_id)
                raise ServerException(code, message, request_id) from e
            else:
                logger.error("Error Message: %s", message)
                raise e
        except Exception as e:
            logger.error("Error Message: %s", str(e))
            raise CredentialException(error_message=str(e), cause=e) from e

    def _convert_scope(self, scopes: str) -> AudienceScope:
        scope_list = ScopeUtil.split_scope(scopes)
        audiences = set()
        scope_values = set()

        for scope in scope_list:
            if not ScopeUtil.is_valid_scope(scope):
                raise ConfigException(
                    ErrorCode.INVALID_SCOPE,
                    f"Invalid scope: {scope}",
                )
            scope_split = scope.split("|")
            if len(scope_split) != 2:
                raise ConfigException(
                    ErrorCode.INVALID_SCOPE,
                    f"Invalid scope format: {scope}, expected 'audience|scope_value'",
                )
            audiences.add(scope_split[0])
            scope_values.add(scope_split[1])

        if len(audiences) > 1:
            raise ConfigException(
                ErrorCode.MULTIPLE_AUDIENCE_NOT_SUPPORTED,
                "Multiple Audience is not supported",
            )

        audience_scope = AudienceScope()
        audience_scope.audience = next(iter(audiences))
        audience_scope.scope_values = list(scope_values)
        return audience_scope

    def _convert_idaas_token_response(self, token_response) -> IDaaSTokenResponse:
        idaas_token_response = IDaaSTokenResponse()
        idaas_token_response.access_token = token_response.access_token
        idaas_token_response.expires_in = token_response.expires_in
        idaas_token_response.expires_at = token_response.expires_at
        return idaas_token_response
