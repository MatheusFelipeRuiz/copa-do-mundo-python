from dataclasses import dataclass
import requests;

from Partida import Partida;
from Gol import Gol;
from Jogador import Jogador;
from Time import Time;

resposta = requests.get(
    'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2018/worldcup.json').json();

PARTIDAS: list[Partida] = [];
GOLS: list[Gol] = [];


@dataclass
class Grupo:
    _nome: str;
    _partidas: list[Partida];

    @property
    def nome(self) -> str:
        return self._nome;

    @property
    def partidas(self) -> list[Partida]:
        return self._partidas;

    def consultar_jogos_grupo(self):
        for partida in self.partidas:
            partida.informacoes_partida();

def carregar_grupo(grupo: str) -> list[int]:
    partidas_carregadas();
    qtde_rodadas: int = len(resposta['rounds']);
    identificador_partidas: list[int] = [];

    for rodada in range(qtde_rodadas):
        dados_rodada = resposta['rounds'][rodada];
        qtde_partidas: int = len(dados_rodada['matches']);
        for partida in range(qtde_partidas):
            if 'group' in dados_rodada['matches'][partida]:
                if grupo in dados_rodada['matches'][partida]['group']:
                    identificador_partidas.append(dados_rodada['matches'][partida]['num']);
    return identificador_partidas;
def carregar_rodada(rodada: int):
    partidas_carregadas();
    identificador_partidas: list[int] = [];
    qtde_partidas: int = len(resposta['rounds'][rodada]['matches']);
    for partida in range(qtde_partidas):
        id = int(resposta['rounds'][rodada]['matches'][partida]['num']);
        identificador_partidas.append(id);
    return identificador_partidas;


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
                                       data_partida, cidade, estadio, horario);
            PARTIDAS.append(partida);


def carregar_gols():
    qtde_rodadas: int = int(len(resposta['rounds']));
    for rodada in range(qtde_rodadas):
        dados_rodada = resposta['rounds'][rodada];
        qtde_partidas: int = len(dados_rodada['matches']);
        for partida in range(qtde_partidas):

            if 'goals1' in dados_rodada['matches'][partida]:
                if len(dados_rodada['matches'][partida]['goals1']) > 0:
                    gols_partida = dados_rodada['matches'][partida]['goals1'];
                    for gol_partida in gols_partida:
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


def consultar_por_selecao(codigo_selecao: str) -> bool:
    partidas_carregadas();

    partidas_selecao: list[Partida] = [];
    for partida in PARTIDAS:
        if partida.mandante.codigo == codigo_selecao or partida.visitante.codigo == codigo_selecao:
            partidas_selecao.append(partida);
    if len(partidas_selecao) > 0:
        for partida in partidas_selecao:
            partida.informacoes_partida();
        return True;
    return False;

def consultar_por_estadio(estadio: str) -> bool:
    partidas_carregadas();

    partidas_estadio: list[Partida] = [];
    for partida in PARTIDAS:
        if partida.estadio == estadio:
            partidas_estadio.append(partida);
    if len(partidas_estadio) > 0:
        for partida in partidas_estadio:
            partida.informacoes_partida();
        return True;
    return False;


def consulta_por_cidade(cidade: str) -> bool:
    partidas_carregadas();

    partidas_cidade: list[Partida] = [];
    for partida in PARTIDAS:
        if partida.cidade == cidade:
            partidas_cidade.append(partida);
    if len(partidas_cidade) > 0:
        for partida in partidas_cidade:
            partida.informacoes_partida();
        return True;
    return False;



def consultar_gols_jogador(jogador: str) -> bool:
    partidas_carregadas();
    if len(GOLS) == 0:
        carregar_gols();
    gols_jogador: list[Gol] = [];
    for gol in GOLS:
        if jogador in gol.jogador:
            gols_jogador.append(gol);
    if len(gols_jogador) > 0:
        jogador = Jogador(jogador, gols_jogador);
        print('=-' * 30);
        print(f'Nome do Jogador: {jogador.nome}');
        print(f'Quantidade de gols marcados: {len(jogador.gols)} gols');
        print('=-' * 30);
        return True;
    return False;

def consulta_rodadas(rodada: int):
    partidas_rodada: list[int] = carregar_rodada(rodada);
    qtde_partidas: int = len(partidas_rodada);
    print('=-' * 50);
    print(f'Quantidade de partidas na rodada: {qtde_partidas} partidas');
    print('=-' * 50);
    for partida in PARTIDAS:
        if partida.id in partidas_rodada:
            partida.informacoes_partida();
def consultar_por_grupo(grupo: str):
    partidas_carregadas();
    lista_id_partidas: list[int] = carregar_grupo(grupo);
    for partida in PARTIDAS:
        if partida.id in lista_id_partidas:
            partida.informacoes_partida();

def analistar_resultados():
    partidas_carregadas();
    qtde_vitorias_mandante: int = 0;
    qtde_vitorias_visitante: int = 0;
    qtde_empates: int = 0;
    for partida in PARTIDAS:
        gols_mandante: int = partida.gols_mandante;
        gols_visitante: int = partida.gols_visitante;

        if gols_mandante > gols_visitante:
            qtde_vitorias_mandante += 1;
        elif gols_visitante > gols_mandante:
            qtde_vitorias_visitante += 1;
        else:
            qtde_empates += 1;
    print('=-' * 30);
    print(f'Quantidade de vitórias mandante: {qtde_vitorias_mandante} vitórias');
    print(f'Quantidade de vitórias visitante: {qtde_vitorias_visitante} vitórias');
    print(f'Quantidade de empates: {qtde_empates} empates');
    print('=-' * 30);


def ler_rodada() -> int:
    return int(input()) - 1;


def menu_rodadas():
    print('Digite a fase que deseja mostrar de 1º a 20: ');
    print('1 a 15 - Fase de grupos ');
    print('16 - Oitavas de final');
    print('17 - Quartas de final');
    print('18 - Semifinal');
    print('19 - Disputa pelo terceiro lugar');
    print('20 - Final ');





def menu_principal():
    print('Menu Principal');
    print('1 - Consultar jogos por rodada ');
    print('2 - Consultar jogos por grupo ');
    print('3 - Consultar jogos por seleção ');
    print('4 - Consultar jogos por estádio ');
    print('5 - Consulta jogos por cidade ');
    print('6 - Consultar gols de determinado jogador');
    print('7 - Resultados copa do mundo');
    print('0 - Sair');


def main():
    opcao: int = -1;
    while opcao != 0:
        menu_principal();
        opcao = int(input('Escolha uma opção: '));
        if opcao == 0:
            break;
        elif opcao == 1:
            menu_rodadas();
            rodada: int = ler_rodada();
            consulta_rodadas(rodada);
        elif opcao == 2:
            grupo: str = input('Digite o grupo que deseja -  Ex: A,B,C : ');
            consultar_por_grupo(grupo);
        elif opcao == 3:
            selecao: str = '';
            while not consultar_por_selecao(selecao):
                selecao = input('Digite o código da seleção - Ex: BRA para Brasil : ');
                consultar_por_selecao(selecao);
        elif opcao == 4:
            estadio: str = '';
            while not consultar_por_estadio(estadio):
                estadio = input('Digite o nome do estádio: ');
                consultar_por_estadio(estadio);
        elif opcao == 5:
            cidade: str = '';
            while not consulta_por_cidade(cidade):
                cidade = input('Digite o nome da cidade: ');
                consultar_por_estadio(cidade);
        elif opcao == 6:
            nome_jogador: str = 'desconhecido';
            jogador_valido: bool = consultar_gols_jogador(nome_jogador);
            while not jogador_valido:
                nome_jogador = input('Digite o nome do jogador: ');
                jogador_valido = consultar_gols_jogador(nome_jogador);
        elif opcao == 7:
            analistar_resultados();


if __name__ == '__main__':
    main();
