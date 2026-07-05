# Site Currículos SEDU — Contexto do Projeto

## O que é este projeto

Site da **Gerência de Currículo da Educação Básica (GECEB)**, da Secretaria de Estado da Educação do Espírito Santo (SEDU). Migração do site WordPress/Elementor em `curriculo.sedu.es.gov.br/curriculo/` para Django moderno.

O dono do projeto (**Dan**) não é programador — ele trabalha na SEDU e precisa de instruções claras, em português, para qualquer operação no terminal. Sempre explique comandos passo a passo.

## Stack

- **Django 5.2** com Python 3.13 (local) / Python 3.11 (PythonAnywhere)
- **SQLite** em desenvolvimento e também em produção (por enquanto)
- **Venv** em `venv/`
- CSS puro (sem frameworks CSS), Font Awesome 6 para ícones, Google Fonts (Inter)
- **Deploy atual: PythonAnywhere** (https://rabalista.pythonanywhere.com) — ver seção "Deploy" abaixo
- **Versionamento: GitHub** — https://github.com/DanBalista/site-curriculos-sedu.git

## Estrutura do projeto

```
curriculo_sedu/          # Projeto Django (settings, urls, wsgi)
conteudo/                # App principal
  models.py              # Categoria, Conteudo, Banner, Comentario, ConfiguracaoSite
  views.py               # home, categoria_detalhe, conteudo_detalhe, busca
  admin.py               # Admin customizado com badges, widgets visuais, moderação
  forms.py               # ConteudoAdminForm, BannerAdminForm (ligam os widgets visuais)
  widgets.py             # CategoriaPicker (grade de categorias) e IconPicker (grade de ícones)
  urls.py                # app_name='conteudo'
  context_processors.py  # site_config (config + menu_categorias global)
  migrations/            # 0001 inicial → 0005 (icone_manual do Conteudo)
  management/commands/
    popular_categorias.py   # Seed de categorias e subcategorias
    popular_descricoes.py   # Textos introdutórios das categorias (HTML)
    migrar_conteudo.py      # 102 itens de conteúdo migrados do WordPress
templates/
  base.html              # Layout base (header, nav dinâmica, footer, ícone discreto de admin)
  home.html              # Home: hero/banners, "Conteúdos recentes" (esquerda) + "Navegue por área" (direita)
  categoria.html         # Lista de conteúdos com filtros, banners de categoria, índice geral (55 botões)
  conteudo_detalhe.html  # Detalhe de conteúdo + seção de comentários (com moderação)
  busca.html             # Resultados de busca
static/
  css/style.css          # Design system completo
  css/admin_picker.css   # Estilos dos widgets visuais do admin (CategoriaPicker, IconPicker)
  js/main.js             # Slider do hero, menu mobile
  img/                   # brasao.png, logo-geceb.png, hero-bg.png
staticfiles/             # Gerado por collectstatic (produção/PythonAnywhere) — não editar
media/                   # Uploads (banners/, destaques/) — não versionado no Git
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
- `icone_manual` (opcional) — ícone Font Awesome escolhido no admin via grade visual (IconPicker); se vazio, usa `icone_criativo` (automático por palavra-chave)
- `destaque` (bool) — aparece na home
- Propriedades: `tipo_icone`, `icone_criativo` (prioriza `icone_manual`, senão detecta por texto), `extensao_arquivo`, `get_video_embed_url()`
- No admin, a categoria de publicação é escolhida clicando em um botão visual (`CategoriaPicker`), não em um dropdown

### Banner
Banners rotativos — na home (`categoria=None`) ou dentro de uma categoria específica (`categoria=<FK>`). Campos: `titulo`, `subtitulo`, `imagem`, `link`, `ordem`, `ativo`, `categoria`, `tamanho` (`pequeno`/`medio`/`grande`, controla a altura de exibição).
- No admin, a área de exibição também é escolhida via botão visual (`CategoriaPicker` com opção extra "Página inicial")
- A imagem nunca é cortada nem distorcida no site — o CSS usa a própria imagem borrada como fundo (efeito letterbox) atrás da imagem original em tamanho real (`object-fit: contain`)

### Comentario
Sistema de comentários com moderação, substituindo o Disqus do WordPress. Campos: `conteudo` (FK), `nome`, `email`, `texto`, `aprovado` (bool, padrão `False`), `data_criacao`.
- Comentários enviados no site ficam pendentes até serem aprovados no admin (`ComentarioAdmin`, com ação em lote "Aprovar")
- Só comentários com `aprovado=True` aparecem na página de detalhe do conteúdo

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

## Deploy (PythonAnywhere)

O site está publicado para teste em **https://rabalista.pythonanywhere.com** (ver também "Onde os arquivos ficam armazenados" mais abaixo).

- **Usuário PythonAnywhere:** `rabalista`
- **Pasta do projeto no servidor:** `/home/rabalista/site-curriculos-sedu/`
- **Arquivo WSGI:** `/var/www/rabalista_pythonanywhere_com_wsgi.py` (força `ALLOWED_HOSTS = ['*']` e `DEBUG = False` após carregar o settings — remover essa sobrescrita se `ALLOWED_HOSTS` for restringido no `settings.py` futuramente)
- **Static files** (aba Web → Static files): URL `/static/` → Directory `/home/rabalista/site-curriculos-sedu/staticfiles`
- **Media files** (uploads): URL `/media/` → Directory `/home/rabalista/site-curriculos-sedu/media`

Fluxo para publicar mudanças feitas localmente:

```bash
# No terminal Bash do PythonAnywhere
cd ~/site-curriculos-sedu
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Depois, na aba **Web** do PythonAnywhere, clicar em **Reload**.

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
- [x] Página home reorganizada: "Conteúdos recentes" à esquerda, "Navegue por área" à direita
- [x] Página de categoria com subcategorias, filtros por tipo e textos introdutórios
- [x] Página-índice "Documentos Curriculares" com os 55 botões de subcategorias (como no site antigo), em ordem alfabética
- [x] Página de detalhe de conteúdo com relacionados
- [x] Busca textual
- [x] Migração de 102 conteúdos do site original WordPress
- [x] 16 textos introdutórios das categorias extraídos do site original
- [x] Header com logos (brasão ES + GECEB) sem distorção de cores
- [x] Ícones criativos por palavra-chave (substituem a seta genérica de "link externo")
- [x] Seletor visual de ícone por conteúdo no admin (`IconPicker`), sobrepondo o automático
- [x] Sistema de comentários com moderação no admin (substitui o Disqus do WordPress)
- [x] Ícone discreto de acesso ao admin no rodapé do site
- [x] Admin com seleção visual de categoria/área (`CategoriaPicker`), tanto para Conteúdo quanto para Banner
- [x] Banners rotativos por área (home ou categoria específica), com imagem nunca cortada/distorcida e tamanho configurável (pequeno/médio/grande)
- [x] Deploy de teste em produção no PythonAnywhere (https://rabalista.pythonanywhere.com)

## O que falta / próximos passos possíveis

- [ ] Adicionar imagens de destaque aos demais conteúdos
- [ ] Refinamentos visuais conforme feedback do Dan e aprovação do chefe
- [ ] Migrar para domínio oficial `curriculo.sedu.es.gov.br` + certificado SSL
- [ ] Deploy final com Docker + PostgreSQL para produção definitiva
- [ ] Testar em Windows (ambiente de trabalho do Dan)
- [ ] Melhorar responsividade mobile
- [ ] Adicionar paginação nas listagens de conteúdo

## Notas importantes

- O banco `db.sqlite3` já contém todos os dados migrados. Não precisa rodar os commands novamente a menos que queira resetar.
- Os conteúdos tipo `link` e `documento` apontam para URLs externas (Google Drive, SEDU, etc.) — os arquivos PDF não estão armazenados localmente.
- O site original em WordPress está em: `curriculo.sedu.es.gov.br/curriculo/`
- O usuário não tem conhecimento de programação — sempre forneça comandos prontos para copiar e colar.
- Widgets visuais do admin (`CategoriaPicker`, `IconPicker`) carregam o Font Awesome via CDN na própria `Media` da classe, pois o admin do Django não inclui o CDN usado no site público (`templates/base.html`).
- O CSS dos widgets (`admin_picker.css`) usa `!important` em vários pontos porque o CSS padrão do Django Admin estiliza `<label>` genericamente (largura fixa, `display: block`), o que sobrescreveria a grade de botões sem isso.
