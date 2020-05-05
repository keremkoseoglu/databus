
Commands to create the database from the scratch:
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[client](
    [client_id] [varchar](10) NOT NULL,
    [log_life_span] [int] NOT NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[client] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[log_head](
    [client_id] [varchar](10) NOT NULL,
    [log_id] [varchar](50) NOT NULL,
    [created_on] [datetime] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[log_head] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [log_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[log_head] ADD  DEFAULT (getdate()) FOR [created_on]
GO
ALTER TABLE [databus].[log_head]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[log_item](
    [client_id] [varchar](10) NOT NULL,
    [log_id] [varchar](50) NOT NULL,
    [item_no] [int] NOT NULL,
    [module] [varchar](50) NULL,
    [message_type] [varchar](1) NULL,
    [message] [nvarchar](max) NULL,
    [message_on] [datetime] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[log_item] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [log_id] ASC,
    [item_no] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[log_item]  WITH CHECK ADD FOREIGN KEY([client_id], [log_id])
REFERENCES [databus].[log_head] ([client_id], [log_id])
GO
ALTER TABLE [databus].[log_item]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[passenger](
    [client_id] [varchar](10) NOT NULL,
    [passenger_id] [varchar](10) NOT NULL,
    [passenger_module] [varchar](50) NOT NULL,
    [queue_module] [varchar](50) NOT NULL,
    [sync_frequency] [int] NOT NULL,
    [queue_life_span] [int] NOT NULL,
    [exe_order] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[passenger] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [passenger_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[passenger]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[processor](
    [client_id] [varchar](10) NOT NULL,
    [passenger_id] [varchar](10) NOT NULL,
    [processor_module] [varchar](50) NOT NULL,
    [exe_order] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[processor] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [passenger_id] ASC,
    [processor_module] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[processor]  WITH CHECK ADD FOREIGN KEY([client_id], [passenger_id])
REFERENCES [databus].[passenger] ([client_id], [passenger_id])
GO
ALTER TABLE [databus].[processor]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[puller](
    [client_id] [varchar](10) NOT NULL,
    [passenger_id] [varchar](10) NOT NULL,
    [puller_module] [varchar](50) NOT NULL,
    [exe_order] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[puller] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [passenger_id] ASC,
    [puller_module] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[puller]  WITH CHECK ADD FOREIGN KEY([client_id], [passenger_id])
REFERENCES [databus].[passenger] ([client_id], [passenger_id])
GO
ALTER TABLE [databus].[puller]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[pusher](
    [client_id] [varchar](10) NOT NULL,
    [passenger_id] [varchar](10) NOT NULL,
    [pusher_module] [varchar](50) NOT NULL,
    [exe_order] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[pusher] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [passenger_id] ASC,
    [pusher_module] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[pusher]  WITH CHECK ADD FOREIGN KEY([client_id], [passenger_id])
REFERENCES [databus].[passenger] ([client_id], [passenger_id])
GO
ALTER TABLE [databus].[pusher]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[queue](
    [client_id] [varchar](10) NOT NULL,
    [queue_id] [varchar](50) NOT NULL,
    [external_id] [nvarchar](100) NULL,
    [source_system] [nvarchar](50) NULL,
    [passenger_module] [varchar](50) NULL,
    [puller_module] [varchar](50) NULL,
    [puller_notified] [bit] NULL,
    [pulled_on] [datetime] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[queue] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [queue_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[queue] ADD  DEFAULT ((0)) FOR [puller_notified]
GO
ALTER TABLE [databus].[queue] ADD  DEFAULT (getdate()) FOR [pulled_on]
GO
ALTER TABLE [databus].[queue]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[queue_attachment](
    [client_id] [varchar](10) NOT NULL,
    [queue_id] [varchar](50) NOT NULL,
    [attachment_id] [nvarchar](100) NOT NULL,
    [txt_content] [nvarchar](max) NULL,
    [bin_content] [varbinary](max) NULL,
    [file_format] [varchar](1) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[queue_attachment] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [queue_id] ASC,
    [attachment_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[queue_attachment]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO
ALTER TABLE [databus].[queue_attachment]  WITH CHECK ADD FOREIGN KEY([client_id], [queue_id])
REFERENCES [databus].[queue] ([client_id], [queue_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[queue_processor](
    [client_id] [varchar](10) NOT NULL,
    [queue_id] [varchar](50) NOT NULL,
    [processor_module] [varchar](50) NOT NULL,
    [status] [varchar](1) NULL,
    [exe_order] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[queue_processor] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [queue_id] ASC,
    [processor_module] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[queue_processor]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO
ALTER TABLE [databus].[queue_processor]  WITH CHECK ADD FOREIGN KEY([client_id], [queue_id])
REFERENCES [databus].[queue] ([client_id], [queue_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[queue_pusher](
    [client_id] [varchar](10) NOT NULL,
    [queue_id] [varchar](50) NOT NULL,
    [pusher_module] [varchar](50) NOT NULL,
    [status] [varchar](1) NULL,
    [exe_order] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[queue_pusher] ADD PRIMARY KEY CLUSTERED 
(
    [client_id] ASC,
    [queue_id] ASC,
    [pusher_module] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[queue_pusher]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO
ALTER TABLE [databus].[queue_pusher]  WITH CHECK ADD FOREIGN KEY([client_id], [queue_id])
REFERENCES [databus].[queue] ([client_id], [queue_id])
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [databus].[insert_queue_attachment] 
@client_id varchar(10), 
@queue_id varchar(50),
@attachment_id varchar(50),
@txt_content nvarchar(max),
@bin_content varbinary(max),
@file_format varchar(1)
AS
     INSERT INTO databus.queue_attachment(
         client_id,
         queue_id,
         attachment_id,
         txt_content,
         bin_content,
         file_format)
     VALUES(
         @client_id,
         @queue_id,
         @attachment_id,
         @txt_content,
         @bin_content,
         @file_format)
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [databus].[log_worst_message_type] as

select client_id, log_id,
    case 
        when message_order = 1 then 'E'
        when message_order = 2 then 'W'
        when message_order = 3 then 'I'
    end as worst_message_type
from (
    select client_id, log_id, min(message_order) as message_order
    from ( 
        select distinct client_id, log_id, message_type, 
            case 
                when message_type = 'E' then 1
                when message_type = 'W' then 2
                when message_type = 'I' then 3
            end as message_order
        from databus.log_item 
        ) as x
    group by client_id, log_id
) as y

GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [databus].[webuser](
	[client_id] [varchar](10) NOT NULL,
	[username] [varchar](20) NOT NULL,
	[password] [nvarchar](20) NULL,
	[token] [nvarchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [databus].[webuser] ADD  CONSTRAINT [user_ok] PRIMARY KEY CLUSTERED 
(
	[client_id] ASC,
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [databus].[webuser]  WITH CHECK ADD FOREIGN KEY([client_id])
REFERENCES [databus].[client] ([client_id])
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [databus].[primary_keys] as

select _tab.table_name, _col.column_name
    from 
        INFORMATION_SCHEMA.TABLE_CONSTRAINTS as _tab
        inner join INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE as _col ON
            _col.TABLE_CATALOG = _tab.TABLE_CATALOG AND
            _col.TABLE_SCHEMA = _tab.TABLE_SCHEMA AND
            _col.TABLE_NAME = _tab.TABLE_NAME AND
            _col.CONSTRAINT_NAME = _tab.CONSTRAINT_NAME
    where _tab.CONSTRAINT_TYPE = 'PRIMARY KEY'

GO