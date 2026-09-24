"""Share links and the guest (shared) profile view."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from .common import BaseContractModel, SharePermission, ShareRole
from .version import SCHEMA_VERSION


class ShareLink(BaseContractModel):
    """A shareable link letting a guest view selected sections of a profile."""

    schema_version: str = SCHEMA_VERSION
    token: str
    role: ShareRole
    label: str | None = None
    permissions: list[SharePermission] = Field(default_factory=list)
    active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SharedProfile(BaseContractModel):
    """Read-only view exposed to a guest through a share link."""

    schema_version: str = SCHEMA_VERSION
    owner_display_name: str
    owner_photo_url: str | None = None
    role: ShareRole
    permissions: list[SharePermission] = Field(default_factory=list)
    updated_at: datetime | None = None
    profile: dict[str, Any] | None = None
    timeline: dict[str, Any] | None = None
    routine: dict[str, Any] | None = None
    calendar: dict[str, Any] | None = None
    machines: list[Any] | None = None
    loads: list[Any] | None = None
    supplements: list[Any] | None = None


__all__ = ["ShareLink", "SharedProfile"]
