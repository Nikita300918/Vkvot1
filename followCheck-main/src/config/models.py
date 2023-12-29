from pydantic import BaseModel


class _Bot(BaseModel):
    token: str
    id: int


class _User(BaseModel):
    token: str
    id: int


class ConfigModel(BaseModel):
    bot: _Bot
    user: _User
