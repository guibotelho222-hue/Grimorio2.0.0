import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

"""
Grimório Mobile - Aba Oráculo / Conexão Sagrada
Permite importação direta via 'from oraculo_tab import ...'
"""

from tab_trono import criar_aba_trono

def criar_aba_oraculo(page, on_update_callback=None):
    """Alias para a Sala do Trono e Oráculo Real."""
    return criar_aba_trono(page, on_update_callback)

__all__ = ["criar_aba_oraculo", "criar_aba_trono"]
