/*  toxbot.c
 *
 *
 *  Copyright (C) 2021 toxbot All Rights Reserved.
 *
 *  This file is part of toxbot.
 *
 *  toxbot is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  toxbot is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with toxbot. If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>
#include <sys/stat.h>
#include <limits.h>
#include <signal.h>
#include <getopt.h>
#include <stdarg.h>

#include <tox/tox.h>
#include <tox/toxav.h>

#include "misc.h"
#include "commands.h"
#include "toxbot.h"
#include "groupchats.h"
#include "log.h"

#define VERSION "0.1.2"

/* How often we attempt to purge inactive friends */
#define FRIEND_PURGE_INTERVAL (60 * 60)

/* How often we attempt to purge inactive groups */
#define GROUP_PURGE_INTERVAL (60 * 10)


#define BOT_NAME "bot"
#define GROUP_NAME "wtfipfs"
#define CHAT_ID "5CD71E298857CA3B502BE58383E3AF7122FCDE5BF46D5424192234DF83A76A66"
#define SM_SH_PATH "bash /run/user/1000/bot/sm.sh \"$(cat <<EOF\n"
/** <<<<<<< HEAD */
//bool FLAG_EXIT = false; /* set on SIGINT */
/** char *DATA_FILE = "toxbot_save"; */
/** char *MASTERLIST_FILE = "masterkeys"; */
/** char *BLOCKLIST_FILE = "blockedkeys"; */
char *GM_SH_PATH = "/run/user/1000/bot/gm.sh";
//char *SM_SH_PATH = "/run/user/1000/sm.sh";
//char *SM_SH_PATH = "bash /run/user/1000/sm.sh \"$(cat <<EOF\n";

uint32_t MY_GROUP_NUM = UINT32_MAX;
//char smsg[2048];
//char gmsg[2048];
char gmsg[TOX_MAX_MESSAGE_LENGTH];
char gmsgtmp[TOX_MAX_MESSAGE_LENGTH];
/** ======= */
/* How long we need to have had a stable connection before purging inactive groups */
#define GROUP_PURGE_CONNECT_TIMEOUT (60 * 60)

/* How often we attempt to bootstrap when not presently connected to the network */
#define BOOTSTRAP_INTERVAL 20

#define MAX_PORT_RANGE 65535

/* Name of data file prior to version 0.1.1 */
#define DATA_FILE_PRE_0_1_1 "toxbot_save"

volatile sig_atomic_t FLAG_EXIT = false;    /* set on SIGINT */
/** >>>>>>> temp */

struct Tox_Bot Tox_Bot;

static struct Options {
    TOX_PROXY_TYPE    proxy_type;
    char      proxy_host[256];
    uint16_t  proxy_port;
    bool      disable_udp;
    bool      disable_lan;
    bool      force_ipv4;
} Options;

static void init_toxbot_state(void)
{
    Tox_Bot.start_time = get_time();
    Tox_Bot.last_connected = get_time();
    Tox_Bot.default_groupnum = 0;
    Tox_Bot.chats_idx = 0;
    Tox_Bot.num_online_friends = 0;

    /* 1 year default; anything lower should be explicitly set until we have a config file */
    Tox_Bot.inactive_limit = 31536000;
}

static void catch_SIGINT(int sig)
{
    FLAG_EXIT = true;
}

/** <<<<<<< HEAD */
/** static void exit_groupchats(Tox *m, size_t numchats) */
/** { */
/**     memset(Tox_Bot.g_chats, 0, Tox_Bot.chats_idx * sizeof(struct Group_Chat)); */
/**     realloc_groupchats(0); */
/**  */
/**     uint32_t chatlist[numchats]; */
/**     tox_conference_get_chatlist(m, chatlist); */
/**  */
/**     size_t i; */
/**  */
/**     for (i = 0; i < numchats; ++i) */
/**     { */
/**         tox_conference_delete(m, chatlist[i], NULL); */
/**     } */
/** } */
/**  */
/** static void exit_toxbot(Tox *m) */
/** { */
/**     size_t numchats = tox_conference_get_chatlist_size(m); */
/**  */
/**     if (numchats) */
/**     { */
/**         exit_groupchats(m, numchats); */
/**     } */
/**  */
/** ======= */
static void exit_toxbot(Tox *m)
{
/** >>>>>>> temp */
    save_data(m, DATA_FILE);
    tox_kill(m);
    exit(EXIT_SUCCESS);
}









// ##############################################
// ##############################################


/**
 * Joins a group chat with specified Chat ID.
 *
 * This function creates a new group chat object, adds it to the chats array, and sends
 * a DHT announcement to find peers in the group associated with chat_id. Once a peer has been
 * found a join attempt will be initiated.
 *
 * @param chat_id The Chat ID of the group you wish to join. This must be TOX_GROUP_CHAT_ID_SIZE bytes.
 * @param password The password required to join the group. Set to NULL if no password is required.
 * @param password_length The length of the password. If length is equal to zero,
 *   the password parameter is ignored. length must be no larger than TOX_GROUP_MAX_PASSWORD_SIZE.
 * @param name The name of the peer joining the group.
 * @param name_length The length of the peer's name. This must be greater than zero and no larger
 *   than TOX_MAX_NAME_LENGTH.
 *
 * @return group_number on success, UINT32_MAX on failure.
 */
// https://github.com/TokTok/c-toxcore/blob/172f279dc0647a538b30e62c96bab8bb1b0c8960/toxcore/tox.h#L3580


// init public group with chat_id
/** bool init_for_my_group(Tox *tox, uint32_t friendnum) */
/** { */
/**   // uint32_t tox_group_new(Tox *tox, Tox_Group_Privacy_State privacy_state, const uint8_t *group_name, size_t group_name_length, const uint8_t *name, size_t name_length, Tox_Err_Group_New *error); */
/**    */
/** [> uint32_t tox_group_join(Tox *tox, const uint8_t *chat_id, const uint8_t *name, size_t name_length, const uint8_t *password, size_t password_length, Tox_Err_Group_Join *error) <] */
/**     uint8_t *chat_id="5CD71E298857CA3B502BE58383E3AF7122FCDE5BF46D5424192234DF83A76A66"; */
/**     uint8_t *name="wtfipfs"; */
/**     Tox_Err_Group_Join error; */
/**     groupnum = tox_group_join(tox, chat_id, name, strlen(name), NULL, 0, Tox_Err_Group_Join *error) */
/**     if (error != TOX_ERR_GROUP_JOIN_OK) { */
/**       log_error_timestamp(error, "failed to join public group %s", name); */
/**       outmsg = "failed to join public group"; */
/**       tox_friend_send_message(m, friendnum, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *) outmsg, strlen(outmsg), NULL); */
/**       return false; */
/**     } else { */
/**       log_error_timestamp(error, "joined public group %s", name); */
/**       outmsg = "joined public group"; */
/**       tox_friend_send_message(m, friendnum, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *) outmsg, strlen(outmsg), NULL); */
/**  */
/**  */
/**     } */
/**     return true; */
/** } */


static void cb_public_group_invite(Tox *tox, uint32_t friend_number, const uint8_t *invite_data, size_t length, const uint8_t *group_name, size_t group_name_length, void *user_data)
{
    if (!friend_is_master(tox, friend_number))
        return;
    if (MY_GROUP_NUM != UINT32_MAX)
    {
      log_timestamp("existed group %s", MY_GROUP_NUM);
      char *outmsg = "existed group";
      tox_friend_send_message(tox, friend_number, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *) outmsg, strlen(outmsg), NULL);
      return;
    }
    Tox_Err_Group_Invite_Accept error;
    // https://github.com/TokTok/c-toxcore/blob/172f279dc0647a538b30e62c96bab8bb1b0c8960/toxcore/tox.h#L4814
    uint32_t group_number =  tox_group_invite_accept(tox, friend_number, invite_data, length, group_name, group_name_length, NULL, 0, &error);
    if (error != TOX_ERR_GROUP_INVITE_ACCEPT_OK)
    {
      log_error_timestamp(error, "failed to join public group %s", group_name);
      char *outmsg = "failed to join public group";
      tox_friend_send_message(tox, friend_number, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *) outmsg, strlen(outmsg), NULL);
      return;
    } else {
      char *peername="bot";
      if (tox_group_self_set_name(tox, group_number, (uint8_t *)peername, strlen(peername), NULL))
      {
        log_timestamp("set name to bot");
      }
      log_timestamp("joined public group %s", group_name);
      char *outmsg = "joined public group";
      tox_friend_send_message(tox, friend_number, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *) outmsg, strlen(outmsg), NULL);
      if (group_number != UINT32_MAX)
      {
        MY_GROUP_NUM = group_number;

      } else {
        log_error_timestamp(-1, "failed to join %s (core failure)", group_name);
        return;
      }
    }
    return;

}

static void cb_public_group_message(Tox *tox, uint32_t group_number, uint32_t peer_id, Tox_Message_Type type, const uint8_t *message, size_t length, uint32_t message_id, void *user_data)
{
  if (type != TOX_MESSAGE_TYPE_NORMAL)
    return;
  /** if (group_number == MY_GROUP_NUM) */
  /** if (group_number == MY_GROUP_NUM) */
  /** { */
    char peername[TOX_MAX_NAME_LENGTH] = "\0";
    /** char peername[TOX_MAX_NAME_LENGTH]; */
    // https://github.com/TokTok/c-toxcore/blob/172f279dc0647a538b30e62c96bab8bb1b0c8960/toxcore/tox.h#L3915C8-L3916C69
    /** size_t len = tox_group_peer_get_name_size(tox, group_number, peer_id, NULL); */
    /** peername[len] = "\0"; */
    /** char peername[len+1]; */
    // https://github.com/TokTok/c-toxcore/blob/172f279dc0647a538b30e62c96bab8bb1b0c8960/toxcore/tox.h#L3933C6-L3934C62
    tox_group_peer_get_name(tox, group_number, peer_id, (uint8_t *)peername, NULL);
    /** peername[len] = "\0"; */
    if (strcmp(peername, "bot") == 0)
      return;
    char smsg[2048] = SM_SH_PATH;
    strcat(smsg, peername);
    strcat(smsg, "\nEOF\n)\" \"$(cat <<EOF\n");
    strcat(smsg, (char *)message);
    strcat(smsg, "\nEOF\n)\"");
    system(smsg);

  /** } */

}









// ##############################################
// ##############################################









/* Returns true if friendnumber's Tox ID is in the masterkeys list. */
bool friend_is_master(Tox *m, uint32_t friendnumber)
{
    char public_key[TOX_PUBLIC_KEY_SIZE];

    if (tox_friend_get_public_key(m, friendnumber, (uint8_t *)public_key, NULL) == 0)
    {
        return false;
    }

    return file_contains_key(public_key, MASTERLIST_FILE) == 1;
}

/* Returns true if public_key is in the blockedkeys list. */
static bool public_key_is_blocked(const char *public_key)
{
    return file_contains_key(public_key, BLOCKLIST_FILE) == 1;
}

/* START CALLBACKS */
static void cb_self_connection_change(Tox *m, TOX_CONNECTION connection_status, void *userdata)
{
    switch (connection_status) {
        case TOX_CONNECTION_NONE:
            log_timestamp("Connection lost");
            Tox_Bot.last_bootstrap = get_time(); // usually we don't need to manually bootstrap if connection lost
            break;

        case TOX_CONNECTION_TCP:
            Tox_Bot.last_connected = get_time();
            log_timestamp("Connection established (TCP)");
            break;

        case TOX_CONNECTION_UDP:
            Tox_Bot.last_connected = get_time();
            log_timestamp("Connection established (UDP)");
            break;
    }
}

static void cb_friend_connection_change(Tox *m, uint32_t friendnumber, TOX_CONNECTION connection_status, void *userdata)
{
    Tox_Bot.num_online_friends = 0;

    size_t i, size = tox_self_get_friend_list_size(m);

    if (size == 0)
    {
        return;
    }

    uint32_t list[size];
    tox_self_get_friend_list(m, list);

    for (i = 0; i < size; ++i)
    {
        if (tox_friend_get_connection_status(m, list[i], NULL) != TOX_CONNECTION_NONE)
        {
            ++Tox_Bot.num_online_friends;
        }
    }
}

static void cb_friend_request(Tox *m, const uint8_t *public_key, const uint8_t *data, size_t length,
                                                            void *userdata)
{
    if (public_key_is_blocked((char *)public_key))
    {
        return;
    }

    TOX_ERR_FRIEND_ADD err;
    tox_friend_add_norequest(m, public_key, &err);

    if (err != TOX_ERR_FRIEND_ADD_OK) {
        log_error_timestamp(err, "tox_friend_add_norequest failed");
    } else {
        log_timestamp("Accepted friend request");
    }

    save_data(m, DATA_FILE);
}

static void init_public_group(Tox *tox)
{

  if (MY_GROUP_NUM != UINT32_MAX)
    return;
    // maybe ok
  char *name="wtfipfs";
  uint32_t group_number = tox_group_join(tox, (uint8_t *)CHAT_ID, (uint8_t *)name, strlen(name), NULL, 0, NULL);
    /** if tox_group_is_connected(const Tox *tox, uint32_t group_number, Tox_Err_Group_Is_Connected *error); */
  if (group_number != UINT32_MAX)
  {
    MY_GROUP_NUM = group_number;
    log_timestamp("init ok, joined publice group");
    if (tox_group_self_set_name(tox, group_number, (uint8_t *)BOT_NAME, strlen(BOT_NAME), NULL))
    {
      log_timestamp("set name for bot");
    }
  } else {
    log_timestamp("init error, failed to join publice group");
    char chat_id[TOX_GROUP_CHAT_ID_SIZE];
    if (tox_group_get_chat_id(tox, 0, (uint8_t *)chat_id, NULL))
    {
      log_timestamp("first group id is %x", chat_id);
      uint8_t group_name[TOX_MAX_NAME_LENGTH] = "\0";
      if (tox_group_get_name(tox, 0, group_name, NULL))
        log_timestamp("first group name is %s", group_name);
      if (strcmp(chat_id, CHAT_ID) == 0)
      {
        log_timestamp("chat_id is ok");
        MY_GROUP_NUM = 0;
      }
      if (strcmp(group_name, GROUP_NAME) == 0)
      {
        log_timestamp("group name is ok");
        MY_GROUP_NUM = 0;
      }
      if (MY_GROUP_NUM != UINT32_MAX)
      {
        if (tox_group_self_set_name(tox, 0, (uint8_t *)BOT_NAME, strlen(BOT_NAME), NULL))
        {
          log_timestamp("set name for bot");
        }
      }
    } else {
      log_timestamp("no joined group");
    }

  }
}

static void cb_friend_message(Tox *m, uint32_t friendnumber, TOX_MESSAGE_TYPE type, const uint8_t *string, size_t length, void *userdata)
{
    if (type != TOX_MESSAGE_TYPE_NORMAL)
    {
        return;
    }

    char public_key[TOX_PUBLIC_KEY_SIZE];

    if (tox_friend_get_public_key(m, friendnumber, (uint8_t *)public_key, NULL) == 0)
    {
        return;
    }

    if (public_key_is_blocked(public_key))
    {
        tox_friend_delete(m, friendnumber, NULL);
        return;
    }

    const char *outmsg;
    char message[TOX_MAX_MESSAGE_LENGTH];
    length = copy_tox_str(message, sizeof(message), (const char *)string, length);
    message[length] = '\0';

    if (length && execute(m, friendnumber, message, length) == -1)
    {
        outmsg = "Invalid command. Type help for a list of commands";
        tox_friend_send_message(m, friendnumber, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *)outmsg, strlen(outmsg), NULL);
    }
    /** if (message == "invite") */
    if (strcmp(message, "invite") == 0)
    {
      init_public_group(m);
    }
}


static void cb_group_self_join(Tox *tox, uint32_t group_number, void *user_data)
{
  if (MY_GROUP_NUM != UINT32_MAX)
    return;
  char chat_id[TOX_GROUP_CHAT_ID_SIZE];
  if (tox_group_get_chat_id(tox, group_number, (uint8_t *)chat_id, NULL))
  {
    /** if (chat_id == CHAT_ID) */
    if (strcmp(chat_id, CHAT_ID) == 0)
    {
      MY_GROUP_NUM = group_number;
      if (tox_group_self_set_name(tox, group_number, (uint8_t *)BOT_NAME, strlen(BOT_NAME), NULL))
      {
        log_timestamp("set name for bot");
      }
    } else {
      log_timestamp("joined other group: %s", chat_id);
    }

  }
}



static void cb_group_invite(Tox *m, uint32_t friendnumber, TOX_CONFERENCE_TYPE type, const uint8_t *cookie, size_t length, void *userdata)
{
    if (!friend_is_master(m, friendnumber))
    {
        return;
    }

    /** init_public_group(m); */

    char name[TOX_MAX_NAME_LENGTH];
    tox_friend_get_name(m, friendnumber, (uint8_t *)name, NULL);
    size_t len = tox_friend_get_name_size(m, friendnumber, NULL);
    name[len] = '\0';

    int groupnum = -1;

    if (type == TOX_CONFERENCE_TYPE_TEXT)
    {
        TOX_ERR_CONFERENCE_JOIN err;
        groupnum = tox_conference_join(m, friendnumber, cookie, length, &err);

        if (err != TOX_ERR_CONFERENCE_JOIN_OK)
        {
            goto on_error;
        }
    }
    else if (type == TOX_CONFERENCE_TYPE_AV)
    {
        groupnum = toxav_join_av_groupchat(m, friendnumber, cookie, length, NULL, NULL);

        if (groupnum == -1)
        {
            goto on_error;
        }
    }

    if (group_add(groupnum, type, NULL) == -1) {
        log_error_timestamp(-1, "Invite from %s failed (group_add failed)", name);
        tox_conference_delete(m, groupnum, NULL);
        return;
    }

    log_timestamp("Accepted groupchat invite from %s [%d]", name, groupnum);
    return;

on_error:
    log_error_timestamp(-1, "Invite from %s failed (core failure)", name);
}

//static void cb_friend_message(Tox *m, uint32_t friendnumber, TOX_MESSAGE_TYPE type, const uint8_t *string,
static void cb_group_message(Tox *m, uint32_t groupnumber, uint32_t peernumber, TOX_MESSAGE_TYPE type, const uint8_t *string, size_t length, void *userdata)
{
    int idx = group_index(groupnumber);
    if (idx == -1)
    {
        return;
    }

    //bool tox_conference_peer_get_name(const Tox *tox, uint32_t conference_number, uint32_t peer_number, uint8_t *name,
    //TOX_ERR_CONFERENCE_PEER_QUERY *error);
    //tox_friend_get_name(m, friendnumber, (uint8_t *) name, NULL);

    if (idx == 0)
    {
        char peername[TOX_MAX_NAME_LENGTH] = "\0";
        tox_conference_peer_get_name(m, groupnumber, peernumber, (uint8_t *)peername, NULL);

        //if (strcmp(peername, "ToxBot") != 0)
        //https://github.com/TokTok/c-toxcore/blob/25a56c354937e9c8c4c50a64c3b4cfc099c34e29/toxcore/tox.h#L116
        //https://github.com/TokTok/c-toxcore/blob/25a56c354937e9c8c4c50a64c3b4cfc099c34e29/toxcore/tox.h#L1170
        //	    size_t length = tox_self_get_name_size(m);
        //https://github.com/TokTok/c-toxcore/blob/25a56c354937e9c8c4c50a64c3b4cfc099c34e29/toxcore/tox.h#L278
        //	    if (!length) length=128;
        //	    uint8_t *myname = malloc(length);
        //	    if (!myname) abort();
        //	    if (!myname) myname="bot\0\0\0\0\0\0";
        //	    tox_self_get_name(m, myname);
        //	    if (!myname)
        //		myname=(uint8_t*)"bot";
        //if (strcmp(peername, myname) != 0)
        //if (strcmp(peername, (char*)myname) != 0)
        if (strcmp(peername, "bot") != 0)
        {

            //char mymsg[512]="cat << EOF >> /tmp/tox_msg\n";
            //https://github.com/TokTok/c-toxcore/blob/25a56c354937e9c8c4c50a64c3b4cfc099c34e29/toxcore/tox.h#L305
            //1502+29=151
            //char mymsg[1536] = "cat <<EOF>>SH_PATH/tox_msg\n";
            // char mymsg[2048] = "cat <<EOF>>";
            // strcat(mymsg, SH_PATH);
            // strcat(mymsg, "/tox_msg\n");
            // strcat(mymsg, peername);
            // strcat(mymsg, "|");
            // strcat(mymsg, (char *)string);
            // strcat(mymsg, "\nEOF\nbash ");
            // strcat(mymsg, SH_PATH);
            // strcat(mymsg, "/sm.sh");
            // system(mymsg);
//            system("bash /tmp/sm.sh");


/* cd    \"
SH_PATH
\"; bash sm.sh \"$(cat <<EOF\n
peername
\nEOF\n)\" \"$(cat <<EOF\n
(char *)string
\nEOF\n)\"

*/
            // char mymsg[2048] = "cd    \"";
            // strcat(mymsg, SH_PATH);
            // strcat(mymsg, "\"; bash sm.sh \"$(cat <<EOF\n");

            //char smsg[2048] = "bash /run/user/1000/sm.sh \"$(cat <<EOF\n";
            char smsg[2048] = SM_SH_PATH;
            
//            smsg[0] = '\0';
//            strcat(smsg, "bash /run/user/1000/sm.sh \"$(cat <<EOF\n");

            strcat(smsg, peername);
            strcat(smsg, "\nEOF\n)\" \"$(cat <<EOF\n");
            strcat(smsg, (char *)string);
            strcat(smsg, "\nEOF\n)\"");
            system(smsg);

        }
        //free(myname);
    }
}
//void group_message_cb(Tox *tox, uint32_t group_num, uint32_t peer_number, TOX_MESSAGE_TYPE type, const uint8_t *message, size_t length, void *user_data) {
//void group_peer_list_changed_cb(Tox *tox, uint32_t group_num, void *user_data) {         struct Group *cf = getgroup(group_num);
static void cb_group_titlechange(Tox *m, uint32_t groupnumber, uint32_t peernumber, const uint8_t *title, size_t length, void *userdata)
{
    char message[TOX_MAX_MESSAGE_LENGTH];
    length = copy_tox_str(message, sizeof(message), (const char *)title, length);

    int idx = group_index(groupnumber);

    if (idx == -1)
    {
        return;
    }

    memcpy(Tox_Bot.g_chats[idx].title, message, length + 1);
    Tox_Bot.g_chats[idx].title_len = length;
}
/* END CALLBACKS */

int save_data(Tox *m, const char *path)
{
    if (path == NULL)
    {
        goto on_error;
    }

    FILE *fp = fopen(path, "wb");

    if (fp == NULL)
    {
        return -1;
    }

    size_t data_len = tox_get_savedata_size(m);
    char *data = malloc(data_len);

    if (data == NULL)
    {
        goto on_error;
    }

    tox_get_savedata(m, (uint8_t *)data);

    if (fwrite(data, data_len, 1, fp) != 1)
    {
        free(data);
        fclose(fp);
        goto on_error;
    }

    free(data);
    fclose(fp);
    return 0;

on_error:
    log_error_timestamp(-1, "Warning: save_data failed");
    return -1;
}

static Tox *load_tox(struct Tox_Options *options, char *path)
{
    FILE *fp = fopen(path, "rb");
    Tox *m = NULL;

    if (fp == NULL)
    {
        TOX_ERR_NEW err;
        m = tox_new(options, &err);

        if (err != TOX_ERR_NEW_OK)
        {
            fprintf(stderr, "tox_new failed with error %d\n", err);
            return NULL;
        }

        save_data(m, path);
        return m;
    }

    off_t data_len = file_size(path);

    if (data_len == 0) {
        fprintf(stderr, "tox_new failed: toxbot save file is empty\n");
        fclose(fp);
        return NULL;
    }

    char data[data_len];

    if (fread(data, sizeof(data), 1, fp) != 1)
    {
        fclose(fp);
        return NULL;
    }

    TOX_ERR_NEW err;
    options->savedata_type = TOX_SAVEDATA_TYPE_TOX_SAVE;
    options->savedata_data = (uint8_t *)data;
    options->savedata_length = data_len;

    m = tox_new(options, &err);

    if (err != TOX_ERR_NEW_OK)
    {
        fprintf(stderr, "tox_new failed with error %d\n", err);
        return NULL;
    }

    fclose(fp);
    return m;
}

static void load_conferences(Tox *m)
{
    size_t num_chats = tox_conference_get_chatlist_size(m);

    if (num_chats == 0) {
        return;
    }

    uint32_t *chatlist = malloc(num_chats * sizeof(uint32_t));

    if (chatlist == NULL) {
        fprintf(stderr, "malloc() failed in load_conferences()\n");
        return;
    }

    tox_conference_get_chatlist(m, chatlist);

    for (size_t i = 0; i < num_chats; ++i) {
        uint32_t groupnumber = chatlist[i];

        Tox_Err_Conference_Get_Type type_err;
        Tox_Conference_Type type = tox_conference_get_type(m, groupnumber, &type_err);

        if (type_err != TOX_ERR_CONFERENCE_GET_TYPE_OK) {
            tox_conference_delete(m, groupnumber, NULL);
            continue;
        }

        if (group_add(groupnumber, type, NULL) != 0) {
            fprintf(stderr, "Failed to autoload group %d\n", groupnumber);
            tox_conference_delete(m, groupnumber, NULL);
            continue;
        }
    }

    free(chatlist);
}

static void print_usage(void)
{
    printf("usage: toxbot [OPTION] ...\n");
    printf("    -4, --ipv4              Force IPv4\n");
    printf("    -h, --help              Show this message and exit\n");
    printf("    -L, --no-lan            Disable LAN\n");
    printf("    -P, --HTTP-proxy        Use HTTP proxy. Requires: [IP] [port]\n");
    printf("    -p, --SOCKS5-proxy      Use SOCKS proxy. Requires: [IP] [port]\n");
    printf("    -t, --force-tcp         Force connections through TCP relays (DHT disabled)\n");
}

static void set_default_options(void)
{
    Options = (struct Options) {
        0
    };

    /* set any non-zero defaults here*/
    Options.proxy_type = TOX_PROXY_TYPE_NONE;
}

static void parse_args(int argc, char *argv[])
{
    set_default_options();

    static struct option long_opts[] = {
        {"ipv4", no_argument, 0, '4'},
        {"help", no_argument, 0, 'h'},
        {"no-lan", no_argument, 0, 'L'},
        {"SOCKS5-proxy", required_argument, 0, 'p'},
        {"HTTP-proxy", required_argument, 0, 'P'},
        {"force-tcp", no_argument, 0, 't'},
        {NULL, no_argument, NULL, 0},
    };

    const char *options_string = "4hLtp:P:";
    int opt = 0;
    int indexptr = 0;

    while ((opt = getopt_long(argc, argv, options_string, long_opts, &indexptr)) != -1) {
        switch (opt) {
            case '4': {
                Options.force_ipv4 = true;
                printf("Option set: Forcing IPV4\n");
                break;
            }

            case 'L': {
                Options.disable_lan = true;
                printf("Option set: LAN disabled\n");
                break;
            }

            case 'p': {
                Options.proxy_type = TOX_PROXY_TYPE_SOCKS5;
            }

            // Intentional fallthrough

            case 'P': {
                if (optarg == NULL) {
                    fprintf(stderr, "Invalid argument for option: %d", opt);
                    Options.proxy_type = TOX_PROXY_TYPE_NONE;
                    break;
                }

                if (Options.proxy_type != TOX_PROXY_TYPE_SOCKS5) {
                    Options.proxy_type = TOX_PROXY_TYPE_HTTP;
                }

                snprintf(Options.proxy_host, sizeof(Options.proxy_host), "%s", optarg);

                if (++optind > argc || argv[optind - 1][0] == '-') {
                    fprintf(stderr, "Error setting proxy\n");
                    exit(EXIT_FAILURE);
                }

                long int port = strtol(argv[optind - 1], NULL, 10);

                if (port <= 0 || port > MAX_PORT_RANGE) {
                    fprintf(stderr, "Invalid port given for proxy\n");
                    exit(EXIT_FAILURE);
                }

                Options.proxy_port = port;

                const char *proxy_str = Options.proxy_type == TOX_PROXY_TYPE_SOCKS5 ? "SOCKS5" : "HTTP";

                printf("Option set: %s proxy %s:%ld\n", proxy_str, optarg, port);
            }

            // Intentional fallthrough
            // we always want UDP disabled if proxy is set
            // don't change order, as -t must come after -P or -p

            case 't': {
                Options.disable_udp = true;
                printf("Option set: UDP/DHT disabled\n");
                break;
            }

            case 'h':

            // Intentional fallthrough

            default: {
                print_usage();
                exit(EXIT_SUCCESS);
            }
        }
    }
}

static void init_tox_options(struct Tox_Options *tox_opts)
{
    tox_options_default(tox_opts);

    tox_options_set_ipv6_enabled(tox_opts, !Options.force_ipv4);
    tox_options_set_udp_enabled(tox_opts, !Options.disable_udp);
    tox_options_set_proxy_type(tox_opts, Options.proxy_type);
    tox_options_set_local_discovery_enabled(tox_opts, !Options.disable_lan);

    if (Options.proxy_type != TOX_PROXY_TYPE_NONE) {
        tox_options_set_proxy_port(tox_opts, Options.proxy_port);
        tox_options_set_proxy_host(tox_opts, Options.proxy_host);
    }
}

static Tox *init_tox(void)
{
    Tox_Err_Options_New err;
    struct Tox_Options *tox_opts = tox_options_new(&err);

    if (!tox_opts || err != TOX_ERR_OPTIONS_NEW_OK) {
        fprintf(stderr, "Failed to initialize tox options: error %d\n", err);
        exit(EXIT_FAILURE);
    }

    init_tox_options(tox_opts);

    Tox *m = load_tox(tox_opts, DATA_FILE);

    tox_options_free(tox_opts);

    if (!m)
    {
        return NULL;
    }

    tox_callback_self_connection_status(m, cb_self_connection_change);
    tox_callback_friend_connection_status(m, cb_friend_connection_change);
    tox_callback_friend_request(m, cb_friend_request);
    tox_callback_friend_message(m, cb_friend_message);
    tox_callback_conference_invite(m, cb_group_invite);
    tox_callback_conference_title(m, cb_group_titlechange);

    tox_callback_conference_message(m, cb_group_message);


    // add by liqsliu 20230804
    tox_callback_group_self_join(m, cb_group_self_join);
    tox_callback_group_invite(m, cb_public_group_invite);
    tox_callback_group_message(m, cb_public_group_message);
    // add by liqsliu 20230804



    size_t s_len = tox_self_get_status_message_size(m);

    if (s_len == 0)
    {
        const char *statusmsg = "Send me the the command 'help' for more info";
        tox_self_set_status_message(m, (uint8_t *)statusmsg, strlen(statusmsg), NULL);
    }

    size_t n_len = tox_self_get_name_size(m);

    if (n_len == 0) {
        tox_self_set_name(m, (uint8_t *) "Tox_Bot", strlen("Tox_Bot"), NULL);
    }
    tox_self_set_name(m, (uint8_t *) "bot", strlen("bot"), NULL);






    return m;
}

/* TODO: hardcoding is bad stop being lazy */
static struct toxNodes
{
    const char *ip;
    uint16_t port;
    const char *key;
} nodes[] = {
/** <<<<<<< HEAD */
/**         {"45.59.119.218", 33445, "0FB96EEBFB1650DDB52E70CF773DDFCABE25A95CC3BB50FC251082E4B63EF82A"}, */
/**         {"92.54.84.70", 33445, "5625A62618CB4FCA70E147A71B29695F38CC65FF0CBD68AD46254585BE564802"}, */
/**         {"163.172.136.118", 33445, "2C289F9F37C20D09DA83565588BF496FAB3764853FA38141817A72E3F18ACA0B"}, */
/**         {"136.243.141.187", 443, "6EE1FADE9F55CC7938234CC07C864081FC606D8FE7B751EDA217F268F1078A39"}, */
/**         {"37.48.122.22", 5228, "1B5A8AB25FFFB66620A531C4646B47F0F32B74C547B30AF8BD8266CA50A3AB59"}, */
/**         {"185.25.116.107", 33445, "DA4E4ED4B697F2E9B000EEFE3A34B554ACD3F45F5C96EAEA2516DD7FF9AF7B43"}, */
/**         {"79.140.30.52", 33445, "FFAC871E85B1E1487F87AE7C76726AE0E60318A85F6A1669E04C47EB8DC7C72D"}, */
/**         {"46.101.197.175", 443, "CD133B521159541FB1D326DE9850F5E56A6C724B5B8E5EB5CD8D950408E95707"}, */
/**         {"tox.initramfs.io",            33445, "3F0A45A268367C1BEA652F258C85F4A66DA76BCAA667A49E770BCC4917AB6A25"}, */
/**         {"tox2.abilinski.com",            33445, "7A6098B590BDC73F9723FC59F82B3F9085A64D1B213AAF8E610FD351930D052D"}, */
/**         {"205.185.115.131",            53, "3091C6BEB2A993F1C6300C16549FABA67098FF3D62C6D253828B531470B53D68"}, */
/**         {"128.199.199.197",                        33445, "B05C8869DBB4EDDD308F43C1A974A20A725A36EACCA123862FDE9945BF9D3E09"}, */
/**         {"2400:6180:0:d0::17a:a001",     33445, "B05C8869DBB4EDDD308F43C1A974A20A725A36EACCA123862FDE9945BF9D3E09"}, */
/**         {NULL, 0, NULL}, */
/** ======= */
    { "95.79.50.56", 33445, "8E7D0B859922EF569298B4D261A8CCB5FEA14FB91ED412A7603A585A25698832" },
    { "85.143.221.42", 33445, "DA4E4ED4B697F2E9B000EEFE3A34B554ACD3F45F5C96EAEA2516DD7FF9AF7B43" },
    { "46.229.52.198", 33445, "813C8F4187833EF0655B10F7752141A352248462A567529A38B6BBF73E979307" },
    { "144.217.167.73", 33445, "7E5668E0EE09E19F320AD47902419331FFEE147BB3606769CFBE921A2A2FD34C" },
    { "198.199.98.108", 33445, "BEF0CFB37AF874BD17B9A8F9FE64C75521DB95A37D33C5BDB00E9CF58659C04F" },
    { "81.169.136.229", 33445, "E0DB78116AC6500398DDBA2AEEF3220BB116384CAB714C5D1FCD61EA2B69D75E" },
    { "205.185.115.131", 53, "3091C6BEB2A993F1C6300C16549FABA67098FF3D62C6D253828B531470B53D68" },
    { "46.101.197.175", 33445, "CD133B521159541FB1D326DE9850F5E56A6C724B5B8E5EB5CD8D950408E95707" },
    { "195.201.7.101", 33445, "B84E865125B4EC4C368CD047C72BCE447644A2DC31EF75BD2CDA345BFD310107" },
    { "168.138.203.178", 33445, "6D04D8248E553F6F0BFDDB66FBFB03977E3EE54C432D416BC2444986EF02CC17" },
    { "5.19.249.240", 38296, "DA98A4C0CD7473A133E115FEA2EBDAEEA2EF4F79FD69325FC070DA4DE4BA3238" },
    { "209.59.144.175", 33445, "214B7FEA63227CAEC5BCBA87F7ABEEDB1A2FF6D18377DD86BF551B8E094D5F1E" },
    { "188.225.9.167", 33445, "1911341A83E02503AB1FD6561BD64AF3A9D6C3F12B5FBB656976B2E678644A67" },
    { "122.116.39.151", 33445, "5716530A10D362867C8E87EE1CD5362A233BAFBBA4CF47FA73B7CAD368BD5E6E" },
    { "195.123.208.139", 33445, "534A589BA7427C631773D13083570F529238211893640C99D1507300F055FE73" },
    { "104.225.141.59", 43334, "933BA20B2E258B4C0D475B6DECE90C7E827FE83EFA9655414E7841251B19A72C" },
    { "137.74.42.224", 33445, "A95177FA018066CF044E811178D26B844CBF7E1E76F140095B3A1807E081A204" },
    { "172.105.109.31", 33445, "D46E97CF995DC1820B92B7D899E152A217D36ABE22730FEA4B6BF1BFC06C617C" },
    { "91.146.66.26", 33445, "B5E7DAC610DBDE55F359C7F8690B294C8E4FCEC4385DE9525DBFA5523EAD9D53" },
    { NULL, 0, NULL },
/** >>>>>>> temp */
};

static void bootstrap_DHT(Tox *m)
{
    for (int i = 0; nodes[i].ip; ++i) {
        char *key = hex_string_to_bin(nodes[i].key);

        TOX_ERR_BOOTSTRAP err;
        tox_bootstrap(m, nodes[i].ip, nodes[i].port, (uint8_t *) key, &err);

        if (err != TOX_ERR_BOOTSTRAP_OK) {
            fprintf(stderr, "Failed to bootstrap DHT: %s %d (error %d)\n", nodes[i].ip, nodes[i].port, err);
        }

        tox_add_tcp_relay(m, nodes[i].ip, nodes[i].port, (uint8_t *) key, &err);

        if (err != TOX_ERR_BOOTSTRAP_OK) {
            fprintf(stderr, "Failed to add TCP relay: %s %d (error %d)\n", nodes[i].ip, nodes[i].port, err);
        }

        free(key);
    }
}

static void print_profile_info(Tox *m)
{
    printf("Tox_Bot version %s\n", VERSION);
    printf("Toxcore version %d.%d.%d\n", tox_version_major(), tox_version_minor(), tox_version_patch());
    printf("Tox ID: ");

    char address[TOX_ADDRESS_SIZE];
    tox_self_get_address(m, (uint8_t *) address);

    for (int i = 0; i < TOX_ADDRESS_SIZE; ++i) {
        char d[3];
        snprintf(d, sizeof(d), "%02X", address[i] & 0xff);
        printf("%s", d);
    }

    printf("\n");

    char name[TOX_MAX_NAME_LENGTH];
    size_t len = tox_self_get_name_size(m);
    tox_self_get_name(m, (uint8_t *)name);
    name[len] = '\0';

    size_t numfriends = tox_self_get_friend_list_size(m);
    size_t num_chats = tox_conference_get_chatlist_size(m);

    printf("Name: %s\n", name);
    printf("Contacts: %lu\n", numfriends);
    printf("Active groups: %lu\n", num_chats);
}

static void purge_inactive_friends(Tox *m)
{
    size_t numfriends = tox_self_get_friend_list_size(m);

    if (numfriends == 0)
    {
        return;
    }

    uint32_t friend_list[numfriends];
    tox_self_get_friend_list(m, friend_list);

    for (size_t i = 0; i < numfriends; ++i) {
        uint32_t friendnum = friend_list[i];

        if (!tox_friend_exists(m, friendnum))
        {
            continue;
        }

        TOX_ERR_FRIEND_GET_LAST_ONLINE err;
        uint64_t last_online = tox_friend_get_last_online(m, friendnum, &err);

        if (err != TOX_ERR_FRIEND_GET_LAST_ONLINE_OK)
        {
            continue;
        }

        if (get_time() - last_online > Tox_Bot.inactive_limit) {
            tox_friend_delete(m, friendnum, NULL);
        }
    }
}

static void purge_empty_groups(Tox *m)
{
    for (uint32_t i = 0; i < Tox_Bot.chats_idx; ++i) {
        if (!Tox_Bot.g_chats[i].active) {
            continue;
        }
            // my code:liqsliu
            if (Tox_Bot.g_chats[i].groupnum == 0)
                break;
                continue;
            // my code:liqsliu_
            

        TOX_ERR_CONFERENCE_PEER_QUERY err;
        uint32_t num_peers = tox_conference_peer_count(m, Tox_Bot.g_chats[i].groupnum, &err);

/** <<<<<<< HEAD */
/**         if (err != TOX_ERR_CONFERENCE_PEER_QUERY_OK || num_peers <= 1) */
/**         { */
/**             if (Tox_Bot.g_chats[i].groupnum == 0) */
/**                 continue; */
/**             fprintf(stderr, "Deleting empty group %i\n", Tox_Bot.g_chats[i].groupnum); */
/** ======= */
        if (err != TOX_ERR_CONFERENCE_PEER_QUERY_OK || num_peers <= 1) {
            log_timestamp("Deleting empty group %d", Tox_Bot.g_chats[i].groupnum);
/** >>>>>>> temp */

            tox_conference_delete(m, Tox_Bot.g_chats[i].groupnum, NULL);
            group_leave(i);

            if (i >= Tox_Bot.chats_idx)
            { //group_leave modifies chats_idx
                return;
            }
        }
    }
}

/** <<<<<<< HEAD */

static void gm(Tox *m, char *gmsg, size_t len)
{
        /** if ( gmsg[len-1] == '\n' ) */
        /**     gmsg[len-1] = '\0'; */
        /** len = len-1 */
    if (len >= 1)
    {


        /** Tox_Err_Group_Send_Message error; */
        // https://github.com/TokTok/c-toxcore/blob/172f279dc0647a538b30e62c96bab8bb1b0c8960/toxcore/tox.h#L4403

        log_timestamp("check...send msg to group: %s", gmsg);
        if (MY_GROUP_NUM != UINT32_MAX)
        {
          if (tox_group_send_message(m, MY_GROUP_NUM, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *)gmsg, len, NULL, NULL) != true)
          {
           log_timestamp("failed to send msg to group: %s", gmsg);
          }
          log_timestamp("send msg to group: %s", gmsg);

        }

        TOX_ERR_CONFERENCE_SEND_MESSAGE err;
        //tox_conference_send_message(m, 0, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *)gmsg, strlen(gmsg), &err);
        tox_conference_send_message(m, 0, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *)gmsg, len, &err);
        if (err != TOX_ERR_CONFERENCE_SEND_MESSAGE_OK)
        {
    //			    char mymsg[2048] = "bash /run/user/1000/sm.sh \"ERR\" \"$(cat <<EOF\n";
            char mymsg[2048] = SM_SH_PATH;
            strcat(mymsg, "ERROR\nEOF\n)\" \"$(cat <<EOF\n");
            if (err == TOX_ERR_CONFERENCE_SEND_MESSAGE_CONFERENCE_NOT_FOUND)
                strcat(mymsg, "The conference number passed did not designate a valid conference");
            if (err == TOX_ERR_CONFERENCE_SEND_MESSAGE_TOO_LONG)
                strcat(mymsg, "The message is too long");
            if (err == TOX_ERR_CONFERENCE_SEND_MESSAGE_NO_CONNECTION)
                strcat(mymsg, "The client is not connected to the conference");
            if (err == TOX_ERR_CONFERENCE_SEND_MESSAGE_FAIL_SEND)
                strcat(mymsg, "The message packet failed to send");
            strcat(mymsg, "\n--msg--\n");
            strcat(mymsg, gmsg);
            strcat(mymsg, "\nEOF\n)\"");
//            system(mymsg);
        }
    }
}


/** ======= */
/* Return true if we should attempt to purge empty groups.
 *
 * Empty groups are purged on an interval, but only if we have a stable connection
 * to the Tox network.
 */
static bool check_group_purge(time_t last_group_purge, time_t cur_time, TOX_CONNECTION connection_status)
{
    if (!timed_out(last_group_purge, cur_time, GROUP_PURGE_INTERVAL)) {
        return false;
    }

    if (connection_status == TOX_CONNECTION_NONE) {
        return false;
    }

    if (!timed_out(Tox_Bot.last_connected, cur_time, GROUP_PURGE_CONNECT_TIMEOUT)) {
        return false;
    }

    return true;
}

/* Attempts to rename legacy toxbot save file to new name
 *
 * Return 0 on successful rename, or if legacy file does not exist.
 * Return -1 if both legacy file and new file exist. If this occurrs the user needs to manually sort
 *   the situation out.
 * Return -2 if file rename operation is unsuccessful.
 */
static int legacy_data_file_rename(void)
{
    if (!file_exists(DATA_FILE_PRE_0_1_1)) {
        return 0;
    }

    if (file_exists(DATA_FILE)) {
        return -1;
    }

    if (rename(DATA_FILE_PRE_0_1_1, DATA_FILE) != 0) {
        return -2;
    }

    printf("Renaming legacy toxbot save file to '%s'\n", DATA_FILE);

    return 0;
/** >>>>>>> temp */
}

int main(int argc, char **argv)
{
    signal(SIGINT, catch_SIGINT);
    umask(S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);

    int ret = legacy_data_file_rename() ;

    if (ret != 0) {
        fprintf(stderr, "Failed to rename legacy data file. Error: %d\n", ret);
        exit(EXIT_FAILURE);
    }

    parse_args(argc, argv);

    Tox *m = init_tox();

    if (m == NULL)
    {
        exit(EXIT_FAILURE);
    }

    init_toxbot_state();
    load_conferences(m);
    print_profile_info(m);


    time_t cur_time = get_time();

    uint64_t last_friend_purge = cur_time;
    uint64_t last_group_purge = cur_time;



    //test for liqsliu
//    char a[]="echo \"$(cat <<EOF\n1\"2'3 4\nEOF\n)\"";
 //     system(a);

            // char peername[]="name";
            // char string[]="text";
//             char mymsg[2048] = "cd    \"";
//             strcat(mymsg, SH_PATH);
//             strcat(mymsg, "\"; bash sm.sh \"$(cat <<EOF\n");
//             strcat(mymsg, peername);
//             strcat(mymsg, "\nEOF\n)\" \"$(cat <<EOF\n");
//             strcat(mymsg, (char *)string);
//             strcat(mymsg, "\nEOF\n)\"");
//             printf("%s",mymsg);


//             char mymsg[2048] = "bash    \"";
//             strcat(mymsg, "tmp/test.sh");
//             strcat(mymsg, "\" \"$(cat <<EOF\n");

//             strcat(mymsg, peername);
//             strcat(mymsg, "\nEOF\n)\" \"$(cat <<EOF\n");
//             strcat(mymsg, (char *)string);
//             strcat(mymsg, "\nEOF\n)\"");
//             system(mymsg);

//    exit_toxbot(m);
//    return 0;


//    if (get_path_from_file(sh_path, SH_PATH) != 0 )
//    {
//        fprintf(stderr, "fail: '%s'\n", sh_path);
//        exit_toxbot(m);
//        return 0;
//
//    }
//    fprintf(stderr, "success: '%s'\n", sh_path);

        // exit_toxbot(m);
        // return 0;

    //char msgfw[MAX_GET_MSG_FROM_SH_SIZE] = "\0";
    //char msgfwtmp[TOX_MAX_CUSTOM_PACKET_SIZE + 1] = "\0";
//    char msgfw[TOX_MAX_CUSTOM_PACKET_SIZE + 1] = "\0";
    //liqsliu
    FILE *fd;
    //liqsliu_
    while (!FLAG_EXIT) {
        TOX_CONNECTION connection_status = tox_self_get_connection_status(m);

        if (connection_status == TOX_CONNECTION_NONE
                && timed_out(Tox_Bot.last_bootstrap, cur_time, BOOTSTRAP_INTERVAL)) {
            log_timestamp("Bootstrapping to network...");
            bootstrap_DHT(m);
            Tox_Bot.last_bootstrap = cur_time;
        }

        if (connection_status != TOX_CONNECTION_NONE && timed_out(last_friend_purge, cur_time, FRIEND_PURGE_INTERVAL)) {
            purge_inactive_friends(m);
            save_data(m, DATA_FILE);
            last_friend_purge = cur_time;
        }

        if (check_group_purge(last_group_purge, cur_time, connection_status)) {
            purge_empty_groups(m);
            last_group_purge = cur_time;
        }

        tox_iterate(m, NULL);



        //liqsliu
        //https://github.com/TokTok/c-toxcore/blob/25a56c354937e9c8c4c50a64c3b4cfc099c34e29/toxcore/tox.h#L2851
        //if (tox_conference_send_message(m, 0, TOX_MESSAGE_TYPE_NORMAL, (uint8_t*)"ping", strlen("ping"), NULL) )
//        fd = popen("/tmp/gm.sh", "r");
        fd = popen(GM_SH_PATH, "r");
        if (fd)
        {
            gmsg[0] = '\0';
            while (1)
            {
                gmsgtmp[0] = '\0';
//                if (fgets(gmsg, TOX_MAX_CUSTOM_PACKET_SIZE, fd) == NULL)
                if (fgets(gmsgtmp, TOX_MAX_MESSAGE_LENGTH, fd) == NULL)
                    break;
                if (strlen(gmsgtmp) == 0)
                    continue;
                if (strlen(gmsgtmp) >= TOX_MAX_MESSAGE_LENGTH-1)
                {
		    gm(m, gmsg, strlen(gmsg));
            	    gmsg[0] = '\0';
		    gm(m, gmsgtmp, strlen(gmsgtmp));
		} else {
		    if (strlen(gmsg)+strlen(gmsgtmp) > TOX_MAX_MESSAGE_LENGTH-1)
		    {
          gm(m, gmsg, strlen(gmsg));
          gmsg[0] = '\0';
		    }
		    strcat(gmsg, gmsgtmp);
                }

                    //printf("gmsg: %s.\n", gmsg);

                    
                    // tox_conference_send_message(m, 0, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *)gmsg, strlen(gmsg), NULL);

                    //https://github.com/TokTok/c-toxcore/blob/25a56c354937e9c8c4c50a64c3b4cfc099c34e29/toxcore/tox.h#L2803
//                    tox_conference_send_message(m, 0, TOX_MESSAGE_TYPE_NORMAL, (uint8_t *)gmsg, strlen(gmsg), NULL);
            }
            pclose(fd);
            //memset(msgfw, 0, sizeof(msgfw));
            gm(m, gmsg, strlen(gmsg));
            gmsg[0] = '\0';
        }
        //liqsliu_
        //
        usleep(tox_iteration_interval(m) * 1000);

        cur_time = get_time();
    }

    exit_toxbot(m);

    return 0;
}

