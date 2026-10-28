# Conexões — dossiê documental

Quadro interativo de relações em processos envolvendo Lula, empreiteiras, sítio de Atibaia, triplex e José Dirceu.

- [Abrir o site](https://hilthsama-ia.github.io/dossie-conexoes-lava-jato/)
- [Dossiê completo em PDF](https://hilthsama-ia.github.io/dossie-conexoes-lava-jato/dossie-completo.pdf)
- [Quadro de relações em PDF](https://hilthsama-ia.github.io/dossie-conexoes-lava-jato/quadro-relacoes.pdf)

Selecione uma fotografia, escolha um fio e siga a cadeia. As fichas abrem perguntas específicas e explicações até os documentos citados e a consulta oficial do processo. Os portais judiciais abrem em outra aba, pois alguns impedem incorporação em outros sites. O acesso a peças pode exigir autenticação ou estar sujeito a sigilo.

O material distingue vínculos, acusações, declarações, condenações históricas, anulações e absolvições. Conexões não transferem responsabilidade criminal. Provas invalidadas permanecem identificadas, sem presunção de veracidade. Há 20 pessoas/entidades, 29 relações, 12 fichas e 55 referências; isso não constitui inventário integral dos autos.

Pesquisa datada de 28/10/2026. Não houve perícia independente nas mídias originais nem auditoria integral de todos os andamentos de 2025–2026. Os links oficiais permitem conferir atualizações.

## Arquivos

`index.html` contém a interface e as imagens incorporadas e funciona sem servidor de aplicação. Os PDFs são arquivos separados. `src/` preserva os dados, modelos e geradores em Python. Para reconstruir, instale Pillow, reportlab e pypdf, execute `python depth.py` e depois `python build.py` dentro de `src/`. O gerador de PDF usa as fontes Arial do Windows; em outro sistema é necessário ajustar os caminhos das fontes.

Os testes de navegação foram executados em simulação de DOM: seleção, aprofundamento, ida e volta da cadeia e links externos. Isso não substitui uma inspeção renderizada em todos os navegadores. Páginas do PDF foram inspecionadas visualmente.

## Imagens e fontes

Créditos e licenças específicos estão no site, no PDF e em `src/assets/manifest.json`. Fotos, marcas e documentos de terceiros mantêm seus direitos próprios; não há licença geral de redistribuição desses materiais. Algumas imagens jornalísticas estão identificadas com reutilização não confirmada. A marca Nova Engevix é posterior ao período dos fatos; imagens de contexto são rotuladas.
