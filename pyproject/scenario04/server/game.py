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
        self.sx, self.sy = size
        self.reset()

        if DEBUG_MODE:
            p0 = self.get_player('133.0.242.0'); p0.name = 'beep'
            p1 = self.get_player('0.4124.33.1'); p1.name = 'boop'
            p2 = self.get_player('12.0.9.1'); p2.name = 'zooooom'
            p2.money = 1337
            p1.money = 50
            p0.money = 0
            p0.vx = 100
            p0.vy = 100

    def draw(self, window):
        sx, sy = window.getSize()
        util.image('background.jpg').draw(0, 0, sx, sy)
        for obj in self.rewards:
            obj.draw(self, window)

        self.boss.draw(self, window)
        for obj in self.players.values():
            obj.draw(self, window)


        window.drawRect(sx - 248, 0, 256, 72 + 16 * len(self.players), 0.2, 0.2, 0.2, 0.5)
        window.drawRect(sx - 240, 0, 240, 64 + 16 * len(self.players), 0.4, 0.4, 0.4, 0.5)
        util.font().draw('--- PLAYERS (%d) ---' % len(self.players), sx - 220, 32, 16)
        y = 40
        for player in sorted(self.players.values(), key=lambda x: -x.money):
            y += 16
            util.font().draw('${} : {}'.format(player.money, player.name), sx - 200, y, 12)

        if self.boss.dead:
          s = min(self.sx, self.sy)
          window.drawRect(0, 0, self.sx, self.sy, 0.1, 0.1, 0.1, 0.9)
          window.drawRect((self.sx - s) / 2 - 16, 0, s + 32, s, 0.2, random.uniform(0, 1), 0.2)
          util.draw_image_centered('win.bin', self.sx / 2, self.sy / 2, s - 16)

    def gen_reward(self):
        reward = Reward(
            self.next_id,
            random.randint(0, self.sx),
            random.randint(0, self.sy))
        self.rewards.append(reward)
        self.next_id += 1

    def get_reward_by_id(self, id):
        for obj in self.rewards:
            if obj.id == id:
                return obj
        return None

    def get_player(self, addr):
        if addr in self.players:
            return self.players[addr]
        player = Player(self.next_id)
        self.players[addr] = player
        self.next_id += 1
        return player

    def get_player_by_id(self, id):
        for player in self.players.values():
            if player.id == id:
                return player
        return None

    def get_player_by_name(self, name):
        for player in self.players.values():
            if player.name == name:
                return player
        return None

    def reset(self):
        self.boss = Boss()
        self.rewards = []
        self.players = {}
        self.next_id = 0

        self.time = 0.0
        self.reset_time = 1e30

        for i in range(REWARD_COUNT):
          self.gen_reward()

    def update(self, dt):
        self.time += dt
        if self.time >= self.reset_time:
            self.reset()

        # Update boss
        if not self.boss.dead:
            self.boss.update(self, dt)
            if self.boss.dead:
                print('The boss is dead! Reset time is: {}'.format(self.reset_time))
                self.reset_time = self.time + 10.0

        remove_list = []
        for obj in self.rewards:
            obj.update(self, dt)
            if obj.remove:
              remove_list.append(obj)
        for obj in remove_list:
            self.rewards.remove(obj)
        while len(self.rewards) < REWARD_COUNT:
            self.gen_reward()

        # Update players
        remove_list = []
        for addr, player in self.players.items():
            player.update(self, dt)
            player.idle += dt
            if player.idle >= PLAYER_TIMEOUT:
                remove_list.append(addr)

        # Remove players that exceed the idle timeout
        for addr in remove_list:
            del self.players[addr]

class MessageFn:
    def __init__(self, *params):
        self.params = params if params != None else []

    def __call__(self, fn):
        def impl(handler, player, args):
            extracted = []
            for tp, name in self.params:
                if not name in args: return 'missing argument: %s' % name
                arg = args[name]
                if type(arg) != tp:
                  return '%s must have type %s' % (name, str(tp))
                extracted.append(arg)
            if len(extracted) > 0:
              return fn(handler, player, *extracted)
            else:
              return fn(handler, player)
        return impl

class MessageHandler:
    def __init__(self, game):
        self.game = game

    def _respond(self, client, msg_name, msg_data):
        if len(msg_name) == 0 or msg_name[0] == '_' or not hasattr(self, msg_name):
            return "'{}' is not a valid message name".format(msg_name)
        player = self.game.get_player(client)
        player.idle = 0
        result = getattr(self, msg_name)(player, msg_data if msg_data else {})
        return (result, None) if type(result) == str else result

    def _adm_auth(self, args):
        if not 'key' in args: return 'missing argument: key'
        key = args['key']
        if type(key) != str: return 'key must be a string...are you really an admin?'
        h = hashlib.sha256(bytes(key, 'utf-8')).hexdigest()
        if h != ADMIN_KEY_HASH: return 'admin key is incorrect'
        return True

    def adm_add_money(self, player, args):
        result = self._adm_auth(args)
        if type(result) == str: return result

        if not 'amount' in args: return 'missing argument: amount'
        amount = args['amount']
        if type(amount) != int: return 'amount must be an int'
        if amount <= 0: return 'amount must be positive'
        player.money += amount
        return config.STATUS_GOOD

    def adm_enable_ai(self, player, args):
        result = self._adm_auth(args)
        if type(result) == str: return result

        if not 'enabled' in args: return 'missing argument: enabled'
        enabled = args['enabled']
        if type(enabled) != bool: return 'enabled must be a bool'
        self.game.boss.enable_ai = enabled
        return config.STATUS_GOOD

    def adm_set_boss_velocity(self, player, args):
        result = self._adm_auth(args)
        if type(result) == str: return result

        if not 'vx' in args: return 'missing argument: vx'
        if not 'vy' in args: return 'missing argument: vy'
        vx = args['vx']
        vy = args['vy']
        if type(vx) not in (int, float): return 'vx must be numeric'
        if type(vy) not in (int, float): return 'vy must be numeric'
        self.game.boss.vx = vx
        self.game.boss.vy = vy
        return config.STATUS_GOOD

    @MessageFn()
    def damage_boss(self, player):
        if player.money < BOSS_DAMAGE_MONEY:
            return 'you need at least ${} to damage the boss'.format(BOSS_DAMAGE_MONEY)
        player.money -= BOSS_DAMAGE_MONEY
        self.game.boss.health -= BOSS_DAMAGE_AMOUNT
        return config.STATUS_GOOD

    @MessageFn()
    def get_boss_health(self, player):
        return config.STATUS_GOOD, self.game.boss.health

    @MessageFn()
    def get_boss_pos(self, player):
        return config.STATUS_GOOD, (self.game.boss.x, self.game.boss.y)

    @MessageFn()
    def get_money(self, player):
        return config.STATUS_GOOD, player.money

    @MessageFn()
    def get_name(self, player):
        return config.STATUS_GOOD, player.name

    @MessageFn((str, 'name'))
    def get_player_id_by_name(self, player, name):
        player = self.game.get_player_by_name(name)
        if not player: return 'no player with that name'
        return config.STATUS_GOOD, player.id

    @MessageFn()
    def get_player_ids(self, player):
        # TODO: Efficiency
        ids = [x.id for x in self.game.players.values()]
        return config.STATUS_GOOD, ids

    @MessageFn((int, 'id'))
    def get_player_pos(self, player, id):
        other = self.game.get_player_by_id(id)
        if not other: return 'no player with that id'
        return config.STATUS_GOOD, (other.x, other.y)

    @MessageFn()
    def get_pos(self, player):
        return config.STATUS_GOOD, (player.x, player.y)

    @MessageFn()
    def get_reward_ids(self, player):
        ids = [x.id for x in self.game.rewards]
        return config.STATUS_GOOD, ids

    @MessageFn((int, 'id'))
    def get_reward_pos(self, player, id):
        # TODO: Efficiency
        reward = self.game.get_reward_by_id(id)
        if not reward: return 'no reward with that id'
        return config.STATUS_GOOD, (reward.x, reward.y)

    @MessageFn()
    def get_velocity(self, player, args):
        return config.STATUS_GOOD, (player.vx, player.vy)

    @MessageFn((int, 'id'), (int, 'amount'))
    def send_money(self, player, id, amount):
        other = self.game.get_player_by_id(id)
        if not other: return 'no player with that id'
        if other == player: return 'cannot send money to yourself'
        if amount > player.money: return 'cannot send more money than you have'
        if amount <= 0: return 'amount must be positive'

        player.money -= amount
        other.money += amount
        return config.STATUS_GOOD

    @MessageFn((str, 'name'))
    def set_name(self, player, name):
        if len(name) < NAME_LEN_MIN:
            return 'name is too short ({} chars min)'.format(NAME_LEN_MIN)
        if len(name) > NAME_LEN_MAX:
            return 'name is too long ({} chars max)'.format(NAME_LEN_MAX)

        for c in name:
            if not c in NAME_VALID_CHARS:
                return 'name contains invalid characters'

        if player.name == name:
            return config.STATUS_GOOD

        other = self.game.get_player_by_name(name)
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
