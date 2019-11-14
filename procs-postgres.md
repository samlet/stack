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

## linux
⊕ [How To Install and Use PostgreSQL on Ubuntu 18.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

```sh
sudo apt install postgresql postgresql-contrib
# Accessing a Postgres Prompt Without Switching Accounts
sudo -u postgres psql
\l
\q
```
```sh
sudo -i -u postgres
psql
\q

# If you are logged in as the postgres account, you can create a new user by typing:
createuser --interactive
# If, instead, you prefer to use sudo for each command without switching from your normal account, type:
sudo -u postgres createuser --interactive

# Output
Enter name of role to add: sammy
Shall the new role be a superuser? (y/n) y

# Creating a New Database
sudo -u postgres createdb sammy
```


