# procs-generator.md
# start
```sh
$ DATABASE="bank"
$ cockroach sql --execute="CREATE DATABASE $DATABASE;
GRANT ALL ON DATABASE $DATABASE TO maxroach;" --insecure
$ cockroach sql --execute="SHOW DATABASES;" --insecure
# $ cockroach sql --execute="DROP DATABASE $DATABASE;" --insecure

$ ./module_generator.py regen-models model_planet.yaml
```

## pycharm (fail)
with url: cockroachdb://maxroach@localhost:26257/planet
    database: planet
    user: maxroach
    port: 26257

- issue: 
    Error encountered when performing Introspect database planet: ERROR: column "xmin" does not exist.

    
