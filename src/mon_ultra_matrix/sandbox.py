"""Scout - merged from Autonomous-Tech-Infrastructure-Platform + quantum-ecosystem swarm scout."""
SOURCES = ["github","defillama","coingecko","monad-explorer"]
def scout_topics(topics):
    return [{"topic":t,"sources":SOURCES,"action":"search, rank by stars/activity/TVL, queue for sandbox experiment"} for t in topics]
