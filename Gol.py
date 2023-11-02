from dataclasses import dataclass;
@dataclass
class Gol:
    _jogador: str;
    _minuto: str;
    @property
    def jogador(self) -> str:
        return self._jogador;
    @property
    def minuto(self) -> str:
        return f'{self._minuto}min' ;
    def __repr__(self) -> str:
        return f'Nome jogador = {self.jogador}, Minuto = {self.minuto}\n';