from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import DomainException


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

    def update(self, name: str, description: str) -> None:
        if not name and not description:
            raise DomainException()

        self._set('name', name)
        self._set('description', description)

    def activate(self) -> None:
        self._set('is_active', True)

    def deactivate(self) -> None:
        self._set('is_active', False)
