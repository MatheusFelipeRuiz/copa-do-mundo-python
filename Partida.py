from dataclasses import dataclass;
from Time import Time;
from datetime import datetime;

@dataclass
class Partida:
    _id: int
    _mandante: Time;
    _visitante: Time;
    _gols_mandante: int;
    _gols_visitante: int;
    _data: str;
    _cidade: str;
    _estadio: str;
    _hora: str;

    @property
    def mandante(self) -> Time:
        return self._mandante;
    @property
    def visitante(self) -> Time:
        return self._visitante;
    @property
    def gols_mandante(self)-> int:
        return self._gols_mandante;
    @property
    def gols_visitante(self) -> int:
        return self._gols_visitante;
    @property
    def data(self) -> str:
        return f"{datetime.strptime(self._data,format('%Y-%m-%d')).strftime('%d/%m/%Y')}";
    @property
    def hora(self) -> str:
        return f'{self._hora}h';
    @property
    def cidade(self) -> str:
        return f'{self._cidade}';
    @property
    def estadio(self) -> str:
        return f'{self._estadio}';
    def informacoes_partida(self) -> None:
        print(f'Time mandante: {self.mandante.nome}');
        print(f'Time Visitante: {self.visitante.nome}');
        print(f'Quantidade de gols Mandante: {self.gols_mandante}');
        print(f'Quantidade de gols Visitante: {self.gols_visitante}');
        print(f'Data da partida: {self.data}');
        print(f'Horário: {self.hora}');
        print(f'Cidade: {self.cidade}');
        print(f'Estádio: {self.estadio}');
        print('=-' * 50);