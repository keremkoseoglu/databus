# Puller

Puller classes are defined to fetch passengers from source systems. For each source system, you may implement your own puller class. Databus has a built-in abstract Exchange puller; which you can implement for your own purposes. 

You can find some demo implementations under databus/puller/demo, or check "[Used by](index.md)" to see real life examples.

## Supplied pullers

### Exchange Server

Databus provides an abstract puller class for Exhange Server under databus/puller/abstract_exchange.py. If you need to get E-Mails from an Exchange Server, you can implement your concrete class and start using it right away. Exchange Server will return passengers of type [E-Mail](passenger.md).

A sample implementation can be found in [Measy](https://keremkoseoglu.github.io/measy/).

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