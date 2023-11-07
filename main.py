import requests;
from Partida import Partida;
from Gol import Gol;
from Jogador import Jogador;
from Time import Time;

resposta = requests.get(
    'https://raw.githubusercontent.com/leandroflores/api-world-cup/main/results_2018').json();

PARTIDAS: list[Partida] = [];
GOLS: list[Gol] = [];

def carregar_grupo(grupo: str) -> list[int]:
    partidas_carregadas();
    rodadas: list[dict] = resposta['rounds'];
    identificador_partidas: list[int] = [];

    for rodada in rodadas:
        partidas: list[dict] = rodada['matches'];
        for partida in partidas:
            if 'group' in partida:
                grupo_partida: str = partida['group'];
                if grupo in grupo_partida:
                    identificador_partidas.append(partida['num']);
    return identificador_partidas;


def carregar_rodada(rodada: int) -> list[int]:
    partidas_carregadas();
    identificador_partidas: list[int] = [];
    partidas: list[dict] = resposta['rounds'][rodada]['matches'];
    for partida in partidas:
        id: int = partida['num'];
        identificador_partidas.append(id);
    return identificador_partidas;


def carregar_partidas() -> None:
    rodadas: list[dict] = resposta['rounds'];
    for rodada in rodadas:
        partidas: list[dict] = rodada['matches'];
        for partida_rodada in partidas:
            time1_nome: str = partida_rodada['team1']['name'];
            time1_codigo: int = partida_rodada['team1']['code'];

            time2_nome: str = partida_rodada['team2']['name'];
            time2_codigo: int = partida_rodada['team2']['code'];

            id: int = partida_rodada['num'];
            data_partida: str = partida_rodada['date'];
            mandante: Time = Time(time1_nome, time1_codigo);
            visitante: Time = Time(time2_nome, time2_codigo);
            gols_mandante: int = partida_rodada['score1'];
            gols_visitante: int = partida_rodada['score2'];

            cidade: str = partida_rodada['city'];
            estadio: str = partida_rodada['stadium']['name'];
            horario: str = partida_rodada['time'];
            partida: Partida = Partida(id, mandante, visitante, gols_mandante, gols_visitante,
                                       data_partida, cidade, estadio, horario);
            PARTIDAS.append(partida);


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
                    minuto_gol: str = gol['minute'];
                    gol: Gol = Gol(nome_jogador, minuto_gol);
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
    partidas_carregadas();
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
    partidas_rodada: list[int] = carregar_rodada(rodada);
    qtde_partidas: int = len(partidas_rodada);
    print('=-' * 50);
    print(f'Quantidade de partidas na rodada: {qtde_partidas} partidas');
    print('=-' * 50);
    partidas: list[Partida] = list(
        filter(lambda partida: partida.id in partidas_rodada,PARTIDAS)
    );
    com_partidas(partidas);

def consultar_por_grupo(grupo: str):
    partidas_carregadas();
    lista_id_partidas: list[int] = carregar_grupo(grupo);
    partidas: list[Partida] = list(
      filter(lambda partida: partida.id in lista_id_partidas,PARTIDAS)
    );
    com_partidas(partidas);
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
