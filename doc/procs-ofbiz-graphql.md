# procs-ofbiz-graphql.md
## start
⊕ [graphile/postgraphile: Execute one command (or mount one Node.js middleware) and get an instant high-performance GraphQL API for your PostgreSQL database!](https://github.com/graphile/postgraphile)

```sh
npm install -g postgraphile

# 需要修改communication_event
psql ofbiz
ofbiz=# ALTER TABLE communication_event drop column to_string;

npx postgraphile -c ofbiz --watch
open http://localhost:5000/graphiql
```
```js
{allUserLogins{
  nodes{
    userLoginId
  }
}}
```

## manual
⊕ [PostGraphile | Example queries and mutations](https://www.graphile.org/postgraphile/examples/#Mutations__Create)

⊕ [PostGraphile | Relations](https://www.graphile.org/postgraphile/relations/)

+ Example database schema for one-to-many relation

```sql
create schema a;
create schema c;

create table c.person (
  id serial primary key,
  name varchar not null,
  about text,
  email varchar not null unique,
  created_at timestamp default current_timestamp
);

create table a.post (
  id serial primary key,
  headline text not null,
  body text,
  -- `references` 👇  sets up the foreign key relation
  author_id int4 references c.person(id)
);
create index on a.post (author_id);
```

+ Example query against the above schema

```js
{
  allPosts {
    nodes {
      headline
      body

      # this relation is automatically exposed
      personByAuthorId {
        id
        name
        about
      }
    }
  }
}
```

⊕ [PostGraphile | Views](https://www.graphile.org/postgraphile/views/)

+ Views enable you to expose a simple "flattened" object built from multiple tables.

```sql
CREATE TABLE app_public.person (
  id serial PRIMARY KEY
);

CREATE TABLE app_public.address (
  person_id int PRIMARY KEY REFERENCES app_public.person,
  country text,
  street text,
);

CREATE VIEW person_view AS
  SELECT person.id, address.country, address.street
  FROM app_public.person person
  INNER JOIN app_public.address
  ON person.id = address.person_id;
```

The GraphQL query using this view is flatter than the query using the underlying tables:

```js
query Before {
  person {
    id
    address {
      country
      street
    }
  }
}

query After {
  personView {
    id
    country
    street
  }
}
```

## cli
⊕ [PostGraphile | Command Line Interface](https://www.graphile.org/postgraphile/usage-cli/)
    --export-schema-graphql <path>
        enables exporting the detected schema, in GraphQL schema format, to the given location. The directories must exist already, if the file exists it will be overwritten.


