# ActorNet
Generate an ego network for any actor. Uses TMDb to collect information about actors, an edge is formed if an actor has worked with another in a movie or TV show. Edge weights represent how many times an actor has worked with another.

## Example

Here's an example of a graph generated with this tool. This graph is a small subset of the top 25 actors ranked by TMDb's popularity metric that have worked with Tom Holland. Even from a rudimentary analysis of this graph a few things immediately jump out. The community detection algorithm has done an okay job of splitting the nodes into actors that are primarily connected through the MCU and those either outside the MCU or those with a more diverse set of roles.

![Tom holland example](/example.png)