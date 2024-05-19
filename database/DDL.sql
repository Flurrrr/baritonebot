-- tables
-- Table: admin_roles
CREATE TABLE IF NOT EXISTS admin_roles (
    guild_id bigint  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT admin_roles_pk PRIMARY KEY (role_id)
);

-- Table: bots
CREATE TABLE bots (
    bot_id bigint  NOT NULL,
    presence_action varchar(12)  NULL,
    presence_value text  NULL,
    CONSTRAINT bots_pk PRIMARY KEY (bot_id)
);

-- Table: cringe_links
CREATE TABLE cringe_links (
    guild_id bigint  NOT NULL,
    url text  NOT NULL,
    CONSTRAINT cringe_links_pk PRIMARY KEY (url,guild_id)
);

-- Table: exempt_channel_ids
CREATE TABLE exempt_channel_ids (
    guild_id bigint  NOT NULL,
    channel_id bigint  NOT NULL,
    CONSTRAINT exempt_channel_ids_pk PRIMARY KEY (channel_id)
);

-- Table: guilds
CREATE TABLE guilds (
    guild_id bigint  NOT NULL,
    voice_role_id bigint  NOT NULL,
    release_role_id bigint  NOT NULL,
    ignored_role_id bigint  NOT NULL,
    logs_channel_id bigint  NOT NULL,
    mod_logs_channel_id bigint  NOT NULL,
    rules_thumbnail_url text  NULL,
    muted_role_id bigint  NOT NULL,
    embed_color varchar(6)  NULL,
    CONSTRAINT guilds_pk PRIMARY KEY (guild_id)
);

-- Table: helper_roles
CREATE TABLE helper_roles (
    guild_id bigint  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT helper_roles_pk PRIMARY KEY (role_id)
);

-- Table: ignored_response_ids
CREATE TABLE ignored_response_ids (
    guild_id bigint  NOT NULL,
    response_number int  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT ignored_response_ids_pk PRIMARY KEY (guild_id,role_id,response_number)
);

-- Table: mod_roles
CREATE TABLE mod_roles (
    guild_id bigint  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT mod_roles_pk PRIMARY KEY (role_id)
);

-- Table: mutes
CREATE TABLE mutes (
    guild_id bigint  NOT NULL,
    user_id bigint  NOT NULL,
    expiry timestamp  NULL,
    CONSTRAINT mutes_pk PRIMARY KEY (user_id,guild_id)
);

-- Table: responses
CREATE TABLE responses (
    guild_id bigint  NOT NULL,
    response_number int  NOT NULL,
    title text  NULL,
    description text  NULL,
    regex text  NOT NULL,
    delete_message boolean  NOT NULL,
    CONSTRAINT responses_pk PRIMARY KEY (guild_id,response_number)
);

-- Table: rules
CREATE TABLE rules (
    guild_id bigint  NOT NULL,
    rule_number int  NOT NULL,
    rule_title text  NOT NULL,
    rule_description text  NOT NULL,
    CONSTRAINT rules_pk PRIMARY KEY (rule_number,guild_id)
);

-- foreign keys
-- Reference: admins_guilds (table: admin_roles)
ALTER TABLE admin_roles ADD CONSTRAINT admins_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: cringe_links_guilds (table: cringe_links)
ALTER TABLE cringe_links ADD CONSTRAINT cringe_links_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: exempt_ids_guilds (table: exempt_channel_ids)
ALTER TABLE exempt_channel_ids ADD CONSTRAINT exempt_ids_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: helpers_guilds (table: helper_roles)
ALTER TABLE helper_roles ADD CONSTRAINT helpers_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: ignored_response_ids_responses (table: ignored_response_ids)
ALTER TABLE ignored_response_ids ADD CONSTRAINT ignored_response_ids_responses
    FOREIGN KEY (guild_id, response_number)
    REFERENCES responses (guild_id, response_number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: mods_guilds (table: mod_roles)
ALTER TABLE mod_roles ADD CONSTRAINT mods_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: mutes_guilds (table: mutes)
ALTER TABLE mutes ADD CONSTRAINT mutes_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: responses_guilds (table: responses)
ALTER TABLE responses ADD CONSTRAINT responses_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: rules_guilds (table: rules)
ALTER TABLE rules ADD CONSTRAINT rules_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

