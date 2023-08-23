from datetime import datetime
from typing import Optional

from __seedwork.domain.entities import Entity

from dataclasses import dataclass, field

@dataclass(kw_only=True, frozen=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )
  
 