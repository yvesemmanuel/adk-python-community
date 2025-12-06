# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Registry integration for ADK community services."""


def register_community_services():
    """Register community-provided services with the ADK service registry."""
    try:
        from google.adk.cli.service_registry import get_service_registry
    except ImportError:
        # ADK not installed or service registry not available
        return

    registry = get_service_registry()

    def redis_session_factory(uri: str, **kwargs):
        """Factory function to create RedisSessionService from URI.

        Parameters:
        -----------
        uri: Redis connection URI (e.g., redis://localhost:6379)
        **kwargs: Additional arguments passed to RedisSessionService

        Returns:
        --------
        RedisSessionService: Configured Redis session service instance
        """
        from google.adk_community.sessions import RedisSessionService

        kwargs_copy = kwargs.copy()
        kwargs_copy.pop("agents_dir", None)
        return RedisSessionService(uri=uri, **kwargs_copy)

    registry.register_session_service("redis", redis_session_factory)
