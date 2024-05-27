import csv
import glob
import gzip
import json
import os

SNAPSHOT_DIR = 'openalex-snapshot'
CSV_DIR = 'csv-files'

if not os.path.exists(CSV_DIR):
    os.mkdir(CSV_DIR)

FILES_PER_ENTITY = int(os.environ.get('OPENALEX_DEMO_FILES_PER_ENTITY', '0'))

csv_files = {
    'authors': {
        'authors': {
            'name': os.path.join(CSV_DIR, 'authors.csv.gz'),
            'columns': [
                'id', 'orcid', 'display_name', 'display_name_alternatives',
                'works_count', 'cited_by_count',
                'last_known_institution', 'works_api_url', 'updated_date',
            ]
        },
        'ids': {
            'name': os.path.join(CSV_DIR, 'authors_ids.csv.gz'),
            'columns': [
                'author_id', 'openalex', 'orcid', 'scopus', 'twitter',
                'wikipedia', 'mag'
            ]
        },
        'counts_by_year': {
            'name': os.path.join(CSV_DIR, 'authors_counts_by_year.csv.gz'),
            'columns': [
                'author_id', 'year', 'works_count', 'cited_by_count',
                'oa_works_count'
            ]
        }
    },
    'concepts': {
        'concepts': {
            'name': os.path.join(CSV_DIR, 'concepts.csv.gz'),
            'columns': [
                'id', 'wikidata', 'display_name', 'level', 'description',
                'works_count', 'cited_by_count', 'image_url',
                'image_thumbnail_url', 'works_api_url', 'updated_date'
            ]
        },
        'ancestors': {
            'name': os.path.join(CSV_DIR, 'concepts_ancestors.csv.gz'),
            'columns': ['concept_id', 'ancestor_id']
        },
        'counts_by_year': {
            'name': os.path.join(CSV_DIR, 'concepts_counts_by_year.csv.gz'),
            'columns': ['concept_id', 'year', 'works_count', 'cited_by_count',
                        'oa_works_count']
        },
        'ids': {
            'name': os.path.join(CSV_DIR, 'concepts_ids.csv.gz'),
            'columns': ['concept_id', 'openalex', 'wikidata', 'wikipedia',
                        'umls_aui', 'umls_cui', 'mag']
        },
        'related_concepts': {
            'name': os.path.join(CSV_DIR, 'concepts_related_concepts.csv.gz'),
            'columns': ['concept_id', 'related_concept_id', 'score']
        }
    },
    'topics': {
        'topics': {
            'name': os.path.join(CSV_DIR, 'topics.csv.gz'),
            'columns': ['id', 'display_name', 'subfield_id',
                        'subfield_display_name', 'field_id',
                        'field_display_name',
                        'domain_id', 'domain_display_name', 'description',
                        'keywords', 'works_api_url', 'wikipedia_id',
                        'works_count', 'cited_by_count', 'updated_date', 'siblings']
        }
    },
    'institutions': {
        'institutions': {
            'name': os.path.join(CSV_DIR, 'institutions.csv.gz'),
            'columns': [
                'id', 'ror', 'display_name', 'country_code', 'type',
                'homepage_url', 'image_url', 'image_thumbnail_url',
                'display_name_acronyms', 'display_name_alternatives',
                'works_count', 'cited_by_count', 'works_api_url',
                'updated_date'
            ]
        },
        'ids': {
            'name': os.path.join(CSV_DIR, 'institutions_ids.csv.gz'),
            'columns': [
                'institution_id', 'openalex', 'ror', 'grid', 'wikipedia',
                'wikidata', 'mag'
            ]
        },
        'geo': {
            'name': os.path.join(CSV_DIR, 'institutions_geo.csv.gz'),
            'columns': [
                'institution_id', 'city', 'geonames_city_id', 'region',
                'country_code', 'country', 'latitude',
                'longitude'
            ]
        },
        'associated_institutions': {
            'name': os.path.join(CSV_DIR,
                                 'institutions_associated_institutions.csv.gz'),
            'columns': [
                'institution_id', 'associated_institution_id', 'relationship'
            ]
        },
        'counts_by_year': {
            'name': os.path.join(CSV_DIR, 'institutions_counts_by_year.csv.gz'),
            'columns': [
                'institution_id', 'year', 'works_count', 'cited_by_count',
                'oa_works_count'
            ]
        }
    },
    'publishers': {
        'publishers': {
            'name': os.path.join(CSV_DIR, 'publishers.csv.gz'),
            'columns': [
                'id', 'display_name', 'alternate_titles', 'country_codes',
                'hierarchy_level', 'parent_publisher',
                'works_count', 'cited_by_count', 'sources_api_url',
                'updated_date'
            ]
        },
        'counts_by_year': {
            'name': os.path.join(CSV_DIR, 'publishers_counts_by_year.csv.gz'),
            'columns': ['publisher_id', 'year', 'works_count', 'cited_by_count',
                        'oa_works_count']
        },
        'ids': {
            'name': os.path.join(CSV_DIR, 'publishers_ids.csv.gz'),
            'columns': ['publisher_id', 'openalex', 'ror', 'wikidata']
        },
    },
    'sources': {
        'sources': {
            'name': os.path.join(CSV_DIR, 'sources.csv.gz'),
            'columns': [
                'id', 'issn_l', 'issn', 'display_name', 'publisher',
                'works_count', 'cited_by_count', 'is_oa',
                'is_in_doaj', 'homepage_url', 'works_api_url', 'updated_date'
            ]
        },
        'ids': {
            'name': os.path.join(CSV_DIR, 'sources_ids.csv.gz'),
            'columns': ['source_id', 'openalex', 'issn_l', 'issn', 'mag',
                        'wikidata', 'fatcat']
        },
        'counts_by_year': {
            'name': os.path.join(CSV_DIR, 'sources_counts_by_year.csv.gz'),
            'columns': ['source_id', 'year', 'works_count', 'cited_by_count',
                        'oa_works_count']
        },
    },
    'works': {
        'works': {
            'name': os.path.join(CSV_DIR, 'works.csv.gz'),
            'columns': [
                'id', 'doi', 'title', 'display_name', 'publication_year',
                'publication_date', 'type', 'cited_by_count',
                'is_retracted', 'is_paratext', 'cited_by_api_url',
                'abstract_inverted_index', 'language'
            ]
        },
        'primary_locations': {
            'name': os.path.join(CSV_DIR, 'works_primary_locations.csv.gz'),
            'columns': [
                'work_id', 'source_id', 'landing_page_url', 'pdf_url', 'is_oa',
                'version', 'license'
            ]
        },
        'locations': {
            'name': os.path.join(CSV_DIR, 'works_locations.csv.gz'),
            'columns': [
                'work_id', 'source_id', 'landing_page_url', 'pdf_url', 'is_oa',
                'version', 'license'
            ]
        },
        'best_oa_locations': {
            'name': os.path.join(CSV_DIR, 'works_best_oa_locations.csv.gz'),
            'columns': [
                'work_id', 'source_id', 'landing_page_url', 'pdf_url', 'is_oa',
                'version', 'license'
            ]
        },
        'authorships': {
            'name': os.path.join(CSV_DIR, 'works_authorships.csv.gz'),
            'columns': [
                'work_id', 'author_position', 'author_id', 'institution_id',
                'raw_affiliation_string'
            ]
        },
        'biblio': {
            'name': os.path.join(CSV_DIR, 'works_biblio.csv.gz'),
            'columns': [
                'work_id', 'volume', 'issue', 'first_page', 'last_page'
            ]
        },
        'topics': {
            'name': os.path.join(CSV_DIR, 'works_topics.csv.gz'),
            'columns': [
                'work_id', 'topic_id', 'score'
            ]
        },
        'concepts': {
            'name': os.path.join(CSV_DIR, 'works_concepts.csv.gz'),
            'columns': [
                'work_id', 'concept_id', 'score'
            ]
        },
        'ids': {
            'name': os.path.join(CSV_DIR, 'works_ids.csv.gz'),
            'columns': [
                'work_id', 'openalex', 'doi', 'mag', 'pmid', 'pmcid'
            ]
        },
        'mesh': {
            'name': os.path.join(CSV_DIR, 'works_mesh.csv.gz'),
            'columns': [
                'work_id', 'descriptor_ui', 'descriptor_name', 'qualifier_ui',
                'qualifier_name', 'is_major_topic'
            ]
        },
        'open_access': {
            'name': os.path.join(CSV_DIR, 'works_open_access.csv.gz'),
            'columns': [
                'work_id', 'is_oa', 'oa_status', 'oa_url',
                'any_repository_has_fulltext'
            ]
        },
        'referenced_works': {
            'name': os.path.join(CSV_DIR, 'works_referenced_works.csv.gz'),
            'columns': [
                'work_id', 'referenced_work_id'
            ]
        },
        'related_works': {
            'name': os.path.join(CSV_DIR, 'works_related_works.csv.gz'),
            'columns': [
                'work_id', 'related_work_id'
            ]
        },
    },
}


def flatten_authors():
    file_spec = csv_files['authors']

    with gzip.open(file_spec['authors']['name'], 'wt',
                   encoding='utf-8') as authors_csv, \
            gzip.open(file_spec['ids']['name'], 'wt',
                      encoding='utf-8') as ids_csv, \
            gzip.open(file_spec['counts_by_year']['name'], 'wt',
                      encoding='utf-8') as counts_by_year_csv:

        authors_writer = csv.DictWriter(
            authors_csv, fieldnames=file_spec['authors']['columns'],
            extrasaction='ignore'
        )
        authors_writer.writeheader()

        ids_writer = csv.DictWriter(ids_csv,
                                    fieldnames=file_spec['ids']['columns'])
        ids_writer.writeheader()

        counts_by_year_writer = csv.DictWriter(counts_by_year_csv, fieldnames=
        file_spec['counts_by_year']['columns'])
        counts_by_year_writer.writeheader()

        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'authors', '*', '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as authors_jsonl:
                for author_json in authors_jsonl:
                    if not author_json.strip():
                        continue

                    author = json.loads(author_json)

                    if not (author_id := author.get('id')):
                        continue

                    # authors
                    author['display_name_alternatives'] = json.dumps(
                        author.get('display_name_alternatives'),
                        ensure_ascii=False)
                    author['last_known_institution'] = (
                                author.get('last_known_institution') or {}).get(
                        'id')
                    authors_writer.writerow(author)

                    # ids
                    if author_ids := author.get('ids'):
                        author_ids['author_id'] = author_id
                        ids_writer.writerow(author_ids)

                    # counts_by_year
                    if counts_by_year := author.get('counts_by_year'):
                        for count_by_year in counts_by_year:
                            count_by_year['author_id'] = author_id
                            counts_by_year_writer.writerow(count_by_year)
            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def flatten_topics():
    with gzip.open(csv_files['topics']['topics']['name'], 'wt',
                   encoding='utf-8') as topics_csv:
        topics_writer = csv.DictWriter(topics_csv,
                                       fieldnames=csv_files['topics']['topics'][
                                           'columns'])
        topics_writer.writeheader()

        seen_topic_ids = set()
        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'topics', '*', '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as topics_jsonl:
                for line in topics_jsonl:
                    if not line.strip():
                        continue
                    topic = json.loads(line)
                    topic['keywords'] = '; '.join(topic.get('keywords', ''))
                    if not (
                    topic_id := topic.get('id')) or topic_id in seen_topic_ids:
                        continue
                    seen_topic_ids.add(topic_id)
                    for key in ('subfield', 'field', 'domain'):
                        topic[f'{key}_id'] = topic[key]['id']
                        topic[f'{key}_display_name'] = topic[key]['display_name']
                        del topic[key]
                    topic['updated_date'] = topic['updated']
                    del topic['updated']
                    topic['wikipedia_id'] = topic['ids'].get('wikipedia')
                    del topic['ids']
                    del topic['created_date']
                    topics_writer.writerow(topic)
            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def flatten_concepts():
    with gzip.open(csv_files['concepts']['concepts']['name'], 'wt',
                   encoding='utf-8') as concepts_csv, \
            gzip.open(csv_files['concepts']['ancestors']['name'], 'wt',
                      encoding='utf-8') as ancestors_csv, \
            gzip.open(csv_files['concepts']['counts_by_year']['name'], 'wt',
                      encoding='utf-8') as counts_by_year_csv, \
            gzip.open(csv_files['concepts']['ids']['name'], 'wt',
                      encoding='utf-8') as ids_csv, \
            gzip.open(csv_files['concepts']['related_concepts']['name'], 'wt',
                      encoding='utf-8') as related_concepts_csv:

        concepts_writer = csv.DictWriter(
            concepts_csv,
            fieldnames=csv_files['concepts']['concepts']['columns'],
            extrasaction='ignore'
        )
        concepts_writer.writeheader()

        ancestors_writer = csv.DictWriter(ancestors_csv, fieldnames=
        csv_files['concepts']['ancestors']['columns'])
        ancestors_writer.writeheader()

        counts_by_year_writer = csv.DictWriter(counts_by_year_csv, fieldnames=
        csv_files['concepts']['counts_by_year']['columns'])
        counts_by_year_writer.writeheader()

        ids_writer = csv.DictWriter(ids_csv,
                                    fieldnames=csv_files['concepts']['ids'][
                                        'columns'])
        ids_writer.writeheader()

        related_concepts_writer = csv.DictWriter(related_concepts_csv,
                                                 fieldnames=
                                                 csv_files['concepts'][
                                                     'related_concepts'][
                                                     'columns'])
        related_concepts_writer.writeheader()

        seen_concept_ids = set()

        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'concepts', '*', '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as concepts_jsonl:
                for concept_json in concepts_jsonl:
                    if not concept_json.strip():
                        continue

                    concept = json.loads(concept_json)

                    if not (concept_id := concept.get(
                            'id')) or concept_id in seen_concept_ids:
                        continue

                    seen_concept_ids.add(concept_id)

                    concepts_writer.writerow(concept)

                    if concept_ids := concept.get('ids'):
                        concept_ids['concept_id'] = concept_id
                        concept_ids['umls_aui'] = json.dumps(
                            concept_ids.get('umls_aui'), ensure_ascii=False)
                        concept_ids['umls_cui'] = json.dumps(
                            concept_ids.get('umls_cui'), ensure_ascii=False)
                        ids_writer.writerow(concept_ids)

                    if ancestors := concept.get('ancestors'):
                        for ancestor in ancestors:
                            if ancestor_id := ancestor.get('id'):
                                ancestors_writer.writerow({
                                    'concept_id': concept_id,
                                    'ancestor_id': ancestor_id
                                })

                    if counts_by_year := concept.get('counts_by_year'):
                        for count_by_year in counts_by_year:
                            count_by_year['concept_id'] = concept_id
                            counts_by_year_writer.writerow(count_by_year)

                    if related_concepts := concept.get('related_concepts'):
                        for related_concept in related_concepts:
                            if related_concept_id := related_concept.get('id'):
                                related_concepts_writer.writerow({
                                    'concept_id': concept_id,
                                    'related_concept_id': related_concept_id,
                                    'score': related_concept.get('score')
                                })

            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def flatten_institutions():
    file_spec = csv_files['institutions']

    with gzip.open(file_spec['institutions']['name'], 'wt',
                   encoding='utf-8') as institutions_csv, \
            gzip.open(file_spec['ids']['name'], 'wt',
                      encoding='utf-8') as ids_csv, \
            gzip.open(file_spec['geo']['name'], 'wt',
                      encoding='utf-8') as geo_csv, \
            gzip.open(file_spec['associated_institutions']['name'], 'wt',
                      encoding='utf-8') as associated_institutions_csv, \
            gzip.open(file_spec['counts_by_year']['name'], 'wt',
                      encoding='utf-8') as counts_by_year_csv:

        institutions_writer = csv.DictWriter(
            institutions_csv, fieldnames=file_spec['institutions']['columns'],
            extrasaction='ignore'
        )
        institutions_writer.writeheader()

        ids_writer = csv.DictWriter(ids_csv,
                                    fieldnames=file_spec['ids']['columns'])
        ids_writer.writeheader()

        geo_writer = csv.DictWriter(geo_csv,
                                    fieldnames=file_spec['geo']['columns'])
        geo_writer.writeheader()

        associated_institutions_writer = csv.DictWriter(
            associated_institutions_csv,
            fieldnames=file_spec['associated_institutions']['columns']
        )
        associated_institutions_writer.writeheader()

        counts_by_year_writer = csv.DictWriter(counts_by_year_csv, fieldnames=
        file_spec['counts_by_year']['columns'])
        counts_by_year_writer.writeheader()

        seen_institution_ids = set()

        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'institutions', '*',
                             '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as institutions_jsonl:
                for institution_json in institutions_jsonl:
                    if not institution_json.strip():
                        continue

                    institution = json.loads(institution_json)

                    if not (institution_id := institution.get(
                            'id')) or institution_id in seen_institution_ids:
                        continue

                    seen_institution_ids.add(institution_id)

                    # institutions
                    institution['display_name_acronyms'] = json.dumps(
                        institution.get('display_name_acronyms'),
                        ensure_ascii=False)
                    institution['display_name_alternatives'] = json.dumps(
                        institution.get('display_name_alternatives'),
                        ensure_ascii=False)
                    institutions_writer.writerow(institution)

                    # ids
                    if institution_ids := institution.get('ids'):
                        institution_ids['institution_id'] = institution_id
                        ids_writer.writerow(institution_ids)

                    # geo
                    if institution_geo := institution.get('geo'):
                        institution_geo['institution_id'] = institution_id
                        geo_writer.writerow(institution_geo)

                    # associated_institutions
                    if associated_institutions := institution.get(
                            'associated_institutions',
                            institution.get('associated_insitutions')
                            # typo in api
                    ):
                        for associated_institution in associated_institutions:
                            if associated_institution_id := associated_institution.get(
                                    'id'):
                                associated_institutions_writer.writerow({
                                    'institution_id': institution_id,
                                    'associated_institution_id': associated_institution_id,
                                    'relationship': associated_institution.get(
                                        'relationship')
                                })

                    # counts_by_year
                    if counts_by_year := institution.get('counts_by_year'):
                        for count_by_year in counts_by_year:
                            count_by_year['institution_id'] = institution_id
                            counts_by_year_writer.writerow(count_by_year)

            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def flatten_publishers():
    with gzip.open(csv_files['publishers']['publishers']['name'], 'wt',
                   encoding='utf-8') as publishers_csv, \
            gzip.open(csv_files['publishers']['counts_by_year']['name'], 'wt',
                      encoding='utf-8') as counts_by_year_csv, \
            gzip.open(csv_files['publishers']['ids']['name'], 'wt',
                      encoding='utf-8') as ids_csv:

        publishers_writer = csv.DictWriter(
            publishers_csv,
            fieldnames=csv_files['publishers']['publishers']['columns'],
            extrasaction='ignore'
        )
        publishers_writer.writeheader()

        counts_by_year_writer = csv.DictWriter(counts_by_year_csv, fieldnames=
        csv_files['publishers']['counts_by_year']['columns'])
        counts_by_year_writer.writeheader()

        ids_writer = csv.DictWriter(ids_csv,
                                    fieldnames=csv_files['publishers']['ids'][
                                        'columns'])
        ids_writer.writeheader()

        seen_publisher_ids = set()

        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'publishers', '*', '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as concepts_jsonl:
                for publisher_json in concepts_jsonl:
                    if not publisher_json.strip():
                        continue

                    publisher = json.loads(publisher_json)

                    if not (publisher_id := publisher.get(
                            'id')) or publisher_id in seen_publisher_ids:
                        continue

                    seen_publisher_ids.add(publisher_id)

                    # publishers
                    publisher['alternate_titles'] = json.dumps(
                        publisher.get('alternate_titles'), ensure_ascii=False)
                    publisher['country_codes'] = json.dumps(
                        publisher.get('country_codes'), ensure_ascii=False)
                    publishers_writer.writerow(publisher)

                    if publisher_ids := publisher.get('ids'):
                        publisher_ids['publisher_id'] = publisher_id
                        ids_writer.writerow(publisher_ids)

                    if counts_by_year := publisher.get('counts_by_year'):
                        for count_by_year in counts_by_year:
                            count_by_year['publisher_id'] = publisher_id
                            counts_by_year_writer.writerow(count_by_year)

            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def flatten_sources():
    with gzip.open(csv_files['sources']['sources']['name'], 'wt',
                   encoding='utf-8') as sources_csv, \
            gzip.open(csv_files['sources']['ids']['name'], 'wt',
                      encoding='utf-8') as ids_csv, \
            gzip.open(csv_files['sources']['counts_by_year']['name'], 'wt',
                      encoding='utf-8') as counts_by_year_csv:

        sources_writer = csv.DictWriter(
            sources_csv, fieldnames=csv_files['sources']['sources']['columns'],
            extrasaction='ignore'
        )
        sources_writer.writeheader()

        ids_writer = csv.DictWriter(ids_csv,
                                    fieldnames=csv_files['sources']['ids'][
                                        'columns'])
        ids_writer.writeheader()

        counts_by_year_writer = csv.DictWriter(counts_by_year_csv, fieldnames=
        csv_files['sources']['counts_by_year']['columns'])
        counts_by_year_writer.writeheader()

        seen_source_ids = set()

        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'sources', '*', '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as sources_jsonl:
                for source_json in sources_jsonl:
                    if not source_json.strip():
                        continue

                    source = json.loads(source_json)

                    if not (source_id := source.get(
                            'id')) or source_id in seen_source_ids:
                        continue

                    seen_source_ids.add(source_id)

                    source['issn'] = json.dumps(source.get('issn'))
                    sources_writer.writerow(source)

                    if source_ids := source.get('ids'):
                        source_ids['source_id'] = source_id
                        source_ids['issn'] = json.dumps(source_ids.get('issn'))
                        ids_writer.writerow(source_ids)

                    if counts_by_year := source.get('counts_by_year'):
                        for count_by_year in counts_by_year:
                            count_by_year['source_id'] = source_id
                            counts_by_year_writer.writerow(count_by_year)

            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def flatten_works():
    file_spec = csv_files['works']

    with gzip.open(file_spec['works']['name'], 'wt',
                   encoding='utf-8') as works_csv, \
            gzip.open(file_spec['primary_locations']['name'], 'wt',
                      encoding='utf-8') as primary_locations_csv, \
            gzip.open(file_spec['locations']['name'], 'wt',
                      encoding='utf-8') as locations, \
            gzip.open(file_spec['best_oa_locations']['name'], 'wt',
                      encoding='utf-8') as best_oa_locations, \
            gzip.open(file_spec['authorships']['name'], 'wt',
                      encoding='utf-8') as authorships_csv, \
            gzip.open(file_spec['biblio']['name'], 'wt',
                      encoding='utf-8') as biblio_csv, \
            gzip.open(file_spec['topics']['name'], 'wt',
                      encoding='utf-8') as topics_csv, \
            gzip.open(file_spec['concepts']['name'], 'wt',
                      encoding='utf-8') as concepts_csv, \
            gzip.open(file_spec['ids']['name'], 'wt',
                      encoding='utf-8') as ids_csv, \
            gzip.open(file_spec['mesh']['name'], 'wt',
                      encoding='utf-8') as mesh_csv, \
            gzip.open(file_spec['open_access']['name'], 'wt',
                      encoding='utf-8') as open_access_csv, \
            gzip.open(file_spec['referenced_works']['name'], 'wt',
                      encoding='utf-8') as referenced_works_csv, \
            gzip.open(file_spec['related_works']['name'], 'wt',
                      encoding='utf-8') as related_works_csv:

        works_writer = init_dict_writer(works_csv, file_spec['works'],
                                        extrasaction='ignore')
        primary_locations_writer = init_dict_writer(primary_locations_csv,
                                                    file_spec[
                                                        'primary_locations'])
        locations_writer = init_dict_writer(locations, file_spec['locations'])
        best_oa_locations_writer = init_dict_writer(best_oa_locations,
                                                    file_spec[
                                                        'best_oa_locations'])
        authorships_writer = init_dict_writer(authorships_csv,
                                              file_spec['authorships'])
        biblio_writer = init_dict_writer(biblio_csv, file_spec['biblio'])
        topics_writer = init_dict_writer(topics_csv, file_spec['topics'])
        concepts_writer = init_dict_writer(concepts_csv, file_spec['concepts'])
        ids_writer = init_dict_writer(ids_csv, file_spec['ids'],
                                      extrasaction='ignore')
        mesh_writer = init_dict_writer(mesh_csv, file_spec['mesh'])
        open_access_writer = init_dict_writer(open_access_csv,
                                              file_spec['open_access'])
        referenced_works_writer = init_dict_writer(referenced_works_csv,
                                                   file_spec[
                                                       'referenced_works'])
        related_works_writer = init_dict_writer(related_works_csv,
                                                file_spec['related_works'])

        files_done = 0
        for jsonl_file_name in glob.glob(
                os.path.join(SNAPSHOT_DIR, 'data', 'works', '*', '*.gz')):
            print(jsonl_file_name)
            with gzip.open(jsonl_file_name, 'r') as works_jsonl:
                for work_json in works_jsonl:
                    if not work_json.strip():
                        continue

                    work = json.loads(work_json)

                    if not (work_id := work.get('id')):
                        continue

                    # works
                    if (abstract := work.get(
                            'abstract_inverted_index')) is not None:
                        work['abstract_inverted_index'] = json.dumps(abstract,
                                                                     ensure_ascii=False)

                    works_writer.writerow(work)

                    # primary_locations
                    if primary_location := (work.get('primary_location') or {}):
                        if primary_location.get(
                                'source') and primary_location.get(
                                'source').get('id'):
                            primary_locations_writer.writerow({
                                'work_id': work_id,
                                'source_id': primary_location['source']['id'],
                                'landing_page_url': primary_location.get(
                                    'landing_page_url'),
                                'pdf_url': primary_location.get('pdf_url'),
                                'is_oa': primary_location.get('is_oa'),
                                'version': primary_location.get('version'),
                                'license': primary_location.get('license'),
                            })

                    # locations
                    if locations := work.get('locations'):
                        for location in locations:
                            if location.get('source') and location.get(
                                    'source').get('id'):
                                locations_writer.writerow({
                                    'work_id': work_id,
                                    'source_id': location['source']['id'],
                                    'landing_page_url': location.get(
                                        'landing_page_url'),
                                    'pdf_url': location.get('pdf_url'),
                                    'is_oa': location.get('is_oa'),
                                    'version': location.get('version'),
                                    'license': location.get('license'),
                                })

                    # best_oa_locations
                    if best_oa_location := (work.get('best_oa_location') or {}):
                        if best_oa_location.get(
                                'source') and best_oa_location.get(
                                'source').get('id'):
                            best_oa_locations_writer.writerow({
                                'work_id': work_id,
                                'source_id': best_oa_location['source']['id'],
                                'landing_page_url': best_oa_location.get(
                                    'landing_page_url'),
                                'pdf_url': best_oa_location.get('pdf_url'),
                                'is_oa': best_oa_location.get('is_oa'),
                                'version': best_oa_location.get('version'),
                                'license': best_oa_location.get('license'),
                            })

                    # authorships
                    if authorships := work.get('authorships'):
                        for authorship in authorships:
                            if author_id := authorship.get('author', {}).get(
                                    'id'):
                                institutions = authorship.get('institutions')
                                institution_ids = [i.get('id') for i in
                                                   institutions]
                                institution_ids = [i for i in institution_ids if
                                                   i]
                                institution_ids = institution_ids or [None]

                                for institution_id in institution_ids:
                                    authorships_writer.writerow({
                                        'work_id': work_id,
                                        'author_position': authorship.get(
                                            'author_position'),
                                        'author_id': author_id,
                                        'institution_id': institution_id,
                                        'raw_affiliation_string': authorship.get(
                                            'raw_affiliation_string'),
                                    })

                    # biblio
                    if biblio := work.get('biblio'):
                        biblio['work_id'] = work_id
                        biblio_writer.writerow(biblio)

                    # topics
                    for topic in work.get('topics', []):
                        if topic_id := topic.get('id'):
                            topics_writer.writerow({
                                'work_id': work_id,
                                'topic_id': topic_id,
                                'score': topic.get('score')
                            })

                    # concepts
                    for concept in work.get('concepts'):
                        if concept_id := concept.get('id'):
                            concepts_writer.writerow({
                                'work_id': work_id,
                                'concept_id': concept_id,
                                'score': concept.get('score'),
                            })

                    # ids
                    if ids := work.get('ids'):
                        ids['work_id'] = work_id
                        ids_writer.writerow(ids)

                    # mesh
                    for mesh in work.get('mesh'):
                        mesh['work_id'] = work_id
                        mesh_writer.writerow(mesh)

                    # open_access
                    if open_access := work.get('open_access'):
                        open_access['work_id'] = work_id
                        open_access_writer.writerow(open_access)

                    # referenced_works
                    for referenced_work in work.get('referenced_works'):
                        if referenced_work:
                            referenced_works_writer.writerow({
                                'work_id': work_id,
                                'referenced_work_id': referenced_work
                            })

                    # related_works
                    for related_work in work.get('related_works'):
                        if related_work:
                            related_works_writer.writerow({
                                'work_id': work_id,
                                'related_work_id': related_work
                            })

            files_done += 1
            if FILES_PER_ENTITY and files_done >= FILES_PER_ENTITY:
                break


def init_dict_writer(csv_file, file_spec, **kwargs):
    writer = csv.DictWriter(
        csv_file, fieldnames=file_spec['columns'], **kwargs
    )
    writer.writeheader()
    return writer


if __name__ == '__main__':
    flatten_topics()
    flatten_authors()
    flatten_concepts()
    flatten_institutions()
    flatten_publishers()
    flatten_sources()
    flatten_works()
