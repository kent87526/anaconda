"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    ball_position_histroy=[]

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        ball_position_histroy.append(scene_info.ball)
        platform_center_x = scene_info.platform[0]+20
        if(len(ball_position_histroy)) == 1:
            ball_going_down = 0
        elif ball_position_histroy[-1][1]-ball_position_histroy[-2][1] > 0:
            ball_going_down = 1
            
            vx = ball_position_histroy[-1][0]-ball_position_histroy[-2][0]
            vy = ball_position_histroy[-1][1]-ball_position_histroy[-2][1]
            ball_position_pridictonplateform = ball_position_histroy[-1][0]+(400-ball_position_histroy[-1][1])*vx/vy
            while ball_position_pridictonplateform < 0 or ball_position_pridictonplateform > 200 :
                if ball_position_pridictonplateform > 200:
                    ball_position_pridictonplateform = 400-ball_position_pridictonplateform
                else:
                    ball_position_pridictonplateform = -ball_position_pridictonplateform
        
            if platform_center_x < ball_position_pridictonplateform:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif platform_center_x > ball_position_pridictonplateform:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                continue
        
        else:
            ball_going_down = 0
        
            if platform_center_x < 100:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif platform_center_x > 100:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                continue
            

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        
