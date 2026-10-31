def trigger_sprite_reaction(event_type):
    if event_type == 'keylogger_spike':
        with open('logs/sprite_reactions.log', 'a') as f:
            f.write("SpriteGirl jumps in alarm! Keyboard spike detected.\n")
