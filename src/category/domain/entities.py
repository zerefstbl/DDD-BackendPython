from datetime import datetime
from typing import Optional

from __seedwork.domain.value_objects import UniqueEntityId

from dataclasses import dataclass, field

import uuid

@dataclass(kw_only=True, frozen=True)
class Category:
  
    id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId()
    )
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )
  
 