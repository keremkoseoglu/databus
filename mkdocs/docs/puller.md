# Puller

Puller classes are defined to fetch passengers from source systems. For each source system, you may implement your own puller class. Databus has a built-in abstract Exchange puller; which you can implement for your own purposes. 

You can find some demo implementations under databus/puller/demo, or check "[Used by](index.md)" to see real life examples.

## Supplied pullers

### Exchange Server

Databus provides an abstract puller class for Exhange Server under databus/puller/abstract_exchange.py. If you need to get E-Mails from an Exchange Server, you can implement your concrete class and start using it right away. Exchange Server will return passengers of type [E-Mail](passenger.md).

You basically need to fill two points here:

- **settings**: Return your Exchange credentials and settings
- **notify_passengers_seated**: The action to take when a passenger is seated. Typically, you would want to call one of the ...seated_passengers... methods from here.

A sample implementation can be found in [Measy](https://keremkoseoglu.github.io/measy/).

Sample config JSON for on-premise Exchange server:
```
"exchange": {
    "server": "mail.your_server.com",
    "username": "your_username",
    "password": "your_password",
    "email": "your_username@your_domain.com",
    "product_owners": [],
    "disable_ssl_validation": true
}
```

Sample config JSON for Office 365:
```
"exchange": {
    "server": "outlook.office365.com",
    "username": "your_username@your_domain.com",
    "password": "your_password",
    "email": "your_username@your_domain.com",
    "product_owners": [],
    "disable_ssl_validation": false
}
```

### Multi Exchange Server

If you need to check multiple Exchange accounts for a particular type of E-Mail, you'll be pleased to know that Databus provides an abstract puller just for that! Checkdatabus/puller/abstract_multi_exchange.py. Create your own concrete class, fill the abstract methods and you are good to go!

Obviously, it uses Exchange Server puller (explained above) behind the scenes.

A sample implementation can be found in [Measy](https://keremkoseoglu.github.io/measy/).

## Implementing a new puller

To implement a new puller;

- Ensure that the corresponding passenger class exists. If not, create your passenger class first.
- Derive a new class from databus.puller.abstract_puller
- Ensure that your .py file has only one class (which is the puller)
- Ensure calling super().__init__()
- Add the puller class to your client configuration. 
    - [json_db](database.md): /data/json_db/clients/(client name)/config.json
    - [sql_db](database.md): databus.puller