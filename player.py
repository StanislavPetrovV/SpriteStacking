from settings import *
import math
from entity import BaseEntity
from bullet import Bullet


class Player(BaseEntity):
    def __init__(self, app, name='player'):
        super().__init__(app, name)
        self.group.change_layer(self, CENTER.y)

        self.rect = self.image.get_rect(center=CENTER)

        self.offset = vec2(0)
        self.inc = vec2(0)
        self.prev_inc = vec2(0)
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt(2)

    def control(self):
        self.inc = vec2(0)
        speed = PLAYER_SPEED * self.app.delta_time
        rot_speed = PLAYER_ROT_SPEED * self.app.delta_time

        key_state = pg.key.get_pressed()

        if key_state[pg.K_LEFT]:
            self.angle += rot_speed
        if key_state[pg.K_RIGHT]:
            self.angle -= rot_speed

        if key_state[pg.K_w]:
            self.inc += vec2(0, -speed).rotate_rad(-self.angle)
        if key_state[pg.K_s]:
            self.inc += vec2(0, speed).rotate_rad(-self.angle)
        if key_state[pg.K_a]:
            self.inc += vec2(-speed, 0).rotate_rad(-self.angle)
        if key_state[pg.K_d]:
            self.inc += vec2(speed, 0).rotate_rad(-self.angle)

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr

    def single_fire(self, event):
        if event.key == pg.K_UP:
            Bullet(app=self.app)

    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.app.collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask)
        if not hit:
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            self.inc = -self.prev_inc

    def update(self):
        super().update()
        self.control()
        self.check_collision()
        self.move()

    def move(self):
        self.offset += self.inc
















