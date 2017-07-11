import ccircle
import time

import config
from gameconfig import *
from boss import Boss
from player import Player

class State:
    def __init__(self):
        self._images = {}
        self._boss = Boss()
        self._players = {}
        self._next_id = 0
        self._font = ccircle.Font('../../res/FiraMono.ttf')
        self._get_player('133.0.242.0').name = 'XXXX'
        self._get_player('0.4124.33.1').name = 'Rakey'
        self._get_player('0.0.0.2').name = 'FmfoeifLAMzP'
        self._time = 0

    def _draw(self, window):
        sx, sy = window.getSize()
        self._get_image('background.jpg').draw(0, 0, sx, sy)

        self._boss.draw(self, window)
        for p in self._players.values():
            p.draw(self, window)

        window.drawRect(sx - 248, 0, 256, 72 + 16 * len(self._players), 0.2, 0.2, 0.2, 0.8)
        window.drawRect(sx - 240, 0, 240, 64 + 16 * len(self._players), 0.4, 0.4, 0.4, 0.8)
        self._font.draw('--- LEADERBOARD ---', sx - 220, 32, 16)
        y = 40
        for addr, player in self._players.items():
            y += 16
            self._font.draw('{} : {}'.format(addr, player.name), sx - 200, y, 12)

    def _get_image(self, name):
        image = self._images.get(name, None)
        if image: return image
        image = ccircle.Image('../image/%s' % name)
        self._images[name] = image
        return image

    def _get_player(self, addr):
        if addr in self._players:
            return self._players[addr]
        player = Player(self._next_id)
        self._players[addr] = player
        self._next_id += 1
        return player

    def _get_player_by_id(self, id):
        for player in self._players.values():
            if player.id == id:
                return player
        return None

    def _get_player_by_name(self, name):
        for player in self._players.values():
            if player.name == name:
                return player
        return None

    def _respond(self, client, msg_name, msg_data):
        if len(msg_name) == 0 or msg_name[0] == '_' or not hasattr(self, msg_name):
            return "'{}' is not a valid message name".format(msg_name)
        player = self._get_player(client)
        player.idle = 0
        result = getattr(self, msg_name)(player, msg_data if msg_data else None)
        return (result, None) if type(result) == str else result

    def _update(self, dt):
        self._time += dt
        self._boss.update(self, dt)

        remove_addrs = []
        for addr, player in self._players.items():
            player.update(self, dt)
            player.idle += dt
            if player.idle >= PLAYER_TIMEOUT:
                remove_addrs.append(addr)

        for addr in remove_addrs:
            self._players[addr] = None


    def get_boss_pos(self, player, args):
        return config.STATUS_GOOD, (self._boss.x, self._boss.y)

    def get_name(self, player, args):
        return config.STATUS_GOOD, player.name

    def get_player_ids(self, player, args):
        ids = [player.id for player in self._players.values()]
        return config.STATUS_GOOD, ids

    def get_player_pos(self, player, args):
        if not 'id' in args: return 'missing argument: id'
        other = self._get_player_by_id(args['id'])
        if not other: return 'no player with that ID'
        return config.STATUS_GOOD, (other.x, other.y)

    def get_player_velocity(self, player, args):
        if not 'id' in args: return 'missing argument: id'
        other = self._get_player_by_id(args['id'])
        if not other: return 'no player with that ID'
        return config.STATUS_GOOD, (other.vx, other.vy)

    def get_pos(self, player, args):
        return config.STATUS_GOOD, (player.x, player.y)

    def get_velocity(self, player, args):
        return config.STATUS_GOOD, (player.vx, player.vy)

    def set_color(self, player, args):
        if not 'r' in args: return 'missing argument: r'
        if not 'g' in args: return 'missing argument: g'
        if not 'b' in args: return 'missing argument: b'
        r = args['r']
        g = args['g']
        b = args['b']
        if type(r) not in (int, float): return 'r must be numeric'
        if type(g) not in (int, float): return 'g must be numeric'
        if type(b) not in (int, float): return 'b must be numeric'
        r = max(0.0, min(1.0, r))
        g = max(0.0, min(1.0, g))
        b = max(0.0, min(1.0, b))
        player.color = (r, g, b)
        return config.STATUS_GOOD

    def set_name(self, player, args):
        if not 'name' in args: return 'missing argument: name'
        name = args['name']
        if len(name) < NAME_LEN_MIN:
            return 'name is too short ({} chars min)'.format(NAME_LEN_MIN)
        if len(name) > NAME_LEN_MAX:
            return 'name is too long ({} chars max)'.format(NAME_LEN_MAX)

        for c in name:
            if not c in NAME_VALID_CHARS:
                return 'name contains invalid characters'

        if player.name == name:
            return config.STATUS_GOOD

        other = self._get_player_by_name(name)
        if other: return 'name is already taken'
        player.name = name
        return config.STATUS_GOOD

    def set_velocity(self, player, args):
        if not 'vx' in args: return 'missing argument: vx'
        if not 'vy' in args: return 'missing argument: vy'
        vx = args['vx']
        vy = args['vy']
        if type(vx) not in (int, float): return 'vx must be numeric'
        if type(vy) not in (int, float): return 'vy must be numeric'
        if max(abs(vx), abs(vy)) > SPEED_MAX:
            return 'velocity exceeds the speed limit ({})'.format(SPEED_MAX)
        player.vx = vx
        player.vy = vy
        return config.STATUS_GOOD
