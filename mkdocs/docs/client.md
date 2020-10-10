# Client

Defines a client company using Databus. Each client can has its own reader / processor / pusher classes. A singular Databus instance can support multiple clients. 

## Client

To add a new client (called abc);

- **json_db**: Create the client folder structure under /data/clients/ as described in [database](database.md) section.
- **sql_db**: Fill the SQL Server tables just like the 'demo' client

If a client doesn't have any users defined, this means that the authentication is not active. The web interface will allow any login for that client.

## User

You may define two user roles, which will affect their capabilities in the web interface.

- **operator**: The standard user, able to browse through files, but unable to configure anything.
- **administrator**: The power user, able to configure as well.

There is also a special God-Mode user. Client: root, user: root. This user can perform actions that no other user can, such as shutting down the system. Check the [web section](web.md) for more details. 

## Client Passenger

Describes a particular [passenger](passenger.md) definition of a client. Each client can contain multiple passengers; as long as they are defined in the [database](database.md) properly.