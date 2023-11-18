import requests;
from Partida import Partida;
from Gol import Gol;
from Jogador import Jogador;
from Time import Time;

resposta = requests.get(
    'https://raw.githubusercontent.com/leandroflores/api-world-cup/main/results_2018').json();

PARTIDAS: list[Partida] = [];
GOLS: list[Gol] = [];

def criar_partida(partida: dict) -> Partida:
    time1_nome: str = partida['team1']['name'];
    time1_codigo: int = partida['team1']['code'];

    time2_nome: str = partida['team2']['name'];
    time2_codigo: int = partida['team2']['code'];

    id: int = partida['num'];
    data_partida: str = partida['date'];
    mandante: Time = Time(time1_nome, time1_codigo);
    visitante: Time = Time(time2_nome, time2_codigo);
    gols_mandante: int = partida['score1'];
    gols_visitante: int = partida['score2'];

    cidade: str = partida['city'];
    estadio: str = partida['stadium']['name'];
    horario: str = partida['time'];
    partida: Partida = Partida(id, mandante, visitante, gols_mandante, gols_visitante,
                               data_partida, cidade, estadio, horario);
    return partida;
def carregar_grupo(grupo: str) -> list[Partida]:
    partidas_carregadas();
    rodadas: list[dict] = resposta['rounds'];
    partidas_grupo: list[Partida] = [];

    for rodada in rodadas:
        partidas: list[dict] = rodada['matches'];
        for partida in partidas:
            if 'group' in partida:
                grupo_partida: str = partida['group'];
                if grupo in grupo_partida:
                    partidas_grupo.append(criar_partida(partida));
    return partidas_grupo;


def carregar_rodada(rodada: int) -> list[Partida]:
    partidas: list[dict] = resposta['rounds'][rodada]['matches'];
    partidas_rodada: list[Partida] = [];
    for partida in partidas:
        partidas_rodada.append(criar_partida(partida));
    return partidas_rodada;


def carregar_partidas() -> None:
    rodadas: list[dict] = resposta['rounds'];
    for rodada in rodadas:
        partidas: list[dict] = rodada['matches'];
        for partida_rodada in partidas:
            PARTIDAS.append(criar_partida(partida_rodada));

def carregar_gols() -> None:
    rodadas: list[dict] = resposta['rounds'];
    for rodada in rodadas:
        partidas: list[dict] = rodada['matches'];
        for partida in partidas:
            if 'goals1' in partida or 'goals2' in partida:
                partida['goals1'].extend(partida['goals2']);
                lista_gols: list[dict] = partida['goals1'];
                for gol in lista_gols:
                    nome_jogador: str = gol['name'];
                    gol: Gol = Gol(nome_jogador);
                    GOLS.append(gol);
def partidas_carregadas() -> None:
    if len(PARTIDAS) == 0:
        carregar_partidas();
def com_partidas(partidas: list[Partida]) -> bool:
    if len(partidas) > 0:
        informacoes_partida = lambda partida: partida.informacoes_partida();
        list(map(informacoes_partida,partidas));
        return True;
    return False;
def consultar_por_selecao(codigo_selecao: str) -> bool:
    partidas_carregadas();
    partidas_selecao: list[Partida] = list(
        filter(lambda partida: partida.mandante.codigo == codigo_selecao or partida.visitante.codigo == codigo_selecao,
         PARTIDAS)
    );
    return com_partidas(partidas_selecao);

def consultar_por_estadio(estadio: str) -> bool:
    partidas_carregadas();
    partidas_estadio: list[Partida] = list(
        filter(lambda partida: partida.estadio == estadio,PARTIDAS)
    );

    return com_partidas(partidas_estadio);


def consulta_por_cidade(cidade: str) -> bool:
    partidas_carregadas();

    partidas_cidade: list[Partida] = list(
        filter(lambda partida: partida.cidade == cidade,PARTIDAS)
    );
    return com_partidas(partidas_cidade);

def consultar_gols_jogador(jogador: str) -> bool:
    if len(GOLS) == 0:
        carregar_gols();

    gols_jogador: list[Gol] = list(
        filter(lambda gol: jogador in gol.jogador, GOLS)
    );

    if len(gols_jogador) > 0:
        jogador: Jogador = Jogador(jogador, gols_jogador);
        print('=-' * 30);
        print(f'Nome do Jogador: {jogador.nome}');
        print(f'Quantidade de gols marcados: {len(jogador.gols)} gols');
        print('=-' * 30);
        return True;
    return False;


def consulta_rodadas(rodada: int):
    partidas_rodada: list[Partida] = carregar_rodada(rodada);
    qtde_partidas: int = len(partidas_rodada);
    print('=-' * 50);
    print(f'Quantidade de partidas na rodada: {qtde_partidas} partidas');
    print('=-' * 50);
    com_partidas(partidas_rodada);

def consultar_por_grupo(grupo: str):
    lista_partidas: list[Partida] = carregar_grupo(grupo);
    com_partidas(lista_partidas);
def get_qtde_vitorias_mandante() -> int:
    qtde_vitorias_mandante: int = 0;
    for partida in PARTIDAS:
        if partida.gols_mandante > partida.gols_visitante:
            qtde_vitorias_mandante += 1;
    return qtde_vitorias_mandante;
def get_qtde_vitorias_visitante() -> int:
    qtde_vitorias_visitante: int = 0;
    for partida in PARTIDAS:
        if partida.gols_mandante < partida.gols_visitante:
            qtde_vitorias_visitante += 1;
    return qtde_vitorias_visitante;

def get_qtde_empates() -> int:
    qtde_empates: int = 0;
    for partida in PARTIDAS:
        if partida.gols_mandante == partida.gols_visitante:
            qtde_empates += 1;
    return qtde_empates

def analistar_resultados():
    partidas_carregadas();

    print('=-' * 30);
    print(f'Quantidade de vitórias mandante: {get_qtde_vitorias_mandante()} vitórias');
    print(f'Quantidade de vitórias visitante: {get_qtde_vitorias_visitante()} vitórias');
    print(f'Quantidade de empates: {get_qtde_empates()} empates');
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
            selecao_encontrada: bool = False;
            while not selecao_encontrada:
                selecao = input('Digite o código da seleção - Ex: BRA para Brasil : ');
                if consultar_por_selecao(selecao):
                    selecao_encontrada = True;
        elif opcao == 4:
            estadio_encontrado: bool = False;
            while not estadio_encontrado:
                estadio = input('Digite o nome do estádio: ');
                if consultar_por_estadio(estadio):
                    estadio_encontrado = True;
        elif opcao == 5:
            cidade_encontrada = False;
            while not cidade_encontrada:
                cidade = input('Digite o nome da cidade: ');
                if consulta_por_cidade(cidade):
                    cidade_encontrada = True;
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
