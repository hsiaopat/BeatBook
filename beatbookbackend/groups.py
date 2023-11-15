# File for groups

NOT IMPLEMENTED YET OR TESTED
def join_group(mysql, headers, group_identifier):
    cursor = mysql.connection.cursor()
    username = get_user(mysql, headers)
    command = "SELECT display_name FROM Users WHERE username = %s"
    cursor.execute(command, (username,))
    name = cursor.fetchone()
    if name:
        name = name[0]
    else:
        cursor.close()
        return False, "User not found"

    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    if group_identifier.isdigit():
        group_id = int(group_identifier)
        group_name_id = f'Group_{group_id}'
    else:
        cursor.execute("SELECT group_id FROM Clubs WHERE group_name = %s", (group_identifier,))
        group_id_result = cursor.fetchone()
        if group_id_result:
            group_id = group_id_result[0]
            group_name_id = f'Group_{group_id}'
        else:
            cursor.close()
            return False, "Group does not exist. You must first create the group"

    if group_name_id in tables:
        command = f"SELECT Member_username FROM {group_name_id}"
        cursor.execute(command)
        current_members = [row[0] for row in cursor.fetchall()]
        if username not in current_members:
            cursor.execute(f"INSERT INTO {group_name_id} (Member_username, Member_name) VALUES (%s, %s)", (username, name))
            cursor.execute("UPDATE Clubs SET num_members = num_members + 1 WHERE group_id = %s", (group_id,))
            cursor.connection.commit()
            cursor.close()
            return True, "User successfully joined the group"
        else:
            cursor.close()
            return False, "User already in the group"
    else:
        cursor.close()
        return False, "Group does not exist. You must first create the group"




#NOT IMPLEMENTED OR TESTED
def create_group(mysql, headers, group_name):
    username = get_user(mysql, headers)
    cursor = mysql.connection.cursor()
    cursor.execute("select display_name from Users where username = '%s'" % username)
    name = cursor.fetchone()  # Fetch a single result directly
    cursor.execute("select group_id from Clubs")
    groups_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("select group_id from Clubs order by group_id desc limit 1")
    new_id = cursor.fetchone()[0] + 1 if cursor.rowcount > 0 else 1
    while new_id in groups_ids:
        new_id += 1

    if new_id not in groups_ids:
        cursor.execute("insert into Clubs (group_id, group_name, num_members) values (%s, %s, 1)",
                       (new_id, group_name))
        command = "create table Group_%s(Member_username varchar(50) primary key, Member_name varchar(100))" % new_id
        cursor.execute(command)
        command = "INSERT INTO Group_%s (Member_username, Member_name) VALUES (%s, %s)"
        cursor.execute(command, (new_id, username, name))
        cursor.connection.commit()
        cursor.close()
        return True, "Group successfully created"
    else:
        cursor.close()
        return False, "Failed to create group"


#NOT IMPLEMENTED OR TESTED
def leave_group(mysql, headers, group_identifier):
    try:
        cursor = mysql.connection.cursor()

        # Retrieve username
        username = get_user(mysql, headers)

        # Retrieve display name
        command = "SELECT display_name FROM Users WHERE username = %s"
        cursor.execute(command, (username,))
        name = cursor.fetchone()
        if name:
            name = name[0]
        else:
            raise ValueError("User not found")

        # Check if the group identifier is a digit or a group name
        if group_identifier.isdigit():
            group_id = int(group_identifier)
            group_name_id = f'Group_{group_id}'
        else:
            # Retrieve group ID from Clubs table
            command = "SELECT group_id FROM Clubs WHERE group_name = %s"
            cursor.execute(command, (group_identifier,))
            group_id_result = cursor.fetchone()
            if group_id_result:
                group_id = group_id_result[0]
                group_name_id = f'Group_{group_id}'
            else:
                raise ValueError("Group does not exist. You must first create the group")

        # Check if the group exists
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        if group_name_id not in tables:
            raise ValueError("Group does not exist")

        # Retrieve current members of the group
        command = "SELECT Member_username FROM Group_%s" % group_id
        cursor.execute(command)
        current_members = [row[0] for row in cursor.fetchall()]

        # Check if the user is a member of the group
        if username in current_members:
            # Use parameterized queries to prevent SQL injection
            command = "DELETE FROM Group_%s WHERE Member_username = %s"
            cursor.execute(command, (group_id, username))

            command = "UPDATE Clubs SET num_members = num_members-1 WHERE group_id = %s"
            cursor.execute(command, (group_id,))

            cursor.connection.commit()
            return True, "Successfully left the group"
        else:
            raise ValueError("User is not a member of the group")
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()


#NOT IMPLEMENTED OR TESTED
#NEED TO FIGURE OUT WHO CAN DELETE GROUPS
def delete_group(mysql, headers):
    print("Help")

def display_groups(mysql, headers):
    cursor = mysql.connection.cursor()
    command = "select group_id, group_name, num_members from Clubs"
    cursor.execute(command)
    groups = cursor.fetchall()
    cursor.connection.commit()
    cursor.close()
    return groups


def get_group_members(mysql, group_id):
    cursor = mysql.connection.cursor()
    command = f"SELECT Member_username FROM Group_{group_id}"
    cursor.execute(command)
    members = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return members
