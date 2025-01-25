from voice import detect_blow


def blow_listener(player):
    while True:
        amplitude = detect_blow()
        if amplitude > 50000:
            player.acceleration_y -= 1
            player.acceleration_y = max(
                player.acceleration_y, player.min_acceleration_y
            )
        else:
            player.acceleration_y += player.gravity
            player.acceleration_y = min(
                player.acceleration_y, player.max_acceleration_y
            )
