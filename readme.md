# Simulates NCAA tournament 2016.

Provided with a json file containing team seedings, simulates the
result of the NCAA tournament.  Winners are determined probabilistically
by the seedings.

For example, if two teams (a,b) play, the chance that team_a loses is
the seeding of team_a divided by the seeding of team_a + team_b.

With concrete numbers, the chance that a 1 seed loses to a 16 seed is
1/17 or approximately 5.9%.  The chance that a 10 seed loses to a 2 seed
is 10/12 or approximately 83%.
