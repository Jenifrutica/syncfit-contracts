"""Directed State Graph of physiological states."""

from __future__ import annotations

from pydantic import Field

from .common import BaseContractModel, PhysiologicalState, StateTransition
from .version import SCHEMA_VERSION


class PhysiologicalStateGraph(BaseContractModel):
    schema_version: str = SCHEMA_VERSION
    nodes: list[PhysiologicalState] = Field(min_length=1)
    edges: list[StateTransition] = Field(default_factory=list)


__all__ = ["PhysiologicalStateGraph"]
