--- CONNECTION OBJECT --------------------------------------------------------------------------------------------------

    connection.create() returns a connection object that you can use to send/receive messages to/from the game server

    The connection object has only one function of interest: .send.

        con.send( message_name [, message_data ]) -> Object

            Send a message to the game server. The return value depends on the message sent.

            message_name
                A string that identifies the type of message you're sending ot the server. You can see a full list
                of supported messages, along with their purpose and the data they take in / return out below

            message_data
                A dictionary of key, value pairs. The keys and values you provide will depend on the message that
                you're sending. Some messages don't require any data (like 'get_pos'), in which case you do not have
                to supply this argument at all.

    Example Usage:

        con.send('set_name', { 'name'='SuperJosh' })

            Sends a 'set_name' message to the server with one key-value pair: ('name', 'SuperJosh')

    Most of the functionality in your program will be sending messages to the server and interpreting the response.

--- GAME SERVER MESSAGES -----------------------------------------------------------------------------------------------

    Below you can find a list of all messages supported by the game server, what they do, the data (if any) that they
    expect you to provide, and the data (if any) that they return.

    get_boss_pos () -> (x, y)
        Returns a tuple that gives the current coordinates of the boss

    get_name () -> str
        Returns your player's current name

    get_player_ids () -> list of player identifiers (ints)
        Returns a complete list of every player in the game (players are represented by a numeric id)

    get_pos () -> (x, y)
        Returns a tuple that gives the current coordinates of yourself

    get_reward_ids () -> list of ids
        Returns a list of the id of every

    get_reward_pos (id) -> (x, y)
        Returns the position of the reward with the given id

    set_velocity (vx, vy) -> None
        Sets your velocity to (vx, vy)

------------------------------------------------------------------------------------------------------------------------