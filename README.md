# Grimório Mobile v2.0 (Clean Architecture)

Aplicativo Dark Fantasy & Gestão do Reino (Edição Android).
Arquitetura Síncrona, Flat & Clean, Otimizada para Serious Python e Flet Build APK.

## Destaques da Versão Clean
- **Estrutura 100% Plana:** Todos os módulos na raiz para evitar `ModuleNotFoundError` no Android.
- **Inicialização Direta:** Abertura instantânea nas 5 abas, sem Splash Screen ou travamentos.
- **Gerenciamento de Estado Síncrono:** Dados salvos em JSON em armazenamento gravável do app.
- **Build Automatizado:** Pipeline GitHub Actions configurado e pronto para gerar o APK.

## Estrutura de Pastas
```text
GrimorioMobile_Clean/
├── .github/workflows/main.yml
├── assets/
│   ├── gatinho_cavaleiro.png
│   ├── grimorio_mobile_dados.json
│   ├── logo.ico
│   ├── logo.png
│   ├── mascote.png
│   ├── princesa_guerreira.png
│   ├── rei_joaquim_trono.png
│   ├── som_alerta.mp3
│   └── som_foco.mp3
├── .gitignore
├── common_ui.py
├── main.py
├── mascote_vector.py
├── oracle.py
├── oraculo_tab.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── storage.py
├── tab_cofre.py
├── tab_foco.py
├── tab_forja.py
├── tab_quests.py
├── tab_trono.py
└── theme.py
```
