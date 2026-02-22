from common.constants import WIDTH, HEIGHT

def move_and_collide(player, colliders):
    # X
    player.rect.x += player.vx

    for c in colliders:
        if player.rect.colliderect(c):
            if player.vx > 0:
                player.rect.right = c.left
            elif player.vx < 0:
                player.rect.left = c.right

    # Y
    player.rect.y += player.vy

    for c in colliders:
        if player.rect.colliderect(c):
            if player.vy > 0:
                player.rect.bottom = c.top
            elif player.vy < 0:
                player.rect.top = c.bottom

    # Межі сцени
    player.rect.x = max(0, min(player.rect.x, WIDTH - player.rect.width))
    player.rect.y = max(0, min(player.rect.y, HEIGHT - player.rect.height))