import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import os
import flet as ft

# Compatibilidade estrita de ft.icons para Serious Python e versões Flet
if hasattr(ft, "icons") and hasattr(ft.icons, "Icons"):
    for _attr in dir(ft.icons.Icons):
        if not _attr.startswith("_") and not hasattr(ft.icons, _attr):
            setattr(ft.icons, _attr, getattr(ft.icons.Icons, _attr))

# 2. Resolução segura de caminhos estáticos (Assets e Mídias)
def resolve_path(relative_path: str) -> str:
    """Resolve caminhos em modo Dev, Mobile (Android/iOS) e PyInstaller usando pathlib."""
    base_dir = Path(__file__).parent.resolve()
    caminho = base_dir / relative_path
    if caminho.exists():
        return str(caminho)
    caminho_assets = base_dir / "assets" / relative_path
    if caminho_assets.exists():
        return str(caminho_assets)
    if hasattr(sys, "_MEIPASS"):
        return str(Path(sys._MEIPASS) / relative_path)
    return str(caminho)

# 3. Importações Diretas da Raiz (Flat Structure - 100% Blindada)
from theme import (
    BG_DARK, BG_SURFACE, GOLD_PRIMARY, GOLD_LIGHT,
    PURPLE_PRIMARY, PURPLE_LIGHT, TEXT_PRIMARY,
    get_dark_theme, get_theme_colors, aplicar_tema
)
from storage import storage
from common_ui import criar_cabecalho_reino, abrir_modal_configuracoes
from tab_trono import criar_aba_trono
from tab_quests import criar_aba_quests
from tab_cofre import criar_aba_cofre
from tab_forja import criar_aba_forja
from tab_foco import criar_aba_foco


def main(page: ft.Page):
    """
    Ponto de Entrada Oficial Síncrono do Grimório Mobile v2.0.
    Inicialização Direta: SEM Splash Screen, SEM loops pesados, boot instantâneo nas 5 abas.
    """
    # Carrega preferências salvas
    cfg = storage.obter_configuracoes()
    tema_atual = cfg.get("tema_atual", "Dark Fantasy Dourado")
    cores = get_theme_colors(tema_atual)

    # Configuração de Título e Cores Base da Página
    page.title = "Grimório"
    page.theme = get_dark_theme(tema_atual)
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = cores["bg_dark"]
    page.padding = 0
    page.spacing = 0

    # Configurações de janela (apenas para testes em Desktop)
    if hasattr(page, "window"):
        try:
            page.window.width = 420
            page.window.height = 840
            page.window.min_width = 360
            page.window.min_height = 640
            caminho_ico = resolve_path("assets/rei_joaquim_trono.png")
            if os.path.exists(caminho_ico):
                page.window.icon = caminho_ico
        except Exception:
            pass

    # Inicialização Segura de Áudio em page.overlay (Protegida contra crash)
    try:
        som_foco_path = resolve_path("assets/som_foco.mp3")
        som_alerta_path = resolve_path("assets/som_alerta.mp3")

        audio_foco = ft.Audio(src=som_foco_path, autoplay=False)
        audio_alerta = ft.Audio(src=som_alerta_path, autoplay=False)
        page.overlay.append(audio_foco)
        page.overlay.append(audio_alerta)
        page.audio_foco = audio_foco
        page.audio_alerta = audio_alerta
    except Exception as e:
        print(f"[Áudio Mobile] Overlay: {e}")
        page.audio_foco = None
        page.audio_alerta = None

    # Estado de Navegação Ativa
    estado_app = {
        "aba_atual": 0
    }

    # Contêineres de Interface
    area_cabecalho = ft.Container()
    area_conteudo = ft.Container(expand=True)

    def atualizar_cabecalho():
        """Atualiza sincronamente os valores de Ouro, EXP, Lua e Runa do cabeçalho real."""
        area_cabecalho.content = criar_cabecalho_reino(
            page=page,
            on_refresh=atualizar_cabecalho,
            on_settings_click=acao_abrir_configuracoes
        )
        try:
            area_cabecalho.update()
        except Exception:
            pass

    def trocar_aba(indice: int):
        """Alterna entre as 5 abas com rolagem independente e zero travamentos."""
        estado_app["aba_atual"] = indice
        atualizar_cabecalho()

        if indice == 0:
            area_conteudo.content = criar_aba_trono(page, on_update_callback=atualizar_cabecalho)
        elif indice == 1:
            area_conteudo.content = criar_aba_quests(page, on_update_callback=atualizar_cabecalho)
        elif indice == 2:
            area_conteudo.content = criar_aba_cofre(page, on_update_callback=atualizar_cabecalho)
        elif indice == 3:
            area_conteudo.content = criar_aba_forja(page, on_update_callback=atualizar_cabecalho)
        elif indice == 4:
            area_conteudo.content = criar_aba_foco(page, on_update_callback=atualizar_cabecalho)

        try:
            area_conteudo.update()
        except Exception:
            pass

    def recarregar_layout():
        """Recarrega cabeçalho, tema, nomes das abas e aba ativa quando configurado."""
        cfg_atual = storage.obter_configuracoes()
        tema_novo = cfg_atual.get("tema_atual", "Dark Fantasy Dourado")
        novas_cores = get_theme_colors(tema_novo)
        nomes_abas = cfg_atual.get("nomes_abas", {})

        aplicar_tema(tema_novo)
        page.theme = get_dark_theme(tema_novo)
        page.bgcolor = novas_cores["bg_dark"]

        # Atualiza labels e cores da barra de navegação
        nav_bar.destinations[0].label = nomes_abas.get("trono", "Trono")
        nav_bar.destinations[1].label = nomes_abas.get("quests", "Quests")
        nav_bar.destinations[2].label = nomes_abas.get("cofre", "Cofre")
        nav_bar.destinations[3].label = nomes_abas.get("forja", "Forja")
        nav_bar.destinations[4].label = nomes_abas.get("foco", "Foco")
        nav_bar.bgcolor = novas_cores["bg_surface"]
        nav_bar.indicator_color = novas_cores["container"]

        atualizar_cabecalho()
        trocar_aba(estado_app["aba_atual"])
        page.update()

    def acao_abrir_configuracoes(e):
        abrir_modal_configuracoes(page, on_saved=recarregar_layout)

    # Barra de Navegação Inferior das 5 Abas Otimizada para Celular
    nomes_abas_iniciais = cfg.get("nomes_abas", {})
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.FORT_OUTLINED,
                selected_icon=ft.icons.FORT,
                label=nomes_abas_iniciais.get("trono", "Trono")
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.AUTO_AWESOME_OUTLINED,
                selected_icon=ft.icons.AUTO_AWESOME,
                label=nomes_abas_iniciais.get("quests", "Quests")
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.SAVINGS_OUTLINED,
                selected_icon=ft.icons.SAVINGS,
                label=nomes_abas_iniciais.get("cofre", "Cofre")
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.BUILD_OUTLINED,
                selected_icon=ft.icons.BUILD,
                label=nomes_abas_iniciais.get("forja", "Forja")
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.SCIENCE_OUTLINED,
                selected_icon=ft.icons.SCIENCE,
                label=nomes_abas_iniciais.get("foco", "Foco")
            ),
        ],
        selected_index=0,
        bgcolor=cores["bg_surface"],
        indicator_color="#4C1D9580",
        height=65,
        on_change=lambda e: trocar_aba(e.control.selected_index)
    )

    # Renderização Direta e Imediata do Reino (SEM Splash Screen)
    atualizar_cabecalho()
    area_conteudo.content = criar_aba_trono(page, on_update_callback=atualizar_cabecalho)

    layout_principal = ft.Column(
        controls=[
            area_cabecalho,
            area_conteudo
        ],
        expand=True,
        spacing=0
    )

    page.navigation_bar = nav_bar
    page.add(layout_principal)
    page.update()


if __name__ == "__main__":
    assets_dir_path = resolve_path("assets")
    if hasattr(ft, "run"):
        ft.run(main, assets_dir=assets_dir_path)
    elif hasattr(ft, "app"):
        ft.app(target=main, assets_dir=assets_dir_path)
