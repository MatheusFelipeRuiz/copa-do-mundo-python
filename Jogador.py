from dataclasses import dataclass;
from Gol import Gol;
@dataclass
class Jogador:
    _nome: str;
    _gols: list[Gol];

    @property
    def nome(self) -> str:
        return self._nome;
    @property
    def gols(self) -> list[Gol]:
        return self._gols;