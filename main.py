import sys
import traceback
from pathlib import Path
import flet as ft

# Injeta a raiz no caminho de busca do Python
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

def main(page: ft.Page):
    page.title = "Grimório v2.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    try:
        # Tenta carregar os módulos da raiz
        import tab_cofre
        import oraculo_tab

        page.clean()
        
        # Teste de renderização dos componentes principais
        page.add(
            ft.Text("Grimório do Rei Joaquim", size=24, weight=ft.FontWeight.BOLD, color="gold"),
            ft.Text("Aplicação iniciada com sucesso!", color="green", size=16),
            ft.Divider()
        )

        # Se tab_cofre tiver a função de montagem, renderiza-a
        if hasattr(tab_cofre, "build_tab_cofre"):
            page.add(tab_cofre.build_tab_cofre(page))
        elif hasattr(tab_cofre, "main"):
            page.add(ft.Text("Aba Cofre Detetada"))

        page.update()

    except Exception as e:
        # Se houver QUALQUER erro ao carregar as abas ou assets,
        # ele SERÁ EXIBIDO EM TEXTO NA TELA em vez da tela preta!
        page.clean()
        page.add(
            ft.Text("⚠️ ERRO DE EXECUÇÃO NO ANDROID", color="red", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Detalhes do Erro: {str(e)}", color="yellow", size=14),
            ft.Divider(),
            ft.Text("Traceback Completo:", color="white", size=12, weight=ft.FontWeight.BOLD),
            ft.Text(traceback.format_exc(), color="white70", size=10)
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
