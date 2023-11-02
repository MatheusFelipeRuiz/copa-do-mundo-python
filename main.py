from dataclasses import dataclass
from datetime import datetime;
import requests;

from Gol import Gol
from Jogador import Jogador

resposta = requests.get('https://raw.githubusercontent.com/openfootball/worldcup.json/master/2018/worldcup.json').json();
@dataclass
class Time:
    _nome: str;
    _codigo: str;
    @property
    def nome(self) -> str:
        return self._nome;
    @property
    def codigo(self) -> str:
        return self._codigo;
    def __repr__(self) -> str:
        return f'Nome do Time: {self.nome} - Sigla: {self.codigo}';

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

PARTIDAS: list[Partida] = [];
GOLS: list[Gol] = [];
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
def carregar_partidas():
    qtde_rodadas: int = int(len(resposta['rounds']));
    for rodada in range(qtde_rodadas):
        dados_rodada = resposta['rounds'][rodada];
        qtde_partidas = len(dados_rodada['matches']);
        for partida in range(qtde_partidas):

            time1_nome: str = dados_rodada['matches'][partida]['team1']['name'];
            time1_codigo: str = dados_rodada['matches'][partida]['team1']['code'];

            time2_nome: str = dados_rodada['matches'][partida]['team2']['name'];
            time2_codigo: str = dados_rodada['matches'][partida]['team2']['code'];


            id: int = dados_rodada['matches'][partida]['num'];
            data_partida: str = dados_rodada['matches'][partida]['date'];
            mandante: Time = Time(time1_nome, time1_codigo);
            visitante: Time = Time(time2_nome, time2_codigo);
            gols_mandante: int = dados_rodada['matches'][partida]['score1'];
            gols_visitante: int = dados_rodada['matches'][partida]['score2'];
            cidade: str = dados_rodada['matches'][partida]['city'];
            estadio: str = dados_rodada['matches'][partida]['stadium']['name'];
            horario: str = dados_rodada['matches'][partida]['time'];
            partida: Partida = Partida(id, mandante, visitante, gols_mandante, gols_visitante,
                              data_partida,cidade,estadio, horario);
            PARTIDAS.append(partida);
def carregar_gols():
    qtde_rodadas: int = int(len(resposta['rounds']));
    for rodada in range(qtde_rodadas):
        dados_rodada = resposta['rounds'][rodada];
        qtde_partidas: int = len(dados_rodada['matches']);
        for partida in range(qtde_partidas):

            if 'goals1' in dados_rodada['matches'][partida]:
                if len(dados_rodada['matches'][partida]['goals1']) >  0:
                    gols_partida = dados_rodada['matches'][partida]['goals1'];
                    for gol_partida in  gols_partida:
                        nome_jogador = gol_partida['name'];
                        minuto_gol = gol_partida['minute'];
                        gol = Gol(nome_jogador, minuto_gol);
                        GOLS.append(gol);

            if 'goals2' in dados_rodada['matches'][partida]:
                if len(dados_rodada['matches'][partida]['goals2']) > 0:
                    gols_partida = dados_rodada['matches'][partida]['goals2'];
                    for gol_partida in gols_partida:
                        nome_jogador = gol_partida['name'];
                        minuto_gol = gol_partida['minute'];
                        gol = Gol(nome_jogador, minuto_gol);
                        GOLS.append(gol);
def partidas_carregadas():
    if len(PARTIDAS) == 0:
        carregar_partidas();
def consultar_por_selecao(codigo_selecao: str) -> None:
    partidas_carregadas();

    partidas_selecao: list[Partida] = [];
    for partida in PARTIDAS:
        if partida.mandante.codigo == codigo_selecao or partida.visitante.codigo == codigo_selecao:
            partidas_selecao.append(partida);
    for partida in partidas_selecao:
        partida.informacoes_partida();
def consultar_por_estadio(estadio: str) -> None:
    partidas_carregadas();

    partidas_estadio: list[Partida] = [];
    for partida in PARTIDAS:
        if partida.estadio == estadio:
            partidas_estadio.append(partida);
    for partida in partidas_estadio:
        partida.informacoes_partida();

def consulta_por_cidade(cidade: str) -> None:
    partidas_carregadas();

    partidas_cidade: list[Partida] = [];
    for partida in PARTIDAS:
        if partida.cidade == cidade:
            partidas_cidade.append(partida);
    for partida in partidas_cidade:
        partida.informacoes_partida();
def consultar_gols_jogador(jogador: str) -> None:
    if len(GOLS) == 0:
        carregar_gols();
    gols_jogador: list[Gol] = [];
    for gol in GOLS:
        if jogador in gol.jogador:
            gols_jogador.append(gol);
    jogador = Jogador(jogador, gols_jogador);
    print(jogador);



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

        time_mandante = Time(time1_nome,time1_sigla);
        time_visitante = Time(time2_nome, time2_sigla);

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
    # carregar_grupos();
    #consultar_por_selecao('BRA');
    # consultar_por_estadio('Luzhniki Stadium');
    # consulta_por_cidade('Moscow');
    # consultar_gols_jogador('Neymar');
    consultar_gols_jogador('Mbappé');
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