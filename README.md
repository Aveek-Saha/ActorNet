# Actor Net
Generate an ego network for any actor. Uses TMDb to collect information about actors, an edge is formed if an actor has worked with another in a movie or TV show. Edge weights represent how many times an actor has worked with another.

# How to use

### Clone this repo
Clone this repository and make it your current working directory
```
git clone https://github.com/Aveek-Saha/ActorNet.git
cd ActorNet
```

### Install prerequisites
The required libraries for this script are:
1. networkx
1. tqdm
1. urllib

### Create a config file
Create a file named `config.py` and add the following to it:

```python
tmdb_api_key = "<<Your tmdb api key>>" 
actor_name = "<<Name of the actor>>"
```

### Run script

Run the script and wait for it to complete, this may take a while.

```
python actor_net.py
```

### Output

The final output is stored in a gml file: `data/<<name of actor>>.gml`. You can open this in a tool of your choice for analysis. I used Gephi for the image shown in the example.


# Example

Here's an example of a graph generated with this tool. This graph is a small subset of the top 25 actors ranked by TMDb's popularity metric that have worked with Tom Holland. Even from a rudimentary analysis of this graph a few things immediately jump out. The community detection algorithm has done an okay job of splitting the nodes into actors that are primarily connected through the MCU and those either outside the MCU or those with a more diverse set of roles.

![Tom holland example](/example.png)