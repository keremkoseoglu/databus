# Processor

A processor can do anything you want to do between a pull and push operation. Filtering data is a typical processor operation.

You can find some demo implementations under databus/processor/demo, or check "[Used by](index.md)" to see real life examples.

## Supplied processors

Currently, Databus provides a ready-to-use processor in databus/processor/email_filter_excel_attachment.py . This is meant to be used with the [E-Mail passenger](passenger.md). It will scan the attachments of the E-Mail, and if it doesn't contain any Excel attachments, the passenger will be marked as "complete" and won't be processed. This is particularly useful if you are expecting E-Mails with Excel attachments.

## Implementing a new processor

To implement a new processor;

- Ensure that the corresponding [passenger](passenger.md) & [puller](puller.md) classes exist. If not, create them first.
- Derive a new class from databus.processor.abstract_processor
- Ensure that your .py file has only one class (which is the processor)
- Ensure calling super().__init__()
- Add the processor class to your [client](client.md) configuration. 
    - [json_db](database.md): /data/json_db/clients/(client name)/config.json
    - [sql_db](database.md): databus.processor