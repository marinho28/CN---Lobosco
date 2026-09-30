"""
Animação da Eliminação de Gauss + Substituição Regressiva
Exemplo da Seção 3 do notebook Sistemas_Lineares_Gauss_LU.ipynb

    2x +  y -  z =   8
   -3x -  y + 2z = -11
   -2x +  y + 2z =  -3

Arquitetura (3 camadas, de propósito):
  1) gerar_estados()  -> roda o algoritmo e guarda "fotografias" de cada passo
  2) desenhar()       -> transforma UMA fotografia em uma imagem
  3) FuncAnimation    -> percorre as fotografias e grava o GIF

Usamos Fraction (aritmética exata) para o GIF mostrar 1/2, 3/2, ... como na
resolução à mão, em vez de 0.5, 1.5 ...
"""
from fractions import Fraction as F
from copy import deepcopy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

# ----------------------------------------------------------------------
# Dados do problema
# ----------------------------------------------------------------------
A = [[2, 1, -1],
     [-3, -1, 2],
     [-2, 1, 2]]
b = [8, -11, -3]
NOMES = ["x", "y", "z"]

# Paleta
VERDE = "#2e9e5b"    # pivô
VERMELHO = "#d64545" # elemento a eliminar
AMARELO = "#f2b705"  # valor recém-calculado
AZUL = "#2f6fdd"     # valores já conhecidos (subst. regressiva)
CINZA = "#8a8f98"
FUNDO_LINHA = {VERDE: "#e3f4ea", VERMELHO: "#fbe6e6", AZUL: "#e6eefc", AMARELO: "#fff4cc"}


# ----------------------------------------------------------------------
# Formatação (mathtext do matplotlib)
# ----------------------------------------------------------------------
def tex(x, paren=False):
    """Fraction -> string mathtext (sem os $)."""
    x = F(x)
    if x.denominator == 1:
        s = str(x.numerator)
    else:
        s = ("-" if x < 0 else "") + r"\frac{%d}{%d}" % (abs(x.numerator), x.denominator)
    if paren and x < 0:
        s = "(" + s + ")"
    return s


def linha_tex(v):
    """[a, b, c, d] -> [a, b, c | d]"""
    return "$[" + ", ".join(tex(e) for e in v[:-1]) + r"\,|\," + tex(v[-1]) + "]$"


def eq_tex(row, nomes):
    """Linha da matriz aumentada -> equação legível."""
    partes = []
    for c, nome in zip(row[:-1], nomes):
        if c == 0:
            continue
        sinal = "-" if c < 0 else "+"
        mod = abs(c)
        coef = "" if mod == 1 else tex(mod)
        partes.append((sinal, coef + nome))
    s = ""
    for k, (sinal, termo) in enumerate(partes):
        if k == 0:
            s += ("-" if sinal == "-" else "") + termo
        else:
            s += f" {sinal} {termo}"
    return "$" + s + " = " + tex(row[-1]) + "$"


# ----------------------------------------------------------------------
# 1) Gera os estados (uma "fotografia" por passo didático)
# ----------------------------------------------------------------------
def gerar_estados(A, b):
    n = len(b)
    M = [[F(v) for v in linha] + [F(bi)] for linha, bi in zip(A, b)]
    L = [[None] * n for _ in range(n)]      # multiplicadores guardados
    estados = []

    def foto(**kw):
        base = dict(M=deepcopy(M), L=deepcopy(L), hi={}, rowhi={}, temp=None,
                    temp_label="", sol=[None] * n, linhas=[], hold=1, fase="")
        base.update(kw)
        estados.append(base)

    # --- abertura ---------------------------------------------------
    foto(titulo="Sistema original → matriz aumentada [A | b]",
         fase="Início",
         linhas=[eq_tex(M[i], NOMES) for i in range(n)] +
                ["", "Objetivo: zerar tudo abaixo da diagonal", "(forma triangular superior)"],
         hold=2)

    # --- eliminação -------------------------------------------------
    passo = 0
    for k in range(n - 1):
        for i in range(k + 1, n):
            passo += 1
            I, K = i + 1, k + 1
            pivo, alvo = M[k][k], M[i][k]
            m = alvo / pivo
            L[i][k] = m

            # (a) achar pivô e multiplicador
            foto(titulo=f"Passo {passo}: zerar a{I}{K} usando o pivô a{K}{K}",
                 fase="Eliminação",
                 hi={(k, k): VERDE, (i, k): VERMELHO},
                 rowhi={k: VERDE, i: VERMELHO},
                 linhas=[r"Pivô:  $a_{%d%d}=%s$" % (K, K, tex(pivo)),
                         r"A eliminar:  $a_{%d%d}=%s$" % (I, K, tex(alvo)),
                         "",
                         r"$m_{%d%d}=\frac{a_{%d%d}}{a_{%d%d}}=\frac{%s}{%s}=%s$"
                         % (I, K, I, K, K, K, tex(alvo), tex(pivo), tex(m)),
                         "",
                         r"Regra:  $R_{%d}\leftarrow R_{%d}-m_{%d%d}\,R_{%d}$" % (I, I, I, K, K)])

            # (b) linha do pivô escalada
            temp = [m * M[k][c] for c in range(n + 1)]
            foto(titulo=f"Passo {passo}: calcular m{I}{K} · R{K}",
                 fase="Eliminação",
                 hi={(k, k): VERDE, (i, k): VERMELHO},
                 rowhi={k: VERDE, i: VERMELHO},
                 temp=temp, temp_label=r"$m_{%d%d}\cdot R_{%d}$" % (I, K, K),
                 linhas=[r"$m_{%d%d}\cdot R_{%d}=%s\cdot$" % (I, K, K, tex(m, True)) + linha_tex(M[k]),
                         "",
                         r"$=$" + linha_tex(temp),
                         "",
                         "Multiplicamos a linha INTEIRA,",
                         "inclusive o termo independente."])

            # (c) subtrair
            antes = M[i][:]
            M[i] = [M[i][c] - temp[c] for c in range(n + 1)]
            mudou = {(i, c): AMARELO for c in range(n + 1)}
            mudou[(i, k)] = VERDE
            foto(titulo=f"Passo {passo}: R{I} ← R{I} − m{I}{K}·R{K}",
                 fase="Eliminação",
                 hi=mudou, rowhi={i: AMARELO},
                 linhas=[r"$R_{%d}=$" % I + linha_tex(antes),
                         r"$\;\;-$" + linha_tex(temp),
                         r"$\;\;=$" + linha_tex(M[i]),
                         "",
                         r"Zero criado em $a_{%d%d}$:  $%s-%s\cdot%s=0$"
                         % (I, K, tex(antes[k]), tex(m, True), tex(pivo, True))],
                 hold=2)

    # --- matriz triangular ------------------------------------------
    foto(titulo="Forma triangular superior (U) alcançada",
         fase="Fim da eliminação",
         rowhi={r: AMARELO for r in range(n)},
         linhas=["Sistema equivalente (mesma solução):", ""] +
                [eq_tex(M[i], NOMES) for i in range(n)] +
                ["", "Agora: resolver de baixo para cima."],
         hold=3)

    # --- substituição regressiva ------------------------------------
    sol = [None] * n
    for i in range(n - 1, -1, -1):
        I = i + 1
        soma = sum(M[i][j] * sol[j] for j in range(i + 1, n))
        xi = (M[i][n] - soma) / M[i][i]

        num = tex(M[i][n])
        for j in range(i + 1, n):
            num += r" - %s\cdot%s" % (tex(M[i][j], True), tex(sol[j], True))
        formula = r"$%s=\frac{%s}{%s}=%s$" % (NOMES[i], num, tex(M[i][i]), tex(xi))

        hi = {(i, i): VERDE}
        hi.update({(i, j): AZUL for j in range(i + 1, n)})
        sol[i] = xi
        foto(titulo=f"Substituição regressiva: achar {NOMES[i]}",
             fase="Substituição regressiva",
             hi=hi, rowhi={i: VERDE},
             sol=sol[:],
             linhas=[f"Equação {I}:  " + eq_tex(M[i], NOMES),
                     "",
                     "Isolando " + f"${NOMES[i]}$" + ":",
                     formula],
             hold=2)

    # --- conferência ------------------------------------------------
    ok = all(sum(F(A[r][c]) * sol[c] for c in range(n)) == b[r] for r in range(n))
    foto(titulo="Solução encontrada",
         fase="Resultado",
         sol=sol[:],
         linhas=[r"$x=%s,\quad y=%s,\quad z=%s$" % tuple(tex(v) for v in sol),
                 "",
                 "Conferência no sistema original:"] +
                [r"$%s$" % (" + ".join(r"(%s)(%s)" % (tex(A[r][c], False), tex(sol[c], False))
                                      for c in range(n)) + " = " + tex(b[r])) for r in range(n)] +
                ["", ("A·x = b  ✓" if ok else "A·x ≠ b  ✗")],
         hold=4)
    return estados


# ----------------------------------------------------------------------
# 2) Desenha UMA fotografia
# ----------------------------------------------------------------------
COL_X = [1.9, 3.2, 4.5, 6.1]   # colunas x1 x2 x3 | b
ROW_Y = [5.0, 4.0, 3.0]        # linhas R1 R2 R3
BARRA_X = 5.3
TEMP_Y = 1.75


def desenhar(ax, est, idx, total):
    ax.clear()
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    # título + chip de fase
    ax.text(0.5, 6.75, est["titulo"], fontsize=19, fontweight="bold", va="center")
    ax.text(12.8, 6.75, est["fase"], fontsize=11, color="white", ha="right", va="center",
            bbox=dict(boxstyle="round,pad=0.4", fc="#3b4252", ec="none"))

    # cabeçalhos das colunas
    for x, nome in zip(COL_X, NOMES + ["b"]):
        ax.text(x, 5.75, nome, fontsize=13, color=CINZA, ha="center", va="center")

    # fundo das linhas destacadas
    for r, cor in est["rowhi"].items():
        ax.add_patch(Rectangle((1.05, ROW_Y[r] - 0.42), 6.05, 0.84,
                               fc=FUNDO_LINHA[cor], ec="none", zorder=0))

    # colchetes e barra vertical
    for sx, dx in ((1.15, 0.12), (7.0, -0.12)):
        ax.plot([sx + dx, sx, sx, sx + dx], [5.45, 5.45, 2.55, 2.55], color="#333", lw=2)
    ax.plot([BARRA_X, BARRA_X], [2.6, 5.4], color="#333", lw=1.5, ls=(0, (4, 3)))

    # rótulos das linhas
    for r in range(3):
        ax.text(0.65, ROW_Y[r], r"$R_%d$" % (r + 1), fontsize=15, color=CINZA,
                ha="center", va="center")

    # células
    for r in range(3):
        for c in range(4):
            cor = est["hi"].get((r, c))
            if cor:
                ax.add_patch(Rectangle((COL_X[c] - 0.55, ROW_Y[r] - 0.33), 1.1, 0.66,
                                       fc="white", ec=cor, lw=3, zorder=1))
            ax.text(COL_X[c], ROW_Y[r], "$" + tex(est["M"][r][c]) + "$",
                    fontsize=21, ha="center", va="center", zorder=2)

    # linha temporária (m · R_k)
    if est["temp"] is not None:
        ax.plot([1.2, 7.0], [2.45, 2.45], color=CINZA, lw=1, ls=":")
        ax.text(0.65, TEMP_Y, est["temp_label"], fontsize=12, color=CINZA,
                ha="center", va="center")
        for c in range(4):
            ax.text(COL_X[c], TEMP_Y, "$" + tex(est["temp"][c]) + "$", fontsize=21,
                    color=AZUL, ha="center", va="center")

    # solução parcial (substituição regressiva)
    if any(v is not None for v in est["sol"]):
        ax.text(0.65, 1.75, "sol.", fontsize=12, color=CINZA, ha="center", va="center")
        for k, v in enumerate(est["sol"]):
            if v is not None:
                ax.text(1.9 + 1.7 * k, 1.75, r"$%s=%s$" % (NOMES[k], tex(v)),
                        fontsize=20, color=VERDE, ha="center", va="center")

    # painel de explicação (direita)
    ax.add_patch(Rectangle((7.7, 2.85), 5.1, 3.4, fc="#f7f8fa", ec="#d8dce3", lw=1))
    y = 5.95
    for txt in est["linhas"]:
        if txt:
            ax.text(7.95, y, txt, fontsize=14, va="center")
        y -= 0.44

    # painel L (multiplicadores) — conexão com a decomposição LU
    ax.text(7.7, 2.45, "Multiplicadores guardados  →  matriz L", fontsize=11.5,
            color=CINZA, va="center")
    lx = [8.7, 10.0, 11.3]
    ly = [1.85, 1.3, 0.75]
    ax.text(7.95, 1.3, r"$L=$", fontsize=16, va="center")
    for r in range(3):
        for c in range(3):
            if r == c:
                txt, col = "1", "#333"
            elif r < c:
                txt, col = "0", "#bbb"
            else:
                v = est["L"][r][c]
                txt, col = (("$%s$" % tex(v)), AMARELO if est["L"][r][c] is not None else "#ccc") \
                    if v is not None else ("?", "#ccc")
                if v is not None:
                    col = "#b8860b"
            ax.text(lx[c], ly[r], txt, fontsize=15, color=col, ha="center", va="center")
    ax.plot([8.25, 8.4, 8.4, 8.25], [2.15, 2.15, 0.45, 0.45], color="#333", lw=1.5)
    ax.plot([11.75, 11.6, 11.6, 11.75], [2.15, 2.15, 0.45, 0.45], color="#333", lw=1.5)

    # barra de progresso
    ax.add_patch(Rectangle((0.5, 0.12), 12.3, 0.1, fc="#e5e7eb", ec="none"))
    ax.add_patch(Rectangle((0.5, 0.12), 12.3 * (idx + 1) / total, 0.1, fc=VERDE, ec="none"))


# ----------------------------------------------------------------------
# 3) Monta e salva o GIF
# ----------------------------------------------------------------------
def main(saida="gauss.gif", fps=0.6):
    estados = gerar_estados(A, b)
    # 'hold' repete o quadro para dar mais tempo de leitura nos passos densos
    quadros = [i for i, e in enumerate(estados) for _ in range(e["hold"])]

    fig, ax = plt.subplots(figsize=(13, 7.2), dpi=90)
    fig.subplots_adjust(0, 0, 1, 1)

    def atualizar(q):
        desenhar(ax, estados[q], q, len(estados))

    anim = FuncAnimation(fig, atualizar, frames=quadros, repeat=True)
    anim.save(saida, writer=PillowWriter(fps=fps))
    print(f"GIF salvo em {saida} ({len(quadros)} quadros)")
    return estados


if __name__ == "__main__":
    main()
