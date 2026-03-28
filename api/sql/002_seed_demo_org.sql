INSERT INTO organizations (name, slug)
VALUES ('Gemellus Demo Org', 'gemellus-demo-org')
ON CONFLICT (slug) DO NOTHING;
