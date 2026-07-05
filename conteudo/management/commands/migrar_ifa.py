"""
Cria a categoria principal "Itinerários Formativos de Aprofundamento (IFA)"
com subcategorias e documentos migrados de:
https://curriculo.sedu.es.gov.br/curriculo/documentos/

Idempotente — pode rodar múltiplas vezes sem duplicar dados.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from conteudo.models import Categoria, Conteudo

B = 'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/'
REF = B + '2023/01/Referenciais-Curriculares-para-Elaboracao-de-Itinerarios-Formativos-1-1.pdf'

# (nome_subcategoria, icone, [(titulo_doc, url_pdf), ...])
SUBCATEGORIAS = [
    ('Documentos Gerais dos IFAs', 'fas fa-file-alt', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Orientações para Elaboração dos Projetos Integradores dos IFAs',
         B + '2025/12/ORIENTACOES-PARA-ELABORACAO-DOS-PROJETOS-INTEGRADORES-3.pdf'),
        ('IFA — Quatro Áreas do Conhecimento (Noturno)',
         B + '2025/12/IFA-DAS-QUATRO-AREAS-DO-CONHECIMENTO-FINALIZADO.pdf'),
        ('IFA — Linguagens e Ciências Humanas e Sociais Aplicadas',
         B + '2025/12/IFA-LINGCHSA-6-1.pdf'),
        ('IFA — Matemática e Ciências da Natureza e suas Tecnologias',
         B + '2025/12/IFA-CNTMAT.pdf'),
    ]),
    ('Educação Financeira e Fiscal', 'fas fa-coins', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Educação Financeira e Fiscal (Matemática)',
         B + '2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf'),
    ]),
    ('Terra, Vida e Cosmo', 'fas fa-globe', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Terra, Vida e Cosmo (Ciências da Natureza)',
         B + '2022/04/Curriculo-EM_Aprofundamento-da-area_-CN_-Alterado_-20_04_22.pdf'),
    ]),
    ('Mídias Digitais: Linguagens em Ação', 'fas fa-film', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Mídias Digitais: Linguagens em Ação (Linguagens)',
         B + '2022/04/Curriculo-EM_Aprofundamento-da-area_-Linguagens_Alterado_19-04.pdf'),
    ]),
    ('Modernização, Transformação Social e Meio Ambiente', 'fas fa-leaf', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Modernização, Transformação Social e Meio Ambiente (Ciências Humanas)',
         B + '2022/04/CurriculoEM_Aprofundamento-da-area-de-CHSA.pdf'),
    ]),
    ('O Esporte, a Ciência e suas Linguagens', 'fas fa-running', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — O Esporte, a Ciência e suas Linguagens (CN e Linguagens)',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_-CN.e-Linguagens_Alterado_20_04_22.pdf'),
    ]),
    ('Energias Renováveis e Eficiência Energética', 'fas fa-solar-panel', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Energias Renováveis e Eficiência Energética (CN, Mat e Linguagens)',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_CN-CHSA-Mat-e-Linguagens_Alterado_20_04_22.pdf'),
    ]),
    ('Narrativas Socioliterárias', 'fas fa-book-open', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Narrativas Socioliterárias: Literatura, Arte e Ciências Humanas',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_CHSA-e-Linguagens_Alterado-20_04_22.pdf'),
    ]),
    ('Humanidades e Relações Socioambientais', 'fas fa-users', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Humanidades e Relações Socioambientais (CN e Ciências Humanas)',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_-CHSA-e-CN_alterado_20-04-22.pdf'),
    ]),
    ('Aspirações Docentes', 'fas fa-chalkboard-teacher', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Documento Curricular — Aspirações Docentes (Linguagens, Matemática, CN e Ciências Humanas)',
         B + '2022/04/Aspiracoes-Docentes-versao-revisada.pdf'),
    ]),
]


class Command(BaseCommand):
    help = 'Migra Itinerários Formativos de Aprofundamento (IFA) do WordPress'

    def handle(self, *args, **options):
        # Categoria principal
        cat_principal, criada = Categoria.objects.get_or_create(
            slug='itinerarios-formativos-ifa',
            defaults={
                'nome': 'Itinerários Formativos de Aprofundamento (IFA)',
                'descricao': '<p>Documentos curriculares dos <strong>Itinerários Formativos de Aprofundamento (IFA)</strong> do Ensino Médio do Espírito Santo, organizados por área de conhecimento.</p>',
                'icone': 'fas fa-route',
                'ordem': 3,
                'ativa': True,
            }
        )
        if criada:
            self.stdout.write(f'  ✔ Categoria principal criada: {cat_principal.nome}')
        else:
            self.stdout.write(f'  — Categoria já existe: {cat_principal.nome}')

        total_subs = 0
        total_docs = 0

        for ordem_sub, (nome_sub, icone_sub, docs) in enumerate(SUBCATEGORIAS, start=1):
            slug_sub = nome_sub.lower()
            slug_sub = ''.join(c if c.isalnum() or c == '-' else '-' for c in
                               slug_sub.replace('ç', 'c').replace('ã', 'a').replace('á', 'a')
                               .replace('é', 'e').replace('ê', 'e').replace('í', 'i')
                               .replace('ó', 'o').replace('ô', 'o').replace('ú', 'u')
                               .replace('â', 'a').replace('õ', 'o').replace('à', 'a')
                               .replace(' ', '-').replace(':', '').replace(',', ''))
            slug_sub = f'ifa-{slug_sub[:40]}'.strip('-')

            sub, criada_sub = Categoria.objects.get_or_create(
                slug=slug_sub,
                defaults={
                    'nome': nome_sub,
                    'icone': icone_sub,
                    'categoria_pai': cat_principal,
                    'ordem': ordem_sub,
                    'ativa': True,
                }
            )
            if criada_sub:
                total_subs += 1

            for titulo, url in docs:
                slug_doc = titulo.lower()
                slug_doc = ''.join(c if c.isalnum() or c == '-' else '-' for c in
                                   slug_doc.replace('ç', 'c').replace('ã', 'a').replace('á', 'a')
                                   .replace('é', 'e').replace('ê', 'e').replace('í', 'i')
                                   .replace('ó', 'o').replace('ô', 'o').replace('ú', 'u')
                                   .replace('â', 'a').replace('õ', 'o').replace('à', 'a')
                                   .replace(' ', '-').replace(':', '').replace(',', '')
                                   .replace('"', '').replace("'", ''))
                slug_doc = f'ifa-{slug_doc[:50]}'.strip('-')

                if not Conteudo.objects.filter(url_externa=url).exists():
                    Conteudo.objects.create(
                        titulo=titulo,
                        slug=slug_doc,
                        tipo='link',
                        status='publicado',
                        url_externa=url,
                        categoria=sub,
                        data_publicacao=timezone.now(),
                    )
                    total_docs += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: 1 categoria principal, {total_subs} subcategorias criadas, '
            f'{total_docs} documentos criados.'
        ))
