# common-Restaurant.md
## request restaurant
* default "sorry, I didn't understand you, please try input something else"
* submit "done!"
@ form restaurant

```yaml
fields:
  cuisine:
    text: "what cuisine?"
  num_people:
    text: "how many people?"
    type: number
  outdoor_seating:
    text: "do you want to seat outside?"
    type: boolean
  preferences:
    text: "please provide additional preferences"
  feedback:
    text: "please give your feedback"
```

im looking for a restaurant
can i get [cuisine:o](swedish) food in any area
a restaurant that serves [cuisine:o](caribbean) food
id like a restaurant
im looking for a restaurant that serves [cuisine:o](mediterranean) food
can i find a restaurant that serves [cuisine:o](chinese)
i need to find a restaurant
uh im looking for a restaurant that serves [cuisine:o](kosher) food
uh can i find a restaurant and it should serve [cuisine:o](brazilian) food
im looking for a restaurant serving [cuisine:o](italian) food
restaurant please
i'd like to book a table for [num_people:n](two) with [cuisine:o](brazilian) cuisine
i need a table for [num_people:n](4)

## affirm restaurant
yeah a cheap restaurant serving international food

## inform
- wrong_cuisine "cuisine type is not in the database, please try again"
- wrong_num_people "number of people should be a positive integer, please try again"
- wrong_outdoor_seating "could not convert input to boolean value, please try again"

[cuisine:o](afghan) food
how bout [cuisine:o](asian oriental)
what about [cuisine:o](indian) food
uh how about [cuisine:o](turkish) type of food
um [cuisine:o](english)
im looking for [cuisine:o](tuscan) food
id like [cuisine:o](moroccan) food
[cuisine:o](seafood)
[cuisine:o](french) food
serves [cuisine:o](british) food
id like [cuisine:o](canapes)
serving [cuisine:o](jamaican) food
um what about [cuisine:o](italian) food
im looking for [cuisine:o](corsica) food
im looking for [cuisine:o](world) food
 serves [cuisine:o](french) food
how about [cuisine:o](indian) food
can i get [cuisine:o](chinese) food
[cuisine:o](irish) food
[cuisine:o](english) food
[cuisine:o](spanish) food
how bout one that serves [cuisine:o](portuguese) food and is cheap
[cuisine:o](german)
[cuisine:o](korean) food
im looking for [cuisine:o](romanian) food
 serves [cuisine:o](canapes) food
[cuisine:o](gastropub)
i want [cuisine:o](french) food
how about [cuisine:o](modern european) type of food
it should serve [cuisine:o](scandinavian) food
how [cuisine:o](european)
how about [cuisine:o](european) food
serves [cuisine:o](traditional) food
[cuisine:o](indonesian) food
[cuisine:o](modern european)
serves [cuisine:o](brazilian)
i would like [cuisine:o](modern european) food
looking for [cuisine:o](lebanese) food
[cuisine:o](portuguese)
[cuisine:o](european)
i want [cuisine:o](polish) food
id like [cuisine:o](thai)
i want to find [cuisine:o](moroccan) food
[cuisine:o](afghan)
[cuisine:o](scottish) food
how about [cuisine:o](vietnamese)
hi im looking for [cuisine:o](mexican) food
how about [cuisine:o](indian) type of food
[cuisine:o](polynesian) food
[cuisine:o](mexican)
instead could it be for [num_people:n](four) people
any [cuisine:o](japanese) food
what about [cuisine:o](thai) food
how about [cuisine:o](asian oriental) food
im looking for [cuisine:o](japanese) food
im looking for [cuisine:o](belgian) food
im looking for [cuisine:o](turkish) food
serving [cuisine:o](corsica) food
serving [cuisine:gastropub:o](gastro pub)
is there [cuisine:o](british) food
[cuisine:o](world) food
im looking for something serves [cuisine:o](japanese) food
id like a [cuisine:o](greek)
im looking for [cuisine:o](malaysian) food
i want to find [cuisine:o](world) food
serves [cuisine:asian:o](pan asian) food
looking for [cuisine:o](afghan) food
that serves [cuisine:o](portuguese) food
[cuisine:asian:o](asian oriental) food
[cuisine:o](russian) food
[cuisine:o](corsica)
[cuisine:asian:o](asian oriental)
serving [cuisine:o](basque) food
how about [cuisine:o](italian)
looking for [cuisine:o](spanish) food in the center of town
it should serve [cuisine:o](gastropub) food
[cuisine:o](welsh) food
i want [cuisine:o](vegetarian) food
im looking for [cuisine:o](swedish) food
um how about [cuisine:o](chinese) food
[cuisine:o](world) food
can i have a [cuisine:o](seafood) please
how about [cuisine:o](italian) food
how about [cuisine:o](korean)
[cuisine:o](corsica) food
[cuisine:o](scandinavian)
[cuisine:o](vegetarian) food
what about [cuisine:o](italian)
how about [cuisine:o](portuguese) food
serving [cuisine:o](french) food
[cuisine:o](tuscan) food
how about uh [cuisine:o](gastropub)
im looking for [cuisine:o](creative) food
im looking for [cuisine:o](malaysian) food
im looking for [cuisine:o](unusual) food
[cuisine:o](danish) food
how about [cuisine:o](spanish) food
im looking for [cuisine:o](vietnamese) food
[cuisine:o](spanish)
a restaurant serving [cuisine:o](romanian) food
im looking for [cuisine:o](lebanese) food
[cuisine:o](italian) food
a restaurant with [cuisine:o](afghan) food
im looking for [cuisine:o](traditional) food
uh i want [cuisine:o](cantonese) food
im looking for [cuisine:o](thai)
i want to seat [seating:o](outside)
i want to seat [seating:o](inside)
i want to seat [seating:o](outdoor)
i want to seat [seating:o](indoor)
let's go [seating:o](inside)
[seating:o](inside)
[seating:o](outdoor)
my feedback is [feedback:o](good)
my feedback is [feedback:o](great)
it was [feedback:o](terrible)
i consider it [feedback:o](success)
you are [feedback:o](awful)


