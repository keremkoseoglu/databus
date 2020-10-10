# Web

Databus has a built-in Flask website, which shows log and queue data. Whenever the dispatcher is started, the web server is activated too. The Web interface is hosted on [Waitress](https://pypi.org/project/waitress/). Web related files are stored in databus/web. It uses [BootStrap](https://getbootstrap.com/), [JQuery](https://jquery.com/) and some minor open source JavaScript libraries.

## Configuration

If you don't do any configuration, the Web interface will start as soon as Databus is started. It runs on [http://localhost:5000](http://localhost:5000) by default. However, you can change the port or disable the Web interface on your [dispatcher ticket](dispatcher.md).

## Logging in

When you access the site for the first time, you are asked for three parameters to log in. 

![Login](img/web_login.png?raw=true "Login")

- [Client](client.md): Name of the client you want to manage. This can be any client defined in the [database](database.md), or "root" if you'll do something more adventureous.
- Username: Obvious.
- Password: Obvious.

The web contents will change depending on the [role of the user](client.md). If you log in using a client account, you can only manage that particular client. If you log in with the **root** account, you can manage all clients and take extra actions; such as shutting down Databus.

If you just installed Databus, you can use one of the supplied accounts.

- demo - demo - demo
- root - root - root

## Passengers

This section will list the passengers defined in the [database](database.md). 

![Passengers](img/web_pass.png?raw=true "Passengers")

If you click "Expedite" for a passenger, the [dispatcher](dispatcher.md) will sync that passenger within a minute - instead of waiting for its next schedule.

## Peek

This section can be used to peek into the [source systems](puller.md) to see what is waiting to be pulled. For example, if your app is pulling E-Mails from Exchange, this section will peek into the inbox and show what's there.

![Peek](img/web_peek.png?raw=true "Peek")

## Queue

This section will show the [passengers](passenger.md) in the [queue](queue.md) along their statuses.

![Queue](img/web_queue.png?raw=true "Queue")

If you click "Purge", the completed [passengers](passenger.md) will be removed from the queue. According to your [database configuration](database.md), Databus automatically purges old queue entries anwyay - but this button is useful if you need to purge manually.

If you click on a [passenger](passenger.md), you can see its details.

![Queue](img/web_queue_disp.png?raw=true "Queue display")

- You can click any status to change it. For example, clicking on a "Complete" status will change it to "Incomplete"; forcing the [driver](driver.md) to re-process it. Or; clicking on an "Incomplete" status will change it to "Complete" so that the [driver](driver.md) won't process it further.

- Attachments can be viewed & downloaded directly.

- Log files related to that particular [passenger](passenger.md) can be viewed from here directly.

## Log

Generated log files can be viewed here. Good for hunting down errors.

![Log](img/web_log.png?raw=true "Log")

If you click "Purge", all log files will be removed. According to your [database configuration](database.md), Databus automatically purges old log files anwyay - but this button is useful if you need to purge manually.

If you click on a log file, you can see its contents.

![Log](img/web_log_disp.png?raw=true "Log display")

## Users

This section will list the users defined in the [database](database.md). 

![User](img/web_user.png?raw=true "User")

If you click "Revoke token", Databus will no longer remember this user and he/she will need to re-authenticate.

## Customizing

This is the section where you can alter system parameters. 

![Customizing](img/web_cust.png?raw=true "Customizing")

You will see two kinds of nodes here.

- Nodes starting with __ are files of the Databus standard. 
- Nodes with regular names are additional files provided in the [dispatcher ticket](dispatcher.md)

Typically, each file here is expected to be in JSON format.

Some __ nodes can only be accessed with the root user.

## Export

If you want to backup your data or migrate to another [database](database.md), this is your section.

![Export](img/web_export.png?raw=true "Export")

Depending on the database you have selected, Databus will ask for additional parameters.

The export operation can be executed in two modes:

- Async: In the background. Good for large volumes of data.
- Sync: In the foreground, real time. Good for small volumes of data.

## About

Provides a good amount of system information.

![About](img/web_about.png?raw=true "About")

## Logout

The 👋 emoji on top can be used to logout of Databus.

## Shutdown

The 🔴 emoji on top can be used to shutdown Databus. The system will finish active [drivers](driver.md) first, then shutdown safely. If you shutdown in any other way, you may cause unwanted data inconsistencies. Note that shutting the system down is only available to the [root user](client.md).
