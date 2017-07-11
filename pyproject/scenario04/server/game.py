import ccircle
import random

import config
import util
import hashlib

from gameconfig import *
from boss import Boss
from player import Player
from reward import Reward

class State:
    def __init__(self, size):
        self._sx, self._sy = size
        self._reset()

        if DEBUG_MODE:
            p0 = self._get_player('133.0.242.0'); p0.name = 'beep'
            p1 = self._get_player('0.4124.33.1'); p1.name = 'boop'
            p2 = self._get_player('12.0.9.1'); p2.name = 'zooooom'
            p2.money = 1337
            p1.money = 50
            p0.money = 0
            p0.vx = 100
            p0.vy = 100

    def _draw(self, window):
        sx, sy = window.getSize()
        util.image('background.jpg').draw(0, 0, sx, sy)
        for obj in self._rewards:
            obj.draw(self, window)

        self._boss.draw(self, window)
        for p in self._players.values():
            p.draw(self, window)

        window.drawRect(sx - 248, 0, 256, 72 + 16 * len(self._players), 0.2, 0.2, 0.2, 0.8)
        window.drawRect(sx - 240, 0, 240, 64 + 16 * len(self._players), 0.4, 0.4, 0.4, 0.8)
        util.font().draw('--- PLAYERS ---', sx - 220, 32, 16)
        y = 40
        for player in sorted(self._players.values(), key=lambda x: -x.money):
            y += 16
            util.font().draw('${} : {}'.format(player.money, player.name), sx - 200, y, 12)

        if self._boss.dead:
          s = min(self._sx, self._sy)
          window.drawRect(0, 0, self._sx, self._sy, 0.1, 0.1, 0.1, 0.9)
          window.drawRect((self._sx - s) / 2 - 16, 0, s + 32, s, 0.2, random.uniform(0, 1), 0.2)
          util.draw_image_centered('win.bin', self._sx / 2, self._sy / 2, s - 16)

    def _gen_reward(self):
        reward = Reward(
            self._next_id,
            random.randint(0, self._sx),
            random.randint(0, self._sy))
        self._rewards.append(reward)
        self._next_id += 1

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

    def _reset(self):
        self._boss = Boss()
        self._rewards = []
        self._players = {}
        self._next_id = 0

        self._time = 0.0
        self._reset_time = 1e30

        for i in range(REWARD_COUNT):
          self._gen_reward()


    def _respond(self, client, msg_name, msg_data):
        if len(msg_name) == 0 or msg_name[0] == '_' or not hasattr(self, msg_name):
            return "'{}' is not a valid message name".format(msg_name)
        player = self._get_player(client)
        player.idle = 0
        result = getattr(self, msg_name)(player, msg_data if msg_data else None)
        return (result, None) if type(result) == str else result

    def _update(self, dt):
        self._time += dt
        if self._time >= self._reset_time:
            self._reset()

        # Update boss
        if not self._boss.dead:
            self._boss.update(self, dt)
            if self._boss.dead:
                print('The boss is dead! Reset time is now: {}'.format(self._reset_time))
                self._reset_time = self._time + 10.0

        remove_list = []
        for obj in self._rewards:
            obj.update(self, dt)
            if obj.remove:
              remove_list.append(obj)
        for obj in remove_list:
            self._rewards.remove(obj)
        while len(self._rewards) < REWARD_COUNT:
            self._gen_reward()

        # Update players
        remove_list = []
        for addr, player in self._players.items():
            player.update(self, dt)
            player.idle += dt
            if player.idle >= PLAYER_TIMEOUT:
                remove_list.append(addr)

        # Remove players that exceed the idle timeout
        for addr in remove_list:
            del self._players[addr]

    def _adm_auth(self, args):
        if not 'key' in args: return 'missing argument: key'
        key = args['key']
        if type(key) != str: return 'key must be a string...are you really an admin?'
        h = hashlib.sha256(bytes(key, 'utf-8')).hexdigest()
        if h != ADMIN_KEY_HASH: return 'admin key is incorrect'
        return True

    def adm_enable_ai(self, player, args):
        result = self._adm_auth(args)
        if type(result) == str: return result
        if not 'enabled' in args: return 'missing argument: enabled'
        enabled = args['enabled']
        if type(enabled) != bool: return 'enabled must be a bool'
        self._boss.enable_ai = enabled
        return config.STATUS_GOOD

    def adm_money(self, player, args):
        result = self._adm_auth(args)
        if type(result) == str: return result
        if not 'amount' in args: return 'missing argument: amount'
        amount = args['amount']
        if type(amount) != int: return 'amount must be an int'
        if amount < 0: return 'amount must be non-negative'
        player.money = amount
        return config.STATUS_GOOD

    def adm_set_boss_velocity(self, player, args):
        if not 'vx' in args: return 'missing argument: vx'
        if not 'vy' in args: return 'missing argument: vy'
        vx = args['vx']
        vy = args['vy']
        if type(vx) not in (int, float): return 'vx must be numeric'
        if type(vy) not in (int, float): return 'vy must be numeric'
        self._boss.vx = vx
        self._boss.vy = vy
        return config.STATUS_GOOD

    def damage_boss(self, player, args):
        if player.money < BOSS_DAMAGE_MONEY:
            return 'you need at least ${} to damage the boss'.format(BOSS_DAMAGE_MONEY)
        player.money -= BOSS_DAMAGE_MONEY
        self._boss.health -= BOSS_DAMAGE_AMOUNT
        return config.STATUS_GOOD

    def get_boss_health(self, player, args):
        return config.STATUS_GOOD, self._boss.health

    def get_boss_pos(self, player, args):
        return config.STATUS_GOOD, (self._boss.x, self._boss.y)

    def get_money(self, player, args):
        return config.STATUS_GOOD, player.money

    def get_name(self, player, args):
        return config.STATUS_GOOD, player.name

    def get_player_id_by_name(self, player, args):
        if not 'name' in args: return 'missing argument: name'
        name = args['name']
        if type(name) != str: return 'name must be a string'
        player = self._get_player_by_name(name)
        if not player: return 'no player with that name'
        return config.STATUS_GOOD, player.id

    def get_player_ids(self, player, args):
        ids = [x.id for x in self._players.values()]
        return config.STATUS_GOOD, ids

    def get_player_pos(self, player, args):
        if not 'id' in args: return 'missing argument: id'
        other = self._get_player_by_id(args['id'])
        if not other: return 'no player with that id'
        return config.STATUS_GOOD, (other.x, other.y)

    def get_pos(self, player, args):
        return config.STATUS_GOOD, (player.x, player.y)

    def get_reward_ids(self, player, args):
        ids = [x.id for x in self._rewards]
        return config.STATUS_GOOD, ids

    def get_reward_pos(self, player, args):
        if not 'id' in args: return 'missing argument: id'
        reward = None
        for obj in self._rewards:
          if obj.id == args['id']:
            reward = obj
            break
        if not reward: return 'no reward with that id'
        return config.STATUS_GOOD, (reward.x, reward.y)

    def get_velocity(self, player, args):
        return config.STATUS_GOOD, (player.vx, player.vy)

    def send_money(self, player, args):
        if not 'id' in args: return 'missing argument: id'
        if not 'amount' in args: return 'missing argument: amount'
        other = self._get_player_by_id(args['id'])
        if not other: return 'no player with that id'
        if other == player: return 'cannot send money to yourself'
        amount = args['amount']
        if type(amount) != int: return 'amount must be an integer'
        if amount <= 0: return 'amount must be positive'
        if amount > player.money: return 'cannot send more money than you have'

        player.money -= amount
        other.money += amount
        return config.STATUS_GOOD

    def _set_color(self, player, args):
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
