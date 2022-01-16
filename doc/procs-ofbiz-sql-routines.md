# procs-ofbiz-sql-routines.md
```sql
select party.party_id,last_name,role_type_id from party 
    left join person on party.party_id=person.party_id 
    left join party_role on party.party_id=party_role.party_id;
```

