from settings import *


class BaseEntity(pg.sprite.Sprite):
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.group = app.main_group
        super().__init__(self.group)

        self.attrs = ENTITY_SPRITE_ATTRS[name]
        entity_cache = self.app.cache.entity_sprite_cache
        self.images = entity_cache[name]['images']
        self.image = self.images[0]
        self.mask = entity_cache[name]['mask']
        self.rect = self.image.get_rect()
        self.frame_index = 0

    def animate(self):
        if self.app.anim_trigger:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]

    def update(self):
        self.animate()


class Entity(BaseEntity):
    def __init__(self, app, name, pos):
        super().__init__(app, name)
        self.pos = vec2(pos) * TILE_SIZE
        self.player = app.player
        self.y_offset = vec2(0, self.attrs['y_offset'])
        self.screen_pos = vec2(0)

    def update(self):
        super().update()
        self.transform()
        self.set_rect()
        self.change_layer()

    def transform(self):
        pos = self.pos - self.player.offset
        pos = pos.rotate_rad(self.player.angle)
        self.screen_pos = pos + CENTER

    def change_layer(self):
        self.group.change_layer(self, self.screen_pos.y)

    def set_rect(self):
        self.rect.center = self.screen_pos + self.y_offset


















