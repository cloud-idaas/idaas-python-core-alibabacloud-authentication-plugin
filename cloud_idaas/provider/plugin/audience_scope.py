from typing import Optional


class AudienceScope:
    def __init__(self, audience: Optional[str] = None, scope_values: Optional[list[str]] = None):
        self._audience = audience
        self._scope_values = scope_values

    @property
    def audience(self):
        return self._audience

    @audience.setter
    def audience(self, audience: Optional[str]):
        self._audience = audience

    @property
    def scope_values(self):
        return self._scope_values

    @scope_values.setter
    def scope_values(self, scope_values: Optional[list[str]]):
        self._scope_values = scope_values
