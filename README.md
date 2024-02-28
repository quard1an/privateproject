# Swisscom challenge

This is an app for Swisscom challenge.

The idea is that we have a cluster and a client which is sending requests to it.

To build cluster and client, please run following command in the root:
`docker-compose build`

## Cluster
First part of a puzzle.
Cluster is made out of couple nodes which have the same endpoints.
To start the cluster, from root folder run:
`docker-compose up`

### Create group endpoint
Endpoint for the group creation

Type: POST 

URL: "/v1/group" 

Request body: { "groupId": str }
### Delete group endpoint
Endpoint for the group deletion

Type: POST 

URL: "/v1/group" 

Request body: { "groupId": str }

### Get group endpoint
Endpoint to get a group 

Type: GET 

URL: "/v1/group/{groupId}" 


## Client
Client represents a module which is in charge of data manipulation.
Data is stored on the cluster in every node. If user wants to create/delete a group,
client will save/delete it on every node of the cluster automatically.

Client supports two methods: create or delete

When client is started, there's a prompt for user to select which action type 
and for which group Id they want to execute.

While everything is fine with the nodes, client will update all of them. As soon 
as there's a problem in connection, client will perform a secure rollback for the changes.

To run the client, please run following command in the client/ folder:
`python client.py`


## Tests
To run the tests, position yourself to the root folder and run:
`pytest`

Individual tests (for the cluster or for the client) can be run with:
`docker-compose run {app_name} pytest` eg `docker-compose run client_app pytest`


## Kubernetes
Firstly, create docker images with command `docker-compose build`

After that apply kubernetes manifests with command `kubectl apply -f manifests/<<ALL_FILES_FROM_THE_FOLDER>>.yaml`

To run a node, run the following command: `kubectl port-forward <<POD_NAME>> 8000:8000`

And finally to run a client module, run the following command : `kubectl run client-app --rm -i --tty --image=client_app --image-pull-policy=Never -- python client/client.py`