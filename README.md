# Conexões — dossiê documental

Quadro interativo de relações em processos envolvendo Lula, empreiteiras, sítio de Atibaia, triplex e José Dirceu.

- [Abrir o site](https://lavajatointerativa.com.br/)
- [Dossiê completo em PDF](https://lavajatointerativa.com.br/dossie-completo.pdf)
- [Quadro de relações em PDF](https://lavajatointerativa.com.br/quadro-relacoes.pdf)

Selecione uma fotografia, escolha um fio e siga a cadeia. As fichas abrem perguntas específicas e explicações até os documentos citados e a consulta oficial do processo. Os portais judiciais abrem em outra aba, pois alguns impedem incorporação em outros sites. O acesso a peças pode exigir autenticação ou estar sujeito a sigilo.

O material distingue vínculos, acusações, declarações, condenações históricas, anulações e absolvições. Conexões não transferem responsabilidade criminal. Provas invalidadas permanecem identificadas, sem presunção de veracidade. Há 20 pessoas/entidades, 29 relações, 12 fichas e 55 referências; isso não constitui inventário integral dos autos.

Pesquisa datada de 28/10/2026. Não houve perícia independente nas mídias originais nem auditoria integral de todos os andamentos de 2025–2026. Os links oficiais permitem conferir atualizações.

## Arquivos

`index.html` contém a interface e as imagens incorporadas e funciona sem servidor de aplicação. Os PDFs são arquivos separados. `src/` preserva os dados, modelos e geradores em Python. Para reconstruir, instale Pillow, reportlab e pypdf, execute `python depth.py` e depois `python build.py` dentro de `src/`. O gerador de PDF usa as fontes Arial do Windows; em outro sistema é necessário ajustar os caminhos das fontes.

Os testes de navegação foram executados em simulação de DOM: seleção, aprofundamento, ida e volta da cadeia e links externos. Isso não substitui uma inspeção renderizada em todos os navegadores. Páginas do PDF foram inspecionadas visualmente.

## Imagens e fontes

Créditos e licenças específicos estão no site, no PDF e em `src/assets/manifest.json`. Fotos, marcas e documentos de terceiros mantêm seus direitos próprios; não há licença geral de redistribuição desses materiais. Algumas imagens jornalísticas estão identificadas com reutilização não confirmada. A marca Nova Engevix é posterior ao período dos fatos; imagens de contexto são rotuladas.

## Publicação na Hostinger e SEO

O domínio principal é `lavajatointerativa.com.br`. O pacote de hospedagem contém a página interativa, cinco guias HTML indexáveis, dois PDFs, imagem social de 1200 × 630, favicon, sitemap, robots e regras de redirecionamento HTTPS. Os arquivos em `src/` são mantidos no GitHub e não precisam ser enviados à hospedagem.

`python src/seo.py` atualiza os metadados e os guias. O Google Search Console depende da verificação do domínio; envio de sitemap e pedido de indexação não garantem inclusão ou posição nos resultados.
