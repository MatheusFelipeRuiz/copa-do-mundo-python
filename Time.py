from dataclasses import dataclass;

@dataclass
class Time:
    _nome: str;
    _codigo: int;
    @property
    def nome(self) -> str:
        return self._nome;
    @property
    def codigo(self) -> int:
        return self._codigo;
    def __repr__(self) -> str:
        return f'Nome do Time: {self.nome} - Sigla: {self.codigo}';