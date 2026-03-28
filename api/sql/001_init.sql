CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE people (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    external_key TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    display_name TEXT,
    role_title TEXT,
    seniority TEXT,
    department TEXT,
    bio TEXT,
    github_login TEXT,
    rag_corpus_name TEXT,
    clone_status TEXT NOT NULL DEFAULT 'pending',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    canonical_name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (organization_id, canonical_name)
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (organization_id, slug)
);

CREATE TABLE person_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    level SMALLINT,
    confidence NUMERIC(4,3) NOT NULL,
    evidence_count INTEGER NOT NULL DEFAULT 0,
    last_inferred_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (person_id, skill_id),
    CHECK (confidence >= 0 AND confidence <= 1),
    CHECK (level IS NULL OR level BETWEEN 1 AND 5)
);

CREATE TABLE project_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    importance NUMERIC(4,3) NOT NULL,
    is_must_have BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (project_id, skill_id),
    CHECK (importance >= 0 AND importance <= 1)
);

CREATE TABLE person_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    role TEXT,
    ownership NUMERIC(4,3),
    started_at DATE,
    ended_at DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (ownership IS NULL OR (ownership >= 0 AND ownership <= 1))
);

CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    person_id UUID REFERENCES people(id) ON DELETE SET NULL,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    source_type TEXT NOT NULL,
    title TEXT NOT NULL,
    external_uri TEXT,
    external_id TEXT,
    content_path TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE source_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_summary TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source_id, chunk_index)
);

CREATE TABLE skill_evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    source_chunk_id UUID REFERENCES source_chunks(id) ON DELETE SET NULL,
    evidence_type TEXT NOT NULL,
    quote TEXT,
    rationale TEXT,
    confidence NUMERIC(4,3) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (confidence >= 0 AND confidence <= 1)
);

CREATE TABLE people_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    from_person_id UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    to_person_id UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL,
    strength NUMERIC(4,3),
    confidence NUMERIC(4,3) NOT NULL DEFAULT 1,
    source TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (from_person_id <> to_person_id),
    CHECK (strength IS NULL OR (strength >= 0 AND strength <= 1)),
    CHECK (confidence >= 0 AND confidence <= 1)
);

CREATE TABLE hiring_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    person_id UUID REFERENCES people(id) ON DELETE SET NULL,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    summary TEXT,
    generated_from TEXT NOT NULL DEFAULT 'manual',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE hiring_profile_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hiring_profile_id UUID NOT NULL REFERENCES hiring_profiles(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    requirement_type TEXT NOT NULL,
    weight NUMERIC(4,3) NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (hiring_profile_id, skill_id, requirement_type),
    CHECK (weight >= 0 AND weight <= 1)
);

CREATE INDEX idx_people_org_external_key ON people (organization_id, external_key);
CREATE INDEX idx_skills_org_name ON skills (organization_id, canonical_name);
CREATE INDEX idx_projects_org_slug ON projects (organization_id, slug);
CREATE INDEX idx_person_skills_person_skill ON person_skills (person_id, skill_id);
CREATE INDEX idx_project_skills_project_skill ON project_skills (project_id, skill_id);
CREATE INDEX idx_person_projects_person_project ON person_projects (person_id, project_id);
CREATE INDEX idx_sources_person_id ON sources (person_id);
CREATE INDEX idx_sources_project_id ON sources (project_id);
CREATE INDEX idx_sources_metadata_gin ON sources USING GIN (metadata);
CREATE INDEX idx_source_chunks_source_id ON source_chunks (source_id);
CREATE INDEX idx_skill_evidence_person_skill ON skill_evidence (person_id, skill_id);
CREATE INDEX idx_people_relationships_from ON people_relationships (from_person_id, relationship_type);
CREATE INDEX idx_people_relationships_to ON people_relationships (to_person_id, relationship_type);
CREATE INDEX idx_hiring_profiles_org_id ON hiring_profiles (organization_id);
