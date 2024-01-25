import pygame
import random
from pygame import *


class GameManager:
    class Moles:
        def __init__(self, mole, hole_num):
            self.mole = mole
            self.hole_num = hole_num
            self.is_down = False
            self.num = -1
            self.left = 0
            self.interval = 0.1
            self.cycle_time = 0
            self.last_time = 0
    def __init__(self):
        # Define constants
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 735
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whack A Mole - Game Programming - Assignment 1"
        self.timer = 90
        # Game states
        self.START_SCREEN = 0
        self.GAME_RUNNING = 1
        self.END_SCREEN = 2
        self.current_state = self.START_SCREEN
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/bg.png")
        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', self.FONT_SIZE)
        # Initialize the mole's sprite sheet
        # 6 different states
        sprite_sheet = pygame.image.load("images/mole.png")
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((40, 210))
        self.hole_positions.append((180, 210))
        self.hole_positions.append((300, 210))
        self.hole_positions.append((420, 210))
        self.hole_positions.append((40, 330))
        self.hole_positions.append((180, 330))
        self.hole_positions.append((300, 330))
        self.hole_positions.append((420, 330))
        self.hole_positions.append((40, 440))
        self.hole_positions.append((180, 440))
        self.hole_positions.append((300, 440))
        self.hole_positions.append((420, 440))
        self.hole_positions.append((570, 210))
        self.hole_positions.append((570, 330))
        self.hole_positions.append((570, 440))
        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    # Check whether the mouse click hit the mole or not
    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        else:
            return False

    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (0, 0, 0))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.background.get_rect().centerx
        score_text_pos.centery = self.SCREEN_HEIGHT - self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # # Update the player's misses
        # current_misses_string = "MISSES: " + str(self.misses)
        # misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        # misses_text_pos = misses_text.get_rect()
        # misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        # misses_text_pos.centery = self.FONT_TOP_MARGIN
        # self.screen.blit(misses_text, misses_text_pos)
        # Update the player's level
        current_level_string = "LEVEL: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (0, 0, 0))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1
        level_text_pos.centery = self.SCREEN_HEIGHT - self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)
        # Update the timer
        current_timer_string = "TIME: " + str(self.timer)
        timer_text = self.font_obj.render(current_timer_string, True, (0, 0, 0))
        timer_text_pos = timer_text.get_rect()
        timer_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        timer_text_pos.centery = self.SCREEN_HEIGHT - self.FONT_TOP_MARGIN
        self.screen.blit(timer_text, timer_text_pos)


    # Start the game's main loop
    # Contains some logic for handling animations, mole hit events, etc..
    def game_loop(self):
        loop = True
        initial_interval = 1
        num_moles = 3
        hole_nums = random.sample(range(-1, 15), num_moles)
        used_hole_nums = hole_nums
        Moles = []
        for hole_num in hole_nums:
            Moles.append(self.Moles(self.mole, hole_num))
        for Mole in Moles:
            Mole.last_time = pygame.time.get_ticks()
        left = 0
        # Time control variables
        clock = pygame.time.Clock()
        # Initialize timer variables
        start_time = pygame.time.get_ticks()
        timer_limit = 60  # 90 seconds
        self.timer = timer_limit
        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    self.soundEffect.playFire()
                    for Mole in Moles:
                        if (Mole.hole_num < 0): Mole.hole_num = random.randint(0, 14)
                        if self.is_mole_hit(mouse.get_pos(), self.hole_positions[Mole.hole_num]) and Mole.num > 0 and Mole.left == 0:
                            Mole.num = 3
                            Mole.left = 14
                            Mole.is_down = False
                            Mole.interval = 0
                            self.score += 1  # Increase player's score
                            self.level = self.get_player_level()  # Calculate player's level
                            # Stop popping sound effect
                            self.soundEffect.stopPop()
                            # Play hurt sound
                            self.soundEffect.playHurt()
                            self.update()
                        else:
                            self.misses += 1 
                            self.update()   
            for Mole in Moles:  
                if (Mole.hole_num < 0): Mole.hole_num = random.randint(0, 14)
                current_time = pygame.time.get_ticks()
                sec = (current_time - Mole.last_time) / 1000.0
                Mole.last_time = pygame.time.get_ticks()
                # if Mole.num > 5:
                #     self.screen.blit(self.background, (0, 0))
                #     self.update()
                #     Mole.num = -1
                #     Mole.left = 0
                # if Mole.num == -1:
                #     self.screen.blit(self.background, (0, 0))
                #     self.update()
                #     Mole.num = 0
                #     Mole.is_down = False
                #     Mole.interval = 0.5
                #     Mole.hole_num = random.randint(-1, 14)
                Mole.cycle_time += sec
                if (Mole.cycle_time > Mole.interval):
                    self.screen.blit(self.background, (0, 0))
                    for Mole_ in Moles:
                        if Mole_.num > 5:
                            self.update()
                            Mole_.num = -1
                            Mole.left = 0
                        if Mole_.num == -1:
                            self.update()
                            Mole_.num = 0
                            Mole_.is_down = False
                            Mole_.interval = 0.5
                            # Random in hole not in used_hole_nums
                            used_hole_nums.remove(Mole_.hole_num)
                            Mole_.hole_num = random.choice([i for i in range(15) if i not in used_hole_nums])
                            used_hole_nums.append(Mole_.hole_num)
                        if (Mole_.hole_num < 0): continue
                        pic = self.mole[Mole_.num]
                        self.screen.blit(pic, self.hole_positions[Mole_.hole_num])
                    self.update()
                    if Mole.is_down == False:
                        Mole.num += 1
                    else:
                        Mole.num -= 1
                    if Mole.num == 4:
                        Mole.interval = 0.3
                    elif Mole.num == 3:
                        Mole.num -= 1
                        Mole.is_down = True
                        self.soundEffect.playPop()
                        Mole.interval = self.get_interval_by_level(initial_interval)  # get the newly decreased interval value
                    else:
                        Mole.interval = 0.1
                    Mole.cycle_time = 0
                    # Delay a little time
                    clock.tick(self.FPS)
            # Update the timer based on elapsed time
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            self.timer = max(timer_limit - elapsed_time // 1000, 0)
            if self.timer <= 0:
                # Game over, transition to the end screen or take appropriate actions
                self.current_state = self.END_SCREEN
                loop = False
            pygame.display.flip()
    def show_start_screen(self):
        # Show the start screen with text instructions
        self.screen.blit(self.background, (0, 0))
        # Create a transparent overlay for a blur effect
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay
        self.screen.blit(overlay, (0, 0))

        # Render text instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACEBAR to start the game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def show_end_screen(self):
        # Show the end screen
        self.screen.blit(self.background, (0, 0))
        # You can create a surface for the end screen text
        end_text_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        end_text_surface.fill((0, 0, 0, 128))  # Semi-transparent black overlay
        self.screen.blit(end_text_surface, (0, 0))
        # Display the player's score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        level_text = font.render(f"Your Level: {self.level}", True, (255, 255, 255))

        # Position the text on the end screen
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 50))
        level_rect = level_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 50))

        # Blit the text onto the end screen surface
        end_text_surface.blit(score_text, score_rect)
        end_text_surface.blit(level_text, level_rect)

        # Blit the end screen surface onto the main screen with alpha blending
        self.screen.blit(end_text_surface, (0, 0))
        pygame.display.flip()


# The Debugger class - use this class for printing out debugging information
class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode == "debug":
            print("> DEBUG: " + str(message))


class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(1.0)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        pygame.mixer.music.play(-1)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

###############################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Run the main loop
my_game = GameManager()
while my_game.current_state == my_game.START_SCREEN:
    my_game.show_start_screen()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            my_game.current_state = my_game.GAME_RUNNING
my_game.game_loop()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        my_game.show_end_screen()
        # Wait 3 seconds before exiting the game'
        pygame.time.wait(3000)
        pygame.quit()
        exit()
# Exit the game if the main loop ends
pygame.quit()
