import socket
import threading
import time

from common.constants import *
from common.protocol import encode, decode
from game.player import Player
from game.level import colliders, get_spawn
from game.collisions import move_and_collide

players = {}
clients = {}
next_id = 1


def handle_client(conn):
    global next_id

    pid = next_id
    next_id += 1

    x, y = get_spawn()
    player = Player(pid, x, y)

    players[pid] = player
    clients[conn] = pid

    conn.sendall(encode({"type": "welcome", "id": pid}))

    buffer = ""

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            buffer += data
            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                msg = decode(msg)

                if msg["type"] == "input":
                    player.apply_input(msg["mx"], msg["my"])

                    if msg["attack"] and player.can_attack():
                        player.do_attack()
                        check_attack(player)

        except:
            break

    del players[pid]
    del clients[conn]
    conn.close()


def check_attack(attacker):
    for p in players.values():
        if p.id == attacker.id or not p.alive:
            continue

        if attacker.rect.colliderect(
            p.rect.inflate(ATTACK_RANGE, ATTACK_RANGE)
        ):
            p.hp -= ATTACK_DAMAGE

            if p.hp <= 0:
                p.alive = False
                p.respawn_timer = time.time()


def update_world():
    for p in players.values():

        if p.alive:
            move_and_collide(p, colliders)
            p.update_state()

        else:
            if time.time() - p.respawn_timer >= RESPAWN_TIME:
                x, y = get_spawn()
                p.rect.topleft = (x, y)
                p.hp = MAX_HP
                p.alive = True


def snapshot():
    return {
        "type": "snapshot",
        "players": [
            {
                "id": p.id,
                "x": p.rect.x,
                "y": p.rect.y,
                "hp": p.hp,
                "alive": p.alive,
                "state": p.state,
            }
            for p in players.values()
        ],
    }


def server_loop():
    while True:
        update_world()
        snap = encode(snapshot())

        for conn in list(clients.keys()):
            try:
                conn.sendall(snap)
            except:
                pass

        time.sleep(1 / TICKRATE)


def run():
    print("SERVER STARTING...")
    s = socket.socket()
    s.bind(("127.0.0.1", 5000))
    s.listen()

    threading.Thread(target=server_loop, daemon=True).start()

    print("Server started")

    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    run()