
_create_admin_roles = """
CREATE TABLE IF NOT EXISTS admin_roles (
    guild_id bigint  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT admin_roles_pk PRIMARY KEY (role_id)
);"""

_create_bots = """
CREATE TABLE IF NOT EXISTS bots (
    bot_id bigint  NOT NULL,
    presence_action varchar(12)  NULL,
    presence_value text  NULL,
    CONSTRAINT bots_pk PRIMARY KEY (bot_id)
);
"""

_create_cringe_links = """
CREATE TABLE IF NOT EXISTS cringe_links (
    guild_id bigint  NOT NULL,
    url text  NOT NULL,
    CONSTRAINT cringe_links_pk PRIMARY KEY (url,guild_id)
);
"""

_create_exempt_channel_ids = """
CREATE TABLE IF NOT EXISTS exempt_channel_ids (
    guild_id bigint  NOT NULL,
    channel_id bigint  NOT NULL,
    CONSTRAINT exempt_channel_ids_pk PRIMARY KEY (channel_id)
);
"""

_create_guilds = """
CREATE TABLE IF NOT EXISTS guilds (
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
"""

_create_helper_roles = """
CREATE TABLE IF NOT EXISTS helper_roles (
    guild_id bigint  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT helper_roles_pk PRIMARY KEY (role_id)
);
"""

_create_ignored_response_ids = """
CREATE TABLE ignored_response_ids (
    guild_id bigint  NOT NULL,
    response_id int  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT ignored_response_ids_pk PRIMARY KEY (guild_id,role_id,response_id)
);
"""

_create_mod_rules = """
CREATE TABLE IF NOT EXISTS mod_roles (
    guild_id bigint  NOT NULL,
    role_id bigint  NOT NULL,
    CONSTRAINT mod_roles_pk PRIMARY KEY (role_id)
);
"""

_create_mutes = """
CREATE TABLE IF NOT EXISTS mutes (
    guild_id bigint  NOT NULL,
    user_id bigint  NOT NULL,
    expiry bigint  NOT NULL,
    CONSTRAINT mutes_pk PRIMARY KEY (user_id,guild_id)
);
"""

_create_responses = """
CREATE TABLE IF NOT EXISTS responses (
    guild_id bigint  NOT NULL,
    response_id int  NOT NULL GENERATED ALWAYS AS IDENTITY,
    title text  NULL,
    description text  NULL,
    regex text  NOT NULL,
    delete_message boolean  NOT NULL,
    CONSTRAINT responses_pk PRIMARY KEY (guild_id,response_id)
);
"""

_create_rules = """
CREATE TABLE IF NOT EXISTS rules (
    guild_id bigint  NOT NULL,
    rule_number int  NOT NULL,
    rule_title text  NOT NULL,
    rule_description text  NOT NULL,
    CONSTRAINT rules_pk PRIMARY KEY (rule_number,guild_id)
);
"""

_alter_admin_roles = """
ALTER TABLE admin_roles ADD CONSTRAINT admins_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_cringe_links = """
ALTER TABLE cringe_links ADD CONSTRAINT cringe_links_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_exempt_channel_ids = """
ALTER TABLE exempt_channel_ids ADD CONSTRAINT exempt_ids_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_helper_roles = """
ALTER TABLE helper_roles ADD CONSTRAINT helpers_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_ignored_response_ids = """
ALTER TABLE ignored_response_ids ADD CONSTRAINT ignored_response_ids_responses
    FOREIGN KEY (guild_id, response_id)
    REFERENCES responses (guild_id, response_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_mod_roles = """
ALTER TABLE mod_roles ADD CONSTRAINT mods_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_mutes = """
ALTER TABLE mutes ADD CONSTRAINT mutes_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_responses = """
ALTER TABLE responses ADD CONSTRAINT responses_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

_alter_rules = """
ALTER TABLE rules ADD CONSTRAINT rules_guilds
    FOREIGN KEY (guild_id)
    REFERENCES guilds (guild_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;
"""

CREATES_LIST = {
    'admin_roles': _create_admin_roles,
    'bots': _create_bots,
    'cringe_links': _create_cringe_links,
    'exempt_channel_ids': _create_exempt_channel_ids,
    'guilds': _create_guilds,
    'helper_roles': _create_helper_roles,
    'ignored_response_ids': _create_ignored_response_ids,
    'mod_rules': _create_mod_rules,
    'mutes': _create_mutes,
    'responses': _create_responses,
    'rules': _create_rules,
}

ALTERS_LIST = {
    'admin_roles': _alter_admin_roles,
    'cringe_links': _alter_cringe_links,
    'exempt_channel_ids': _alter_exempt_channel_ids,
    'helper_roles': _alter_helper_roles,
    'ignored_response_ids': _alter_ignored_response_ids,
    'mod_roles': _alter_mod_roles,
    'mutes': _alter_mutes,
    'responses': _alter_responses,
    'rules': _alter_rules
}
