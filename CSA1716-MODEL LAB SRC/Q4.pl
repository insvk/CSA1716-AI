% Facts: Animal characteristics
has_hair(dog).
has_hair(cow).
has_hair(cat).

gives_milk(dog).
gives_milk(cow).
gives_milk(cat).

warm_blooded(dog).
warm_blooded(cow).
warm_blooded(cat).
warm_blooded(eagle).
warm_blooded(sparrow).

has_feathers(eagle).
has_feathers(sparrow).

lays_eggs(eagle).
lays_eggs(sparrow).
lays_eggs(snake).
lays_eggs(crocodile).

has_scales(snake).
has_scales(crocodile).

cold_blooded(snake).
cold_blooded(crocodile).

lives_in_water(shark).
lives_in_water(salmon).

has_gills(shark).
has_gills(salmon).

has_fins(shark).
has_fins(salmon).

% Rules: Category definitions
mammal(X)  :- has_hair(X), gives_milk(X), warm_blooded(X).
bird(X)    :- has_feathers(X), lays_eggs(X), warm_blooded(X).
reptile(X) :- has_scales(X), cold_blooded(X), lays_eggs(X).
aquatic(X) :- lives_in_water(X), has_gills(X), has_fins(X).

% Classification rule
classify(X, 'Mammal')         :- mammal(X).
classify(X, 'Bird')           :- bird(X).
classify(X, 'Reptile')        :- reptile(X).
classify(X, 'Aquatic Animal') :- aquatic(X).
