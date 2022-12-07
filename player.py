from typing import Callable, Dict, List, Tuple, cast

import pygame

from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int],
                 surface: pygame.Surface,
                 create_jump_particles: Callable) -> None:
        super().__init__()
        self.import_character_assets()
        self.fram_index = 0
        self.animation_speed = 0.15
        self.image: pygame.Surface = self.animations['idle'][self.fram_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_fram_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self) -> None:
        character_path = './graphics/character/'
        self.animations: Dict[str, List[pygame.Surface]] = {
            'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self) -> None:
        self.dust_run_particles = import_folder(
            './graphics/character/dust_particles/run')

    def animate(self) -> None:
        animation = self.animations[self.status]

        # loop over fram index
        self.fram_index += self.animation_speed
        if self.fram_index >= len(animation):
            self.fram_index = 0

        image = animation[int(self.fram_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            flipped_image = cast(pygame.Surface, flipped_image)
            # second value is x and third is y
            self.image = flipped_image

        # set the rect
        if self.rect is None:
            ...
        elif self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def run_dust_animation(self) -> None:
        if self.status == 'run' and self.on_ground:
            self.dust_fram_index += self.dust_animation_speed
            if self.dust_fram_index >= len(self.dust_run_particles):
                self.dust_fram_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_fram_index)]

            if self.facing_right:
                pos = (self.rect.bottomleft  # type: ignore
                       - pygame.math.Vector2(6, 10))
                self.display_surface.blit(dust_particle, pos)

            else:
                pos = (self.rect.bottomright  # type: ignore
                       - pygame.math.Vector2(6, 10))
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:  # player will not double jump
            self.jump()
            self.create_jump_particles(self.rect.midbottom)  # type: ignore

    def get_status(self) -> None:
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self) -> None:
        self.direction.y += self.gravity
        self.rect.y += self.direction.y  # type: ignore

    def jump(self) -> None:
        self.direction.y = self.jump_speed

    def update(self) -> None:
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
