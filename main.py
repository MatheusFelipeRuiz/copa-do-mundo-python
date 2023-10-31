from dataclasses import dataclass
from datetime import datetime;
import requests;

resposta = requests.get('https://raw.githubusercontent.com/openfootball/worldcup.json/master/2018/worldcup.json').json();

@dataclass
class Time:

    _id: int;
    _nome: str;
    _sigla: str;

    @property
    def id(self) -> int:
        return self._id;
    @property
    def nome(self) -> str:
        return self._nome;
    @property
    def sigla(self) -> str:
        return self._sigla;


    def __str__(self) -> str:
        return f'Nome do Time: {self._nome} - Sigla: {self._sigla}';

@dataclass
class Partida:
    _id: int
    _mandante: Time;
    _visitante: Time;
    _gols_mandante: int;
    _gols_visitante: int;
    _data: str;
    _grupo: str;
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
    def grupo(self) -> str:
        return f"{self._grupo.replace('Group','').strip()}";
    @property
    def hora(self) -> str:
        return f'{self._hora}h';
    def informacoes_partida(self) -> None:
        print(f'Time mandante: {self._mandante.nome}');
        print(f'Time Visitante: {self._visitante.nome}');
        print(f'Quantidade de gols Mandante: {self.gols_mandante}');
        print(f'Quantidade de gols Visitante: {self.gols_visitante}');
        print(f'Data da partida: {self.data}');
        print(f'Grupo: {self.grupo}');
        print(f'Horário: {self.hora}')
        print('=-' * 50);
@dataclass
class Grupo:
    _id: int;
    _nome: str;
    _partidas: list[Partida];

    @property
    def id(self) -> int:
        return self._id;
    @property
    def nome(self) -> str:
        return self._nome;
    @property
    def partidas(self) -> list[Partida]:
        return self._partidas;

    def consultar_jogos_grupo(self):
        for partida in self.partidas:
            partida.informacoes_partida();

def carregar_grupos():
    qtde_rodadas = int(len(resposta['rounds']));
    count = 0;
    for rodada in range(qtde_rodadas):
        qtde_partidas = len(resposta['rounds'][rodada]['matches']);
        for partida in range(qtde_partidas):
            if 'group' in resposta['rounds'][rodada]['matches'][partida]:
                print(resposta['rounds'][rodada]['matches'][partida]['group']);
                count += 1;
    
def menu_rodadas():
    print('Digite a fase que deseja mostrar de 1º a 20: ');
    print('1 a 15 - Fase de grupos ');
    print('16 - Oitavas de final');
    print('17 - Quartas de final');
    print('18 - Semifinal');
    print('19 - Disputa pelo terceiro lugar');
    print('20 - Final ');
def consulta_rodadas(rodada: int):
    dados_partida = resposta['rounds'][rodada]['matches'];
    qtde_partidas_rodada = len(resposta['rounds'][rodada]['matches']);
    print('=-' * 50);
    print(f'Quantidade de partidas na rodada: {qtde_partidas_rodada} partidas');
    print('=-' * 50);

    for partida in range(qtde_partidas_rodada):
        time1_nome = dados_partida[partida]['team1']['name'];
        time1_sigla = dados_partida[partida]['team1']['code'];
        time1_gols = dados_partida[partida]['score1'];

        time2_nome = dados_partida[partida]['team2']['name'];
        time2_sigla = dados_partida[partida]['team2']['code'];
        time2_gols = dados_partida[partida]['score2'];

        time_mandante = Time(partida,time1_nome,time1_sigla);
        time_visitante = Time(partida,time2_nome, time2_sigla);

        data_partida = dados_partida[partida]['date'];
        grupo_copa = dados_partida[partida]['group'];
        hora_partida = dados_partida[partida]['time'];

        partida =  Partida(1,time_mandante,time_visitante,time1_gols,time2_gols,data_partida,grupo_copa,hora_partida);
        partida.informacoes_partida();
def menu_principal():
    print('Menu Principal');
    print('1 - Consultar jogos por fase ');
    print('2 - Consultar jogos por grupo ');
    print('3 - Consultar jogos por seleção ');
    print('4 - Consultar jogos por estádio ');
    print('5 - Consulta jogos por cidade ');
    print('6 - Consultar gols de determinado jogador');
    print('0 - Sair');
def main():
    carregar_grupos();
    # opcao = -1;
    #
    # while opcao != 0:
    #     menu_principal();
    #     opcao = int(input('Escolha de opção: '));
    #
    #     if opcao == 1:
    #         menu_rodadas();
    #         rodada = int(input('Digite a opção que deseja: ')) - 1;
    #         consulta_rodadas(rodada);
    #     elif opcao == 0:
    #         break;




if __name__ == '__main__':
    main();