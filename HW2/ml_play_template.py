"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)
import numpy as np
import pickle
def ml_loop():
    """The main loop of the machine learning process
    This loop is run in a separate process, and communicates with the game process.
    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """
ball_position_history=[]
   # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    
filename='svc_example.sav'
model=pickle.load(open(filename, 'rb'))

comm.ml_ready()
    

    # 3. Start an endless loop.
while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        ball_position_history.append(scene_info.ball)
        if(len(ball_position_history) > 2):
            vx1=ball_position_history[-1][0]
            vx2=ball_position_history[-2][0]
            vy1=ball_position_history[-1][1]
            vy2=ball_position_history[-2][1]
            inp_temp=np.array([vx2, vy2, vx1, vy1, scene_info.platform[0]])
            input=inp_temp[np.newaxis, :]
            print(input)
        # 3.2. If the game is over or passed, the game process will reset
            if scene_info.status == GameStatus.GAME_OVER or \
                scene_info.status == GameStatus.GAME_PASS:
                comm.ml_ready()
                continue
        #      the scene and wait for ml process doing resetting job.
        # 3.3. Put the code here to handle the scene information
            move=model.predict(input)
        # 3.4. Send the instruction for this frame to the game process
            print(move)
            if move > 0:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif move < 0:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
