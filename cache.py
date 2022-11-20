from settings import *


class Cache:
    def __init__(self):
        self.stacked_sprite_cache = {}
        self.entity_sprite_cache = {}
        self.viewing_angle = 360 // NUM_ANGLES
        self.outline_thickness = 5
        self.alpha_value = 70  #
        self.get_stacked_sprite_cache()
        self.get_entity_sprite_cache()

    def get_entity_sprite_cache(self):
        for sprite_name in ENTITY_SPRITE_ATTRS:
            self.entity_sprite_cache[sprite_name] = {
                'images': None
            }
            attrs = ENTITY_SPRITE_ATTRS[sprite_name]
            images = self.get_layer_array(attrs)
            self.entity_sprite_cache[sprite_name]['images'] = images

            mask = self.get_entity_mask(attrs, images)
            self.entity_sprite_cache[sprite_name]['mask'] = mask

    def get_entity_mask(self, attrs, images):
        path = attrs.get('mask_path', False)
        if not path:
            return pg.mask.from_surface(images[0])
        else:
            scale = attrs['scale']
            mask_image = pg.image.load(path).convert_alpha()
            mask_image = pg.transform.scale(mask_image, vec2(mask_image.get_size()) * scale)
            return pg.mask.from_surface(mask_image)

    def get_stacked_sprite_cache(self):
        for obj_name in STACKED_SPRITE_ATTRS:
            self.stacked_sprite_cache[obj_name] = {
                'rotated_sprites': {},
                'alpha_sprites': {},
                'collision_masks': {}
            }
            attrs = STACKED_SPRITE_ATTRS[obj_name]
            layer_array = self.get_layer_array(attrs)
            self.run_prerender(obj_name, layer_array, attrs)

    def run_prerender(self, obj_name, layer_array, attrs):
        outline = attrs.get('outline', True)
        transparency = attrs.get('transparency', False)
        mask_layer = attrs.get('mask_layer', attrs['num_layers'] // 2)

        for angle in range(NUM_ANGLES):
            surf = pg.Surface(layer_array[0].get_size())
            surf = pg.transform.rotate(surf, angle * self.viewing_angle)
            sprite_surf = pg.Surface([surf.get_width(), surf.get_height()
                                      + attrs['num_layers'] * attrs['scale']])
            sprite_surf.fill('khaki')
            sprite_surf.set_colorkey('khaki')

            for ind, layer in enumerate(layer_array):
                layer = pg.transform.rotate(layer, angle * self.viewing_angle)
                sprite_surf.blit(layer, (0, ind * attrs['scale']))

                # get collision mask
                if ind == mask_layer:
                    surf = pg.transform.flip(sprite_surf, True, True)
                    mask = pg.mask.from_surface(surf)
                    self.stacked_sprite_cache[obj_name]['collision_masks'][angle] = mask

            # get outline
            if outline:
                outline_coords = pg.mask.from_surface(sprite_surf).outline()
                pg.draw.polygon(sprite_surf, 'black', outline_coords, self.outline_thickness)

            # get alpha sprites
            if transparency:  #
                alpha_sprite = sprite_surf.copy()
                alpha_sprite.set_alpha(self.alpha_value)
                alpha_sprite = pg.transform.flip(alpha_sprite, True, True)
                self.stacked_sprite_cache[obj_name]['alpha_sprites'][angle] = alpha_sprite

            image = pg.transform.flip(sprite_surf, True, True)
            self.stacked_sprite_cache[obj_name]['rotated_sprites'][angle] = image



    def get_layer_array(self, attrs):
        # load sprite sheet
        sprite_sheet = pg.image.load(attrs['path']).convert_alpha()
        # scaling
        sprite_sheet = pg.transform.scale(sprite_sheet,
                                          vec2(sprite_sheet.get_size()) * attrs['scale'])
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        sprite_height = sheet_height // attrs['num_layers']
        # new height to prevent error
        sheet_height = sprite_height * attrs['num_layers']
        # get sprites
        layer_array = []
        for y in range(0, sheet_height, sprite_height):
            sprite = sprite_sheet.subsurface((0, y, sheet_width, sprite_height))
            layer_array.append(sprite)
        return layer_array[::-1]