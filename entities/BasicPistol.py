from entities.Bullet import Bullet


class BasicPistol:
    MAGAZINE_SIZE = 17
    FIRE_RATE = 3  # bullets per second
    RELOAD_TIME = 3
    DAMAGE = 40

    def __init__(self, bullet_group):
        self.bullet_group = bullet_group
        self.bullets_remaining = self.MAGAZINE_SIZE
        self.reload_timer = 0
        self.reloading = False
        self.fire_rate_timer = 0
        self.ready_to_fire = True

    def reload(self):
        self.bullets_remaining = 0
        self.reloading = True

    def update(self, dt):
        # chamber the next bullet
        if not self.ready_to_fire:
            self.fire_rate_timer += dt
            if self.fire_rate_timer > (1 / self.FIRE_RATE):
                self.fire_rate_timer = 0
                self.ready_to_fire = True

        # reload the magazine
        if self.reloading:
            self.reload_timer += dt
            if self.reload_timer > self.RELOAD_TIME:
                self.reload_timer = 0
                self.reloading = False
                self.bullets_remaining = self.MAGAZINE_SIZE

    def fire(self, pos, vel):
        if self.ready_to_fire:
            self.ready_to_fire = False
        else:
            return
        # create the bullet entity
        bullet = Bullet(pos, vel)
        self.bullet_group.add(bullet)

        self.bullets_remaining -= 1
        if self.bullets_remaining < 1 and not self.reloading:
            self.reload()
