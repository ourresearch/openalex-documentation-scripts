--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-2.heroku1+1)
-- Dumped by pg_dump version 14.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: openalex; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA openalex;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: authors; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.authors (
    id text NOT NULL,
    orcid text,
    display_name text,
    display_name_alternatives json,
    works_count integer,
    cited_by_count integer,
    last_known_institution text,
    works_api_url text,
    updated_date timestamp without time zone
);


--
-- Name: authors_counts_by_year; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.authors_counts_by_year (
    author_id text NOT NULL,
    year integer NOT NULL,
    works_count integer,
    cited_by_count integer,
    oa_works_count integer
);


--
-- Name: authors_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.authors_ids (
    author_id text NOT NULL,
    openalex text,
    orcid text,
    scopus text,
    twitter text,
    wikipedia text,
    mag bigint
);


--
-- Name: concepts; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.concepts (
    id text NOT NULL,
    wikidata text,
    display_name text,
    level integer,
    description text,
    works_count integer,
    cited_by_count integer,
    image_url text,
    image_thumbnail_url text,
    works_api_url text,
    updated_date timestamp without time zone
);


--
-- Name: concepts_ancestors; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.concepts_ancestors (
    concept_id text,
    ancestor_id text
);


--
-- Name: concepts_counts_by_year; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.concepts_counts_by_year (
    concept_id text NOT NULL,
    year integer NOT NULL,
    works_count integer,
    cited_by_count integer,
    oa_works_count integer
);


--
-- Name: concepts_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.concepts_ids (
    concept_id text NOT NULL,
    openalex text,
    wikidata text,
    wikipedia text,
    umls_aui json,
    umls_cui json,
    mag bigint
);


--
-- Name: concepts_related_concepts; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.concepts_related_concepts (
    concept_id text,
    related_concept_id text,
    score real
);


--
-- Name: institutions; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.institutions (
    id text NOT NULL,
    ror text,
    display_name text,
    country_code text,
    type text,
    homepage_url text,
    image_url text,
    image_thumbnail_url text,
    display_name_acroynyms json,
    display_name_alternatives json,
    works_count integer,
    cited_by_count integer,
    works_api_url text,
    updated_date timestamp without time zone
);


--
-- Name: institutions_associated_institutions; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.institutions_associated_institutions (
    institution_id text,
    associated_institution_id text,
    relationship text
);


--
-- Name: institutions_counts_by_year; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.institutions_counts_by_year (
    institution_id text NOT NULL,
    year integer NOT NULL,
    works_count integer,
    cited_by_count integer,
    oa_works_count integer
);


--
-- Name: institutions_geo; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.institutions_geo (
    institution_id text NOT NULL,
    city text,
    geonames_city_id text,
    region text,
    country_code text,
    country text,
    latitude real,
    longitude real
);


--
-- Name: institutions_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.institutions_ids (
    institution_id text NOT NULL,
    openalex text,
    ror text,
    grid text,
    wikipedia text,
    wikidata text,
    mag bigint
);


--
-- Name: publishers; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.publishers (
    id text NOT NULL,
    display_name text,
    alternate_titles json,
    country_codes json,
    hierarchy_level integer,
    parent_publisher text,
    works_count integer,
    cited_by_count integer,
    sources_api_url text,
    updated_date timestamp without time zone
);


--
-- Name: publishers_counts_by_year; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.publishers_counts_by_year (
    publisher_id text NOT NULL,
    year integer NOT NULL,
    works_count integer,
    cited_by_count integer,
    oa_works_count integer
);


--
-- Name: publishers_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.publishers_ids (
    publisher_id text,
    openalex text,
    ror text,
    wikidata text
);


--
-- Name: sources; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.sources (
    id text NOT NULL,
    issn_l text,
    issn json,
    display_name text,
    publisher text,
    works_count integer,
    cited_by_count integer,
    is_oa boolean,
    is_in_doaj boolean,
    homepage_url text,
    works_api_url text,
    updated_date timestamp without time zone
);


--
-- Name: sources_counts_by_year; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.sources_counts_by_year (
    source_id text NOT NULL,
    year integer NOT NULL,
    works_count integer,
    cited_by_count integer,
    oa_works_count integer
);


--
-- Name: sources_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.sources_ids (
    source_id text,
    openalex text,
    issn_l text,
    issn json,
    mag bigint,
    wikidata text,
    fatcat text
);


--
-- Name: works; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works (
    id text NOT NULL,
    doi text,
    title text,
    display_name text,
    publication_year integer,
    publication_date text,
    type text,
    cited_by_count integer,
    is_retracted boolean,
    is_paratext boolean,
    cited_by_api_url text,
    abstract_inverted_index json
);

--
-- Name: works_primary_locations; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_primary_locations (
    work_id text,
    source_id text,
    landing_page_url text,
    pdf_url text,
    is_oa boolean,
    version text,
    license text
);


--
-- Name: works_locations; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_locations (
    work_id text,
    source_id text,
    landing_page_url text,
    pdf_url text,
    is_oa boolean,
    version text,
    license text
);


--
-- Name: works_best_oa_locations; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_best_oa_locations (
    work_id text,
    source_id text,
    landing_page_url text,
    pdf_url text,
    is_oa boolean,
    version text,
    license text
);


--
-- Name: works_authorships; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_authorships (
    work_id text,
    author_position text,
    author_id text,
    institution_id text,
    raw_affiliation_string text
);


--
-- Name: works_biblio; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_biblio (
    work_id text NOT NULL,
    volume text,
    issue text,
    first_page text,
    last_page text
);


--
-- Name: works_concepts; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_concepts (
    work_id text,
    concept_id text,
    score real
);


--
-- Name: works_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_ids (
    work_id text NOT NULL,
    openalex text,
    doi text,
    mag bigint,
    pmid text,
    pmcid text
);


--
-- Name: works_mesh; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_mesh (
    work_id text,
    descriptor_ui text,
    descriptor_name text,
    qualifier_ui text,
    qualifier_name text,
    is_major_topic boolean
);


--
-- Name: works_open_access; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_open_access (
    work_id text NOT NULL,
    is_oa boolean,
    oa_status text,
    oa_url text,
    any_repository_has_fulltext boolean
);


--
-- Name: works_referenced_works; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_referenced_works (
    work_id text,
    referenced_work_id text
);


--
-- Name: works_related_works; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex.works_related_works (
    work_id text,
    related_work_id text
);


----
---- Name: authors_counts_by_year authors_counts_by_year_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.authors_counts_by_year
--    ADD CONSTRAINT authors_counts_by_year_pkey PRIMARY KEY (author_id, year);
--
--
----
---- Name: authors_ids authors_ids_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.authors_ids
--    ADD CONSTRAINT authors_ids_pkey PRIMARY KEY (author_id);
--
--
----
---- Name: authors authors_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.authors
--    ADD CONSTRAINT authors_pkey PRIMARY KEY (id);
--
--
----
---- Name: concepts_counts_by_year concepts_counts_by_year_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.concepts_counts_by_year
--    ADD CONSTRAINT concepts_counts_by_year_pkey PRIMARY KEY (concept_id, year);
--
--
----
---- Name: concepts_ids concepts_ids_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.concepts_ids
--    ADD CONSTRAINT concepts_ids_pkey PRIMARY KEY (concept_id);
--
--
----
---- Name: concepts concepts_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.concepts
--    ADD CONSTRAINT concepts_pkey PRIMARY KEY (id);
--
--
----
---- Name: institutions_counts_by_year institutions_counts_by_year_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.institutions_counts_by_year
--    ADD CONSTRAINT institutions_counts_by_year_pkey PRIMARY KEY (institution_id, year);
--
--
----
---- Name: institutions_geo institutions_geo_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.institutions_geo
--    ADD CONSTRAINT institutions_geo_pkey PRIMARY KEY (institution_id);
--
--
----
---- Name: institutions_ids institutions_ids_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.institutions_ids
--    ADD CONSTRAINT institutions_ids_pkey PRIMARY KEY (institution_id);
--
--
----
---- Name: institutions institutions_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.institutions
--    ADD CONSTRAINT institutions_pkey PRIMARY KEY (id);
--
--
----
---- Name: sources source_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.sources
--    ADD CONSTRAINT source_pkey PRIMARY KEY (id);
--
--
----
---- Name: sources_counts_by_year sources_counts_by_year_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.sources_counts_by_year
--    ADD CONSTRAINT sources_counts_by_year_pkey PRIMARY KEY (source_id, year);
--
--
----
---- Name: works_biblio works_biblio_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.works_biblio
--    ADD CONSTRAINT works_biblio_pkey PRIMARY KEY (work_id);
--
--
----
---- Name: works_ids works_ids_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.works_ids
--    ADD CONSTRAINT works_ids_pkey PRIMARY KEY (work_id);
--
--
----
---- Name: works_open_access works_open_access_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.works_open_access
--    ADD CONSTRAINT works_open_access_pkey PRIMARY KEY (work_id);
--
--
----
---- Name: works works_pkey; Type: CONSTRAINT; Schema: openalex; Owner: -
----
--
--ALTER TABLE ONLY openalex.works
--    ADD CONSTRAINT works_pkey PRIMARY KEY (id);
--

--
-- Name: concepts_ancestors_concept_id_idx; Type: INDEX; Schema: openalex; Owner: -
--

CREATE INDEX concepts_ancestors_concept_id_idx ON openalex.concepts_ancestors USING btree (concept_id);


--
-- Name: concepts_related_concepts_concept_id_idx; Type: INDEX; Schema: openalex; Owner: -
--

CREATE INDEX concepts_related_concepts_concept_id_idx ON openalex.concepts_related_concepts USING btree (concept_id);


--
-- Name: concepts_related_concepts_related_concept_id_idx; Type: INDEX; Schema: openalex; Owner: -
--

CREATE INDEX concepts_related_concepts_related_concept_id_idx ON openalex.concepts_related_concepts USING btree (related_concept_id);

--
-- Name: works_primary_locations_work_id_idx; Type: INDEX; Schema: openalex; Owner: -
--

CREATE INDEX works_primary_locations_work_id_idx ON openalex.works_primary_locations USING btree (work_id);


--
-- Name: works_locations_work_id_idx; Type: INDEX; Schema: openalex; Owner: -
--

CREATE INDEX works_locations_work_id_idx ON openalex.works_locations USING btree (work_id);


--
-- Name: works_best_oa_locations_work_id_idx; Type: INDEX; Schema: openalex; Owner: -
--

CREATE INDEX works_best_oa_locations_work_id_idx ON openalex.works_best_oa_locations USING btree (work_id);


--
-- PostgreSQL database dump complete
--
