from voice import detect_blow


def blow_listener(player):
    while True:
        amplitude = detect_blow()
        if amplitude > 80000:
            player.acceleration_y -= 3  # Decrease acceleration
        else:
            player.acceleration_y *= 0.9  # Apply damping

        if player.acceleration_y < -0.4:  # Threshold can be adjusted
            player.acceleration_y = abs(player.acceleration_y)
