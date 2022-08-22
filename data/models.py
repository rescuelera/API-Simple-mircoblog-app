from dataclasses import field
from typing import Optional
from faker import Faker

from pydantic.dataclasses import dataclass

fake = Faker()


@dataclass
class CreateMicroblogBody:
    owner: int
    title: str = field(default_factory=lambda: fake.pystr(12))
    text: str = field(default_factory=lambda: fake.pystr(12))


@dataclass
class CreateUserBody:
    name: str= field(default_factory=lambda: fake.pystr(12))
    email: str = field(default_factory=lambda: fake.email(domain="yopmail.com"))
    password: str = field(default_factory=lambda: fake.password(12, special_chars=True))
