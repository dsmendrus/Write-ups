# SQL Injection
here i will be showing egzamples of sql injection, what is it, how to use, and how to defend agaisnt this

so first of all, sqli injection is a special values that we can type in input areas. We use SQL languege to comunicate wit datavases, and if that input goes straight to a database we can explore and cause some damage

# Example
if we have input areas login and password and then it is proggramed to compare our input to some form database Input = login & input = password we can manipulate "" and do something like ' OR 1 = 1; 
``` SQL
`OR 1=1; DROP TABLE Dane
```