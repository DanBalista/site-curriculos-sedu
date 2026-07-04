# Site Currículos SEDU — Contexto do Projeto

## O que é este projeto

Site da **Gerência de Currículo da Educação Básica (GECEB)**, da Secretaria de Estado da Educação do Espírito Santo (SEDU). Migração do site WordPress/Elementor em `curriculo.sedu.es.gov.br/curriculo/` para Django moderno.

O dono do projeto (**Dan**) não é programador — ele trabalha na SEDU e precisa de instruções claras, em português, para qualquer operação no terminal. Sempre explique comandos passo a passo.

## Stack

- **Django 5.2** com Python 3.13
- **SQLite** em desenvolvimento, PostgreSQL planejado para produção
- **Venv** em `venv/`
- CSS puro (sem frameworks CSS), Font Awesome 6 para ícones, Google Fonts (Inter)
- Deploy futuro com Docker

## Estrutura do projeto

```
curriculo_sedu/          # Projeto Django (settings, urls, wsgi)
conteudo/                # App principal
  models.py              # Categoria, Conteudo, Banner, ConfiguracaoSite
  views.py               # home, categoria_detalhe, conteudo_detalhe, busca
  admin.py               # Admin customizado com badges coloridos
  urls.py                # app_name='conteudo'
  context_processors.py  # site_config (config + menu_categorias global)
  management/commands/
    popular_categorias.py   # Seed de categorias e subcategorias
    popular_descricoes.py   # Textos introdutórios das categorias (HTML)
    migrar_conteudo.py      # 102 itens de conteúdo migrados do WordPress
templates/
  base.html              # Layout base (header, nav dinâmica, footer)
  home.html              # Home: banners, categorias, destaques, recentes
  categoria.html         # Lista de conteúdos com filtros por tipo
  conteudo_detalhe.html  # Página de detalhe de conteúdo
  busca.html             # Resultados de busca
static/
  css/style.css          # Design system completo (~700 linhas)
  js/main.js             # Slider do hero, menu mobile
  img/                   # brasao.png, logo-geceb.png, hero-bg.png
db.sqlite3               # Banco já populado com 102 conteúdos
```

## Modelos principais

### Categoria
- `nome`, `slug`, `descricao` (HTML para textos introdutórios), `icone` (classe Font Awesome)
- `categoria_pai` (FK self) — hierarquia de 2 níveis
- `ordem`, `ativa`, `imagem`

### Conteudo
- Tipos: `documento`, `video`, `post`, `link`, `pagina`
- Status: `rascunho`, `publicado`, `arquivado`
- Campos: `titulo`, `slug`, `resumo`, `corpo` (HTML), `arquivo`, `url_video`, `url_externa`, `imagem_destaque`
- `destaque` (bool) — aparece na home
- Propriedades: `tipo_icone`, `extensao_arquivo`, `get_video_embed_url()`

### Banner
Banners rotativos na home. Campos: `titulo`, `subtitulo`, `imagem`, `link`, `ordem`, `ativo`.

### ConfiguracaoSite
Singleton (pk=1). `nome_site`, `descricao`, `email_contato`, `telefone`, `endereco`, `logo`, `favicon`.

## URLs

```
/                          → home
/admin/                    → Django Admin
/busca/?q=termo            → busca textual
/categoria/<slug>/         → lista de conteúdos com filtros
/categoria/<slug>/?tipo=X  → filtro por tipo (documento, video, post, link)
/conteudo/<slug>/          → detalhe de conteúdo
```

## Categorias atuais (6 principais + subcategorias)

1. **Documentos Curriculares** (fas fa-book) — subcategorias: Currículo Atual, Orientações Curriculares, Cadernos Metodológicos, Mapas de Progressão, Ementas Curriculares, Rotinas de Recomposição, Espaços Potencialmente Educativos
2. **Programas** (fas fa-project-diagram) — subcategorias: Educar para a Paz, Mais Leitores, Educação Ambiental, Sucesso Escolar
3. **Livro Didático** (fas fa-book-reader)
4. **Modalidades e Diversidade** (fas fa-users) — subcategorias: EJA — Documentos, Educação do Campo, Educação Quilombola, Educação Indígena, Relações Étnico-Raciais, Socioeducação
5. **Olimpíadas e Competições** (fas fa-trophy)
6. **Institucional** (fas fa-landmark)

## Design system (CSS)

Variáveis principais em `style.css`:
- `--primary: #2d5a8e` (azul do header e acentos)
- `--primary-dark: #1e3a5f`
- `--text: #1a1a2e`, `--text-light: #4a5568`
- `--bg: #ffffff`, `--bg-alt: #f7f8fa`
- Font: Inter, system-ui

Header: fundo `--primary`, logos 50px, nav com dropdown implícito, busca inline, largura 100% com padding 32px.

Componentes: `.content-card`, `.category-card`, `.content-list .list-item`, `.filter-chip`, `.subcategory-chip`, `.page-intro-body` (texto introdutório com borda azul à esquerda).

## Decisões de design já tomadas

1. **Header sem filtros CSS nos logos** — brightness/blend-mode removidos, logos exibidos com cores originais
2. **Textos introdutórios** aparecem entre os filtros de tipo e o grid de conteúdo (não no header)
3. **Cards da home** usam `|striptags|truncatewords:10` para descrições limpas
4. **Conteúdo migrado** via web scraping do WordPress — 102 itens com links para PDFs e Google Drive
5. **16 categorias** têm textos introdutórios em HTML (populados via `popular_descricoes.py`)

## Como rodar

```bash
cd "Site Curriculos SEDU"
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/ (criar superuser com `python manage.py createsuperuser`)

## Management commands disponíveis

```bash
python manage.py popular_categorias    # Cria categorias e subcategorias
python manage.py popular_descricoes    # Textos introdutórios das categorias
python manage.py migrar_conteudo       # 102 itens de conteúdo do site original
```

Todos são idempotentes (usam `get_or_create` ou verificam existência).

## O que já foi feito

- [x] Estrutura completa do Django (models, views, admin, templates, CSS)
- [x] Admin personalizado com badges coloridos, filtros e ações em lote
- [x] Template base responsivo com header, nav dinâmica e footer
- [x] Página home com categorias, destaques e conteúdos recentes
- [x] Página de categoria com subcategorias, filtros por tipo e textos introdutórios
- [x] Página de detalhe de conteúdo com relacionados
- [x] Busca textual
- [x] Migração de 102 conteúdos do site original WordPress
- [x] 16 textos introdutórios das categorias extraídos do site original
- [x] Header com logos (brasão ES + GECEB) sem distorção de cores

## O que falta / próximos passos possíveis

- [ ] Adicionar imagens de destaque aos conteúdos
- [ ] Configurar banners/slider na home (model Banner existe mas sem dados)
- [ ] Refinamentos visuais conforme feedback do Dan
- [ ] Deploy com Docker + PostgreSQL para produção
- [ ] Testar em Windows (ambiente de trabalho do Dan)
- [ ] Configurar domínio e certificado SSL
- [ ] Melhorar responsividade mobile
- [ ] Adicionar paginação nas listagens de conteúdo

## Notas importantes

- O banco `db.sqlite3` já contém todos os dados migrados. Não precisa rodar os commands novamente a menos que queira resetar.
- Os conteúdos tipo `link` e `documento` apontam para URLs externas (Google Drive, SEDU, etc.) — os arquivos PDF não estão armazenados localmente.
- O site original em WordPress está em: `curriculo.sedu.es.gov.br/curriculo/`
- O usuário não tem conhecimento de programação — sempre forneça comandos prontos para copiar e colar.
