import pygame
import socket
import threading

from common.constants import *
from common.protocol import encode, decode

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

players = {}
my_id = None


def receive(sock):
    global players
    buffer = ""

    while True:
        data = sock.recv(1024).decode()
        if not data:
            break

        buffer += data

        while "\n" in buffer:
            msg, buffer = buffer.split("\n", 1)
            msg = decode(msg)

            if msg["type"] == "welcome":
                global my_id
                my_id = msg["id"]

            elif msg["type"] == "snapshot":
                players = {p["id"]: p for p in msg["players"]}


def run():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 5000))

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    running = True

    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        mx = keys[pygame.K_d] - keys[pygame.K_a]
        my = keys[pygame.K_s] - keys[pygame.K_w]
        attack = keys[pygame.K_SPACE]

        sock.sendall(
            encode({
                "type": "input",
                "mx": mx,
                "my": my,
                "attack": attack
            })
        )

        screen.fill((30, 30, 30))

        for p in players.values():
            color = (0, 255, 0) if p["id"] == my_id else (255, 0, 0)
            pygame.draw.rect(screen, color,
                             (p["x"], p["y"], 40, 40))

            hp_text = pygame.font.SysFont(None, 20).render(
                str(p["hp"]), True, (255, 255, 255)
            )
            screen.blit(hp_text, (p["x"], p["y"] - 15))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()