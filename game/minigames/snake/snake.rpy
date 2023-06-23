init:
    $ import game.minigames.snake.grass_cutter as grass_cutter
    $ import game.minigames.snake.snake as snake
    $ import game.minigames.snake.snake_draw as snake_draw

label play_snake:

    e "Welcome!"

    e "What do you want to Play??"

label aliens_retry:
    menu:
        "Snake":
            $ score = snake.main()
        "Grass Cutter":
            $ score = grass_cutter.main()
        "Snake Draw (Test)":
            $ score = snake_draw.main()

    e "Point: [score]"

    if score > 10:

        e "Not bad!"

    menu:

        "Would you like to try again?"

        "Sure.":

            "Okay, get ready..."

            jump aliens_retry

        "No thanks.":

            "Okay, by"

            pass
    return
