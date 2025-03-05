from dataclasses import dataclass, field
from itertools import count
import datetime

@dataclass
class Task():
    description: str
    id: int = field(default_factory=count().__next__)
    status: str = "in-progress"
    createdAt: str = datetime.date.today().strftime("%Y-%m-%d")
    updatedAt: str = datetime.date.today().strftime("%Y-%m-%d")

    def __repr__(self):
        result = "{}) \"{}\", with status \"{}\", created {} and modified {}"\
        .format(self.id ,self.description, self.status, self.createdAt, self.updatedAt)
        return result