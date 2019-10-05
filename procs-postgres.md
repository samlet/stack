# procs-postgres.md
⊕ [library/postgres - Docker Hub](https://hub.docker.com/_/postgres/)

+ 查看数据库表

```sh
$ psql -l  # 列出已有数据库
$ psql demo
demo=# \d test1_test1
demo-# \q
```
```sh
$ psql odoo -h localhost -U odoo
# password: odoo
```

## issue: macos error
⊕ [PostgreSQL not running on Mac - Database Administrators Stack Exchange](https://dba.stackexchange.com/questions/75214/postgresql-not-running-on-mac)
    I was getting the same. Is the server running locally and accepting connections on Unix domain socket "/tmp/.s.PGSQL.5432"? 
    loop of Homebrew install / start / stop / restart to no avail...
    Finally, brew postgresql-upgrade-database worked.
    Seems I was on 9.6 instead of 10.4, and something my latest App Store restart restarted all my database servers...

```sh
$ brew postgresql-upgrade-database
$ brew services start postgresql
$ psql -l
```

