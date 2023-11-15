from dataclasses import dataclass;
@dataclass
class Gol:
    _jogador: str;
    @property
    def jogador(self) -> str:
        return self._jogador;
    def __repr__(self) -> str:
        return f'Nome jogador = {self.jogador}, Minuto = {self.minuto}\n';