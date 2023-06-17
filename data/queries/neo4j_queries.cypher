# Query to create virtual network and port nodes
CREATE (vn:VirtualNetwork {name: $virtualNetworkName})
CREATE (vm:VirtualMachine {name: $virtualMachineName})
CREATE (port:Port {number: $portNumber})

# Query to establish relationships between virtual network, virtual machine, and port
MERGE (vn)-[:CONTAINS]->(vm)
MERGE (vm)-[:CONNECTED_TO]->(port)

# Query to create identity node with last accessed property
CREATE (id:Identity {name: $identityName, lastAccessed: $lastAccessed})

# Query to establish relationship between virtual machine and identity
MERGE (vm)-[:IDENTIFIED_BY]->(id)
