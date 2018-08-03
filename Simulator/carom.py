from Constants import*
from numpy.polynomial import Polynomial as P
import math

class Carom:
    
    def __init__(self, render = False, pos_white = P0_WHITE, pos_yellow = P0_YELLOW, pos_red = P0_RED):
        Carom.build_table()
        self.white_ball, self.yellow_ball, self.red_ball = Carom.build_balls(pos_white, pos_yellow, pos_red)
        self.set_balls_init(pos_white, pos_yellow, pos_red)
        self.time = 0
        self.red_col = 0
        self.yellow_col =  0
        self.reward = 0
        self.action_reward = 0
        self.render = render   
        self.episode = 0
        self.input_scene = canvas(width=0, height=0)
        box(canvas=self.input_scene)
        self.reward_scene = canvas(width=0, height=0)
        box(canvas=self.reward_scene)
        self.episode_scene = canvas(width=0, height=0)
        box(canvas=self.episode_scene)
        self.observation_list = [(round(self.white_ball.P.x, 2),round(self.white_ball.P.y, 2),round(self.yellow_ball.P.x, 2),round(self.yellow_ball.P.y, 2),round(self.red_ball.P.x, 2),round(self.red_ball.P.y, 2))]
        
   
    def step(self, a, b, theta, phi, V):
        self.red_col = 0
        self.yellow_col =  0
        c = abs(sqrt(RADIUS**2 - a**2 - b**2))
        F = 2*BALL_MASS*V/(1 + BALL_MASS/CUE_MASS + (5/(2*RADIUS**2))*(a**2 + (b*cosinus(theta))**2 + (c*sinus(theta))**2 - 2*b*c*cosinus(theta)*sinus(theta)))
        #cf matrice de rotation
        rotation = -90 - (180 - phi)
        compv_x = 0
        compv_y = -F*cosinus(theta)/BALL_MASS
        compv_z = 0
        self.white_ball.v.x = compv_x*cosinus(rotation) - compv_y*sinus(rotation)
        self.white_ball.v.y = compv_x*sinus(rotation) + compv_y*cosinus(rotation)
        self.white_ball.v.z = compv_z
        ###
        compw_x = (-c*F*sinus(theta) + b*F*cosinus(theta))/I
        compw_y = a*F*sinus(theta)/I
        compw_z = -a*F*cosinus(theta)/I
        self.white_ball.w.x = compw_x*cosinus(rotation) - compw_y*sinus(rotation)
        self.white_ball.w.y = compw_x*sinus(rotation) + compw_y*cosinus(rotation)
        self.white_ball.w.z = compw_z
        self.set_ball_spin(self.white_ball)
        self.set_ball_u(self.white_ball)
        self.set_ball_color(self.white_ball, "WHITE")
        self.set_ball_state(self.white_ball)
        self.input_scene.caption = "\n\n<b>CUE INPUTS</b>\t\t\t<b>EQUIVALENT BALL IMPULSION</b> \na: %.3f\t\t\t\tv0 = (%.3f,%.3f,%.3f)\nb: %.3f\t\t\t\tw0 = (%.3f,%.3f,%.3f)\ntheta: %.3f\nphi: %.3f\nV: %.3f "%(a,self.white_ball.v.x,self.white_ball.v.y,self.white_ball.v.z,b,self.white_ball.w.x,self.white_ball.w.y,self.white_ball.w.z,theta,phi,V)
        self.move_balls()
        self.reward = self.reward + math.floor(self.yellow_col + self.red_col)
        self.action_reward = math.floor(self.yellow_col + self.red_col)
        done = self.action_reward == 0
        observation = (round(self.white_ball.P.x, 2),round(self.white_ball.P.y, 2),round(self.yellow_ball.P.x, 2),round(self.yellow_ball.P.y, 2),round(self.red_ball.P.x, 2),round(self.red_ball.P.y, 2))
        add_new_state = self.check_new_state(observation)
        if (add_new_state == True and done == False):
            self.observation_list.append(observation)
        if done == False:
            state = self.observation_list.index(observation)
        else:
            state = None
        self.reward_scene.caption = "\n\n<b>REWARD</b>: %d"%(self.reward)
        return state, self.action_reward, done, add_new_state
    


    def step2(self, a, b, theta, phi, V):
        self.red_col = 0
        self.yellow_col =  0
        c = abs(sqrt(RADIUS**2 - a**2 - b**2))
        F = 2*BALL_MASS*V/(1 + BALL_MASS/CUE_MASS + (5/(2*RADIUS**2))*(a**2 + (b*cosinus(theta))**2 + (c*sinus(theta))**2 - 2*b*c*cosinus(theta)*sinus(theta)))
        #cf matrice de rotation
        rotation = -90 - (180 - phi)
        compv_x = 0
        compv_y = -F*cosinus(theta)/BALL_MASS
        compv_z = 0
        self.white_ball.v.x = compv_x*cosinus(rotation) - compv_y*sinus(rotation)
        self.white_ball.v.y = compv_x*sinus(rotation) + compv_y*cosinus(rotation)
        self.white_ball.v.z = compv_z
        ###
        compw_x = (-c*F*sinus(theta) + b*F*cosinus(theta))/I
        compw_y = a*F*sinus(theta)/I
        compw_z = -a*F*cosinus(theta)/I
        self.white_ball.w.x = compw_x*cosinus(rotation) - compw_y*sinus(rotation)
        self.white_ball.w.y = compw_x*sinus(rotation) + compw_y*cosinus(rotation)
        self.white_ball.w.z = compw_z
        self.set_ball_spin(self.white_ball)
        self.set_ball_u(self.white_ball)
        self.set_ball_color(self.white_ball, "WHITE")
        self.set_ball_state(self.white_ball)
        self.input_scene.caption = "\n\n<b>CUE INPUTS</b>\t\t\t<b>EQUIVALENT BALL IMPULSION</b> \na: %.3f\t\t\t\tv0 = (%.3f,%.3f,%.3f)\nb: %.3f\t\t\t\tw0 = (%.3f,%.3f,%.3f)\ntheta: %.3f\nphi: %.3f\nV: %.3f "%(a,self.white_ball.v.x,self.white_ball.v.y,self.white_ball.v.z,b,self.white_ball.w.x,self.white_ball.w.y,self.white_ball.w.z,theta,phi,V)
        self.move_balls()
        self.reward = self.reward + math.floor(self.yellow_col + self.red_col)
        self.action_reward = math.floor(self.yellow_col + self.red_col)
        done = self.action_reward == 0
        observation = (self.white_ball.P.x,self.white_ball.P.y,self.yellow_ball.P.x,self.yellow_ball.P.y,self.red_ball.P.x,self.red_ball.P.y)
        add_new_state = self.check_new_state(observation)
        self.reward_scene.caption = "\n\n<b>REWARD</b>: %d"%(self.reward)
        return observation, self.action_reward, done, add_new_state

    def step3(self, a, b, theta, phi, V):
        self.red_col = 0
        self.yellow_col =  0
        c = abs(sqrt(RADIUS**2 - a**2 - b**2))
        F = 2*BALL_MASS*V/(1 + BALL_MASS/CUE_MASS + (5/(2*RADIUS**2))*(a**2 + (b*cosinus(theta))**2 + (c*sinus(theta))**2 - 2*b*c*cosinus(theta)*sinus(theta)))
        #cf matrice de rotation
        rotation = -90 - (180 - phi)
        compv_x = 0
        compv_y = -F*cosinus(theta)/BALL_MASS
        compv_z = 0
        self.white_ball.v.x = compv_x*cosinus(rotation) - compv_y*sinus(rotation)
        self.white_ball.v.y = compv_x*sinus(rotation) + compv_y*cosinus(rotation)
        self.white_ball.v.z = compv_z
        ###
        compw_x = (-c*F*sinus(theta) + b*F*cosinus(theta))/I
        compw_y = a*F*sinus(theta)/I
        compw_z = -a*F*cosinus(theta)/I
        self.white_ball.w.x = compw_x*cosinus(rotation) - compw_y*sinus(rotation)
        self.white_ball.w.y = compw_x*sinus(rotation) + compw_y*cosinus(rotation)
        self.white_ball.w.z = compw_z
        self.set_ball_spin(self.white_ball)
        self.set_ball_u(self.white_ball)
        self.set_ball_color(self.white_ball, "WHITE")
        self.set_ball_state(self.white_ball)
        self.input_scene.caption = "\n\n<b>CUE INPUTS</b>\t\t\t<b>EQUIVALENT BALL IMPULSION</b> \na: %.3f\t\t\t\tv0 = (%.3f,%.3f,%.3f)\nb: %.3f\t\t\t\tw0 = (%.3f,%.3f,%.3f)\ntheta: %.3f\nphi: %.3f\nV: %.3f "%(a,self.white_ball.v.x,self.white_ball.v.y,self.white_ball.v.z,b,self.white_ball.w.x,self.white_ball.w.y,self.white_ball.w.z,theta,phi,V)
        self.move_balls()
        self.action_reward = 1/self.get_total_distance()
        self.reward = self.reward + self.action_reward
        self.reward_scene.caption = "\n\n<b>ACTION REWARD</b>: %.3f"%(self.action_reward)
        self.reward_scene.append_to_caption("\n\n<b>CUMULATED EPISODE REWARD</b>: %.3f"%(self.reward))
        return self.action_reward

    def get_total_distance(self):
        dist_wy = sqrt((self.white_ball.P.x - self.yellow_ball.P.x)**2 + (self.white_ball.P.y - self.yellow_ball.P.y)**2)
        dist_wr = sqrt((self.white_ball.P.x - self.red_ball.P.x)**2 + (self.white_ball.P.y - self.red_ball.P.y)**2)
        dist_yr = sqrt((self.yellow_ball.P.x - self.red_ball.P.x)**2 + (self.yellow_ball.P.y - self.red_ball.P.y)**2)
        return dist_wy + dist_wr + dist_yr

    def check_new_state(self, observation):
        return observation not in self.observation_list
            
    def reset(self, pos_white = P0_WHITE, pos_yellow = P0_YELLOW, pos_red = P0_RED):
        self.set_balls_init(pos_white, pos_yellow, pos_red)
        self.time = 0
        self.reward = 0
        self.episode += 1
        self.episode_scene.caption = "\n\n<b>EPISODE</b>: %d"%(self.episode)

    def get_actions(self):
        actions = []
        for a in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
            for b in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
                for theta in np.arange(0,50,5):
                    for phi in np.arange(0,360,20):
                        for V in np.arange(0.1,6,0.5):
                            actions.append((a,b,theta,phi,V))
        return actions
        
    def set_balls_init(self, pos_white = P0_WHITE, pos_yellow = P0_YELLOW, pos_red = P0_RED):
        self.white_ball.pos = pos_white
        self.yellow_ball.pos = pos_yellow
        self.red_ball.pos = pos_red
        self.white_ball.P = pos_white
        self.yellow_ball.P = pos_yellow
        self.red_ball.P = pos_red
        self.white_ball.v = V0_WHITE
        self.yellow_ball.v = V0_YELLOW
        self.red_ball.v = V0_RED
        self.white_ball.w = W0_WHITE
        self.yellow_ball.w = W0_YELLOW
        self.red_ball.w = W0_RED
        self.set_ball_u(self.white_ball)
        self.set_ball_u(self.yellow_ball)
        self.set_ball_u(self.red_ball)
        self.set_ball_state(self.white_ball)
        self.set_ball_state(self.yellow_ball)
        self.set_ball_state(self.red_ball)
        self.set_ball_color(self.white_ball, "WHITE")
        self.set_ball_color(self.yellow_ball, "YELLOW")
        self.set_ball_color(self.red_ball, "RED")
        self.set_ball_spin(self.white_ball)
        self.set_ball_spin(self.yellow_ball)
        self.set_ball_spin(self.red_ball)

        
    def rendering(self):
        pass

    def take_action(self):
        pass
    
    def get_reward(self):
        pass



# class Build():
#     def __init__(self):
#         pass

    @staticmethod
    def build_table():
        surface = box(canvas=scene, pos=vector(0,0,- RADIUS - SURFACE_THICKNESS/2), size=vector(SURFACE_LENGTH,SURFACE_WIDTH, SURFACE_THICKNESS), color= green)
        Low_side = box(canvas=scene, pos=vector(0,-SURFACE_WIDTH/2 - SIDE_LENGTH/2,-RADIUS), size=vector(SURFACE_LENGTH + 2*SIDE_LENGTH, SIDE_LENGTH, 2*HEIGHT_RAILS), color = brown)
        Up_side = box(canvas=scene, pos=vector(0,SURFACE_WIDTH/2 + SIDE_LENGTH/2,-RADIUS), size=vector(SURFACE_LENGTH + 2*SIDE_LENGTH, SIDE_LENGTH,2*HEIGHT_RAILS), color = brown)
        R_side = box(canvas=scene, pos=vector(SURFACE_LENGTH/2 + SIDE_LENGTH/2,0,-RADIUS), size=vector(SIDE_LENGTH, SURFACE_WIDTH,2*HEIGHT_RAILS), color = brown)
        L_side = box(canvas=scene, pos=vector(-SURFACE_LENGTH/2 - SIDE_LENGTH/2,0,-RADIUS), size=vector(SIDE_LENGTH, SURFACE_WIDTH,2*HEIGHT_RAILS), color = brown)

    @staticmethod
    def build_balls(pos_white=P0_WHITE, pos_yellow=P0_YELLOW, pos_red = P0_RED):
        white_ball = sphere(canvas=scene, pos=pos_white, radius=RADIUS, color=color.white, make_trail = False)
        yellow_ball = sphere(canvas=scene, pos=pos_yellow, radius=RADIUS, color=color.yellow, make_trail = False)
        red_ball = sphere(canvas=scene, pos=pos_red, radius=RADIUS, color=color.red, make_trail = False)
        return white_ball, yellow_ball, red_ball

# class Physics():
#     def __init__(self):
#         pass

    def get_init(self, ball):
        ball_init = [ball.P, ball.v, ball.w, ball.u]
        return ball_init

    def FIND_DELTAT_NBSTEPS(self, time_end, print_ = False):
        nb_time_steps = math.ceil((time_end - self.time)/0.01)
        deltat = (time_end - self.time)/nb_time_steps
        if print_:
            print("Deltat : %f, nbtimestep :%d, ts + product:%f, time_end: %f"
            %(deltat,nb_time_steps, self.time + nb_time_steps*deltat,time_end))
        return deltat, nb_time_steps

    def set_ball_u(self, ball):
        ball.u = ball.v + RADIUS*cross(e_z,ball.w)

    def set_ball_state(self, ball):
        if (mag(ball.v)==0):
            ball.state = "STATIONNARY"
        else:
            if (mag(ball.u)<1e-6):
                ball.state = "ROLLING"
            else:
                ball.state = "SLIDING"
            
    def set_ball_color(self, ball, color):
        ball.col = color
        
    def set_ball_spin(self, ball):
        if(abs(ball.w.z) > EPS):
            ball.spin = True
        else:
            ball.spin = False

    def move_balls(self):
        if(self.white_ball.state == "STATIONNARY" and self.yellow_ball.state == "STATIONNARY" and self.red_ball.state == "STATIONNARY"):
            scene.caption =  "<b>LINEAR SPEED</b> [m/s]\nWHITE: %.3f \nYELLOW: %.3f\nRED: %.3f "%(mag(self.white_ball.v),mag(self.yellow_ball.v),mag(self.red_ball.v))
            scene.append_to_caption("\n\n<b>ROTATIONAL SPEED</b> [deg/s]\nWHITE: (%.3f,%.3f,%.3f) - Norm: %.3f\nYELLOW: (%.3f,%.3f,%.3f) - Norm: %.3f\nRED: (%.3f,%.3f,%.3f) - Norm: %.3f"%(self.white_ball.w.x,self.white_ball.w.y,self.white_ball.w.z,mag(self.white_ball.w),self.yellow_ball.w.x,self.yellow_ball.w.y,self.yellow_ball.w.z,mag(self.yellow_ball.w),self.red_ball.w.x,self.red_ball.w.y,self.red_ball.w.z,mag(self.red_ball.w)))
            scene.append_to_caption("\n\n<b>NEXT EVENT</b>: None")
            #scene.append_to_caption("\n\n<b>REWARD</b>: %d"%(self.reward))
        else:
            
            event,time_next_ev = self.NEXT_EVENT_BALLS()
            scene.caption =  "<b>LINEAR SPEED</b> [m/s]\nWHITE: %.3f \nYELLOW: %.3f\nRED: %.3f "%(mag(self.white_ball.v),mag(self.yellow_ball.v),mag(self.red_ball.v))
            scene.append_to_caption("\n\n<b>ROTATIONAL SPEED</b> [deg/s]\nWHITE: (%.3f,%.3f,%.3f) - Norm: %.3f\nYELLOW: (%.3f,%.3f,%.3f) - Norm: %.3f\nRED: (%.3f,%.3f,%.3f) - Norm: %.3f"%(self.white_ball.w.x,self.white_ball.w.y,self.white_ball.w.z,mag(self.white_ball.w),self.yellow_ball.w.x,self.yellow_ball.w.y,self.yellow_ball.w.z,mag(self.yellow_ball.w),self.red_ball.w.x,self.red_ball.w.y,self.red_ball.w.z,mag(self.red_ball.w)))
            scene.append_to_caption("\n\n<b>NEXT EVENT</b>: " + event)
            #scene.append_to_caption("\n\n<b>REWARD</b>: %d"%(self.reward))
            #sleep(1)
            self.white_ball, self.yellow_ball, self.red_ball = self.SLIDING_OR_ROLLING(time_next_ev)
            self.white_ball, self.yellow_ball, self.red_ball = self.EVENT_PROCESSING_BALLS(event)
            self.time = time_next_ev
            self.move_balls()
    
    def NEXT_EVENT_BALLS(self):
        balls = []
        balls.append(self.white_ball)
        balls.append(self.yellow_ball)
        balls.append(self.red_ball)
        real_solutions = []
        # EVENTS = ["SLI2ROL","ROL2STA","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL",
        # "HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","END_SPIN"]
        EVENTS = []
        ## TIME END SLIDINGROLLING ##
        for ball in balls:
            if ball.state != "STATIONNARY":
                prefix = ball.col
                if ball.state == "SLIDING":
                    coef_x = 0.5*MU_s*hat(ball.u).x
                    coef_y = 0.5*MU_s*hat(ball.u).y
                    time_end_sliding = 2*mag(ball.u)/(7*MU_s*g)
                    real_solutions.append(time_end_sliding)
                    EVENTS.append(prefix + "SLI2ROL")
                elif ball.state =="ROLLING":
                    coef_x = (5/14)*MU_r*hat(ball.v).x
                    coef_y = (5/14)*MU_r*hat(ball.v).y
                    time_end_rolling = (7/5)*(mag(ball.v)/(MU_r*g))
                    real_solutions.append(time_end_rolling)
                    EVENTS.append(prefix + "ROL2STA")

                ## TIME COLLISION WITH RIGHT RAIL ##
                p = P([ball.P.x - (SURFACE_LENGTH/2 - RADIUS), ball.v.x, -coef_x*g])
                solutions = p.roots()
                real_solutions.extend([i for i in solutions if i.imag == 0])
                length_added_sol = len([i for i in solutions if i.imag == 0])
                EVENTS.extend([prefix + "RIGHT_RAIL_COL" for i in range(length_added_sol)])

                ## TIME COLLISION WITH LEFT RAIL ##
                p = P([ball.P.x - (-SURFACE_LENGTH/2 + RADIUS), ball.v.x, -coef_x*g])
                solutions = p.roots()
                real_solutions.extend([i for i in solutions if i.imag == 0])
                length_added_sol = len([i for i in solutions if i.imag == 0])
                EVENTS.extend([prefix + "LEFT_RAIL_COL" for i in range(length_added_sol)])

                # ## TIME COLLISION WITH UP RAIL ##
                p = P([ball.P.y - (SURFACE_WIDTH/2 - RADIUS), ball.v.y, -coef_y*g])
                solutions = p.roots()
                real_solutions.extend([i for i in solutions if i.imag == 0])
                length_added_sol = len([i for i in solutions if i.imag == 0])
                EVENTS.extend([prefix + "UP_RAIL_COL" for i in range(length_added_sol)])

                # ## TIME COLLISION WITH DOWN RAIL ##
                p = P([ball.P.y - (-SURFACE_WIDTH/2 + RADIUS), ball.v.y, -coef_y*g])
                solutions = p.roots()
                #coef = [-coef*g*hat(ball.u).y,ball.v.y,ball.P.y - (-SURFACE_WIDTH/2 + RADIUS)]
                #solutions = np.roots(coef)
                real_solutions.extend([i for i in solutions if i.imag == 0])
                length_added_sol = len([i for i in solutions if i.imag == 0])
                EVENTS.extend([prefix + "DOWN_RAIL_COL" for i in range(length_added_sol)])

                ## TIME STOP SPIN
                if ball.spin:
                    time_end_spinning = np.sign(ball.w.z)*2*RADIUS*(ball.w.z)/(5*MU_sp*g)
                    real_solutions.append(time_end_spinning)
                    EVENTS.append(prefix + "END_SPIN")

                ## TIME COLLISION WITH BALL
                #  ....
                if ball.col == "WHITE":
                        ######## COLLISION BLANCHE JAUNE ###########
                    if balls[1].state == "SLIDING":
                        coef_x2 = 0.5*MU_s*hat(balls[1].u).x
                        coef_y2 = 0.5*MU_s*hat(balls[1].u).y
                    elif balls[1].state =="ROLLING":
                        coef_x2 = (5/14)*MU_r*hat(balls[1].v).x
                        coef_y2 = (5/14)*MU_r*hat(balls[1].v).y	
                    elif balls[1].state =="STATIONNARY":
                        coef_x2 = 0
                        coef_y2 = 0
                    a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
                    b = g*(-2*(ball.v.x - balls[1].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[1].v.y)*(coef_y - coef_y2))
                    c = (ball.v.x - balls[1].v.x)**2 - 2*g*(ball.P.x - balls[1].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[1].v.y)**2 - 2*g*(ball.P.y - balls[1].P.y)*(coef_y - coef_y2)
                    d = 2*(ball.P.x - balls[1].P.x)*(ball.v.x - balls[1].v.x) + 2*(ball.P.y - balls[1].P.y)*(ball.v.y - balls[1].v.y)
                    e = (ball.P.x - balls[1].P.x)**2 + (ball.P.y - balls[1].P.y)**2 -4*(RADIUS**2)
                    coef_eq=[a,b,c,d,e]
                    solutions = np.roots(coef_eq)
                    real_solutions.extend([i for i in solutions if i.imag == 0])
                    length_added_sol = len([i for i in solutions if i.imag == 0])
                    EVENTS.extend([prefix + "-YELLOW-BALLBALL" for i in range(length_added_sol)])

                    ###### COLLISION BLANCHE -> ROUGE ########	
                    if balls[2].state == "SLIDING":
                        coef_x2 = 0.5*MU_s*hat(balls[2].u).x
                        coef_y2 = 0.5*MU_s*hat(balls[2].u).y
                    elif balls[2].state =="ROLLING":
                        coef_x2 = (5/14)*MU_r*hat(balls[2].v).x
                        coef_y2 = (5/14)*MU_r*hat(balls[2].v).y	
                    elif balls[2].state =="STATIONNARY":
                        coef_x2 = 0
                        coef_y2 = 0
                    a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
                    b = g*(-2*(ball.v.x - balls[2].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[2].v.y)*(coef_y - coef_y2))
                    c = (ball.v.x - balls[2].v.x)**2 - 2*g*(ball.P.x - balls[2].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[2].v.y)**2 - 2*g*(ball.P.y - balls[2].P.y)*(coef_y - coef_y2)
                    d = 2*(ball.P.x - balls[2].P.x)*(ball.v.x - balls[2].v.x) + 2*(ball.P.y - balls[2].P.y)*(ball.v.y - balls[2].v.y)
                    e = (ball.P.x - balls[2].P.x)**2 + (ball.P.y - balls[2].P.y)**2 -4*(RADIUS**2)
                    coef_eq=[a,b,c,d,e]
                    solutions = np.roots(coef_eq)
                    real_solutions.extend([i for i in solutions if i.imag == 0])
                    length_added_sol = len([i for i in solutions if i.imag == 0])
                    EVENTS.extend([prefix + "-RED-BALLBALL" for i in range(length_added_sol)])

                if ball.col == "YELLOW":
                    ######## COLLISION JAUNE BLANCHE ###########
                    if balls[0].state == "SLIDING":
                        coef_x2 = 0.5*MU_s*hat(balls[0].u).x
                        coef_y2 = 0.5*MU_s*hat(balls[0].u).y
                    elif balls[0].state =="ROLLING":
                        coef_x2 = (5/14)*MU_r*hat(balls[0].v).x
                        coef_y2 = (5/14)*MU_r*hat(balls[0].v).y	
                    elif balls[0].state =="STATIONNARY":
                        coef_x2 = 0
                        coef_y2 = 0
                    a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
                    b = g*(-2*(ball.v.x - balls[0].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[0].v.y)*(coef_y - coef_y2))
                    c = (ball.v.x - balls[0].v.x)**2 - 2*g*(ball.P.x - balls[0].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[0].v.y)**2 - 2*g*(ball.P.y - balls[0].P.y)*(coef_y - coef_y2)
                    d = 2*(ball.P.x - balls[0].P.x)*(ball.v.x - balls[0].v.x) + 2*(ball.P.y - balls[0].P.y)*(ball.v.y - balls[0].v.y)
                    e = (ball.P.x - balls[0].P.x)**2 + (ball.P.y - balls[0].P.y)**2 -4*(RADIUS**2)
                    coef_eq=[a,b,c,d,e]
                    solutions = np.roots(coef_eq)
                    real_solutions.extend([i for i in solutions if i.imag == 0])
                    length_added_sol = len([i for i in solutions if i.imag == 0])
                    EVENTS.extend([prefix + "-WHITE-BALLBALL" for i in range(length_added_sol)])

                    ######## COLLISION JAUNE ROUGE ###########
                    if balls[2].state == "SLIDING":
                        coef_x2 = 0.5*MU_s*hat(balls[2].u).x
                        coef_y2 = 0.5*MU_s*hat(balls[2].u).y
                    elif balls[2].state =="ROLLING":
                        coef_x2 = (5/14)*MU_r*hat(balls[2].v).x
                        coef_y2 = (5/14)*MU_r*hat(balls[2].v).y	
                    elif balls[2].state =="STATIONNARY":
                        coef_x2 = 0
                        coef_y2 = 0
                    a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
                    b = g*(-2*(ball.v.x - balls[2].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[2].v.y)*(coef_y - coef_y2))
                    c = (ball.v.x - balls[2].v.x)**2 - 2*g*(ball.P.x - balls[2].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[2].v.y)**2 - 2*g*(ball.P.y - balls[2].P.y)*(coef_y - coef_y2)
                    d = 2*(ball.P.x - balls[2].P.x)*(ball.v.x - balls[2].v.x) + 2*(ball.P.y - balls[2].P.y)*(ball.v.y - balls[2].v.y)
                    e = (ball.P.x - balls[2].P.x)**2 + (ball.P.y - balls[2].P.y)**2 -4*(RADIUS**2)
                    coef_eq=[a,b,c,d,e]
                    solutions = np.roots(coef_eq)
                    real_solutions.extend([i for i in solutions if i.imag == 0])
                    length_added_sol = len([i for i in solutions if i.imag == 0])
                    EVENTS.extend([prefix + "-RED-BALLBALL" for i in range(length_added_sol)])

                if ball.col == "RED":
                    ######## COLLISION ROUGE BLANC ###########
                    if balls[0].state == "SLIDING":
                        coef_x2 = 0.5*MU_s*hat(balls[0].u).x
                        coef_y2 = 0.5*MU_s*hat(balls[0].u).y
                    elif balls[0].state =="ROLLING":
                        coef_x2 = (5/14)*MU_r*hat(balls[0].v).x
                        coef_y2 = (5/14)*MU_r*hat(balls[0].v).y	
                    elif balls[0].state =="STATIONNARY":
                        coef_x2 = 0
                        coef_y2 = 0
                    a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
                    b = g*(-2*(ball.v.x - balls[0].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[0].v.y)*(coef_y - coef_y2))
                    c = (ball.v.x - balls[0].v.x)**2 - 2*g*(ball.P.x - balls[0].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[0].v.y)**2 - 2*g*(ball.P.y - balls[0].P.y)*(coef_y - coef_y2)
                    d = 2*(ball.P.x - balls[0].P.x)*(ball.v.x - balls[0].v.x) + 2*(ball.P.y - balls[0].P.y)*(ball.v.y - balls[0].v.y)
                    e = (ball.P.x - balls[0].P.x)**2 + (ball.P.y - balls[0].P.y)**2 -4*(RADIUS**2)
                    coef_eq=[a,b,c,d,e]
                    solutions = np.roots(coef_eq)
                    real_solutions.extend([i for i in solutions if i.imag == 0])
                    length_added_sol = len([i for i in solutions if i.imag == 0])
                    EVENTS.extend([prefix + "-WHITE-BALLBALL" for i in range(length_added_sol)])

                    ######## COLLISION ROUGE JAUNE ###########
                    if balls[1].state == "SLIDING":
                        coef_x2 = 0.5*MU_s*hat(balls[1].u).x
                        coef_y2 = 0.5*MU_s*hat(balls[1].u).y
                    elif balls[1].state =="ROLLING":
                        coef_x2 = (5/14)*MU_r*hat(balls[1].v).x
                        coef_y2 = (5/14)*MU_r*hat(balls[1].v).y	
                    elif balls[1].state =="STATIONNARY":
                        coef_x2 = 0
                        coef_y2 = 0
                    a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
                    b = g*(-2*(ball.v.x - balls[1].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[1].v.y)*(coef_y - coef_y2))
                    c = (ball.v.x - balls[1].v.x)**2 - 2*g*(ball.P.x - balls[1].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[1].v.y)**2 - 2*g*(ball.P.y - balls[1].P.y)*(coef_y - coef_y2)
                    d = 2*(ball.P.x - balls[1].P.x)*(ball.v.x - balls[1].v.x) + 2*(ball.P.y - balls[1].P.y)*(ball.v.y - balls[1].v.y)
                    e = (ball.P.x - balls[1].P.x)**2 + (ball.P.y - balls[1].P.y)**2 -4*(RADIUS**2)
                    coef_eq=[a,b,c,d,e]
                    solutions = np.roots(coef_eq)
                    real_solutions.extend([i for i in solutions if i.imag == 0])
                    length_added_sol = len([i for i in solutions if i.imag == 0])
                    EVENTS.extend([prefix + "-WHITE-BALLBALL" for i in range(length_added_sol)])
                


        min_time = min(x for x in real_solutions if x > EPS)
        #print(real_solutions)
        #print(EVENTS)
        min_index = real_solutions.index(min_time)
        found_event = EVENTS[min_index]
        #print(min_index)
        #print(min_time)
        min_time = min_time + self.time
        return found_event, min_time.real


    def SLIDING_OR_ROLLING(self, time_end):
        balls = []
        balls.append(self.white_ball)
        balls.append(self.yellow_ball)
        balls.append(self.red_ball)
        #INITIAL STATE
        deltat, nb_time_steps = self.FIND_DELTAT_NBSTEPS(time_end)
        ball_init_white = self.get_init(balls[0])
        ball_init_yellow = self.get_init(balls[1])
        ball_init_red = self.get_init(balls[2])
        balls[0].init = ball_init_white
        balls[1].init = ball_init_yellow
        balls[2].init = ball_init_red
        #RENDERING PART 
        if self.render:
            for i in range(nb_time_steps + 1):
                rate(rate_value)
                t = i*deltat + self.time
                for ball in balls:
                    if(ball.state == "SLIDING"):
                        ball.pos = ball.init[0] + ball.init[1]*(t - self.time) - 0.5*MU_s*g*((t - self.time)**2)*hat(ball.init[3])
                        #ball.v = ball.init[1] - MU_s*g*(t - self.time)*hat(ball.init[3])
                        #print(mag(ball.v))
                    elif(ball.state == "ROLLING"):
                        ball.pos = ball.init[0] + ball.init[1]*(t -	 self.time) - (5/14)*MU_r*g*((t - self.time)**2)*hat(ball.init[1])
                        #ball.v = ball.init[1] - (5/7)*MU_r*g*(t - self.time)*hat(ball.init[1])
                        #print(mag(ball.v))
        #FINAL STATE
        else:
            t = nb_time_steps*deltat + self.time
        for ball in balls:
            if(ball.state == "SLIDING"):
                ball.P = ball.init[0] + ball.init[1]*(t - self.time) - 0.5*MU_s*g*((t - self.time)**2)*hat(ball.init[3])
                ball.v = ball.init[1] - MU_s*g*(t - self.time)*hat(ball.init[3])
                ball.w = ball.init[2] + 2.5*MU_s*g*(t - self.time)*cross(e_z,hat(ball.init[3]))/RADIUS # Has to be verified (- or + before 2.5 depending on papers)
                if(ball.spin):
                    ball.w.z = ball.init[2].z - np.sign(ball.init[2].z)*2.5*MU_sp*g*(t - self.time)/RADIUS # Has no efffect (but still to be verified)
                ball.u = ball.v + RADIUS*cross(e_z, ball.w) #  OR THIS: ball.u = ball_init[3] - 3.5*MU_s*g*t*hat(ball_init[3])
            elif(ball.state == "ROLLING"):
                ball.P = ball.init[0] + ball.init[1]*(t - self.time) - (5/14)*MU_r*g*((t - self.time)**2)*hat(ball.init[1])
                ball.v = ball.init[1] - (5/7)*MU_r*g*(t - self.time)*hat(ball.init[1])
                ball.w = cross(hat(e_z),ball.v)/RADIUS
                if(ball.spin):
                    ball.w.z = ball.init[2].z - np.sign(ball.init[2].z)*2.5*MU_sp*g*(t - self.time)/RADIUS # Has no efffect (but still to be verified)
                ball.u = ball.v + RADIUS*cross(e_z, ball.w) # u remains equal to 0 during rolling
        return balls[0],balls[1],balls[2]

    def EVENT_PROCESSING_BALLS(self, event):
        #print(event)
        balls = []
        balls.append(self.white_ball)
        balls.append(self.yellow_ball)
        balls.append(self.red_ball)
        for ball in balls:
            if event == ball.col + "SLI2ROL":
                ball.state = "ROLLING"
            elif event == ball.col + "ROL2STA":
                ball.state = "STATIONNARY"
            elif event == ball.col + "LEFT_RAIL_COL":
                #ball = VERTICAL_RAIL_COLLISION(ball)
                ball = self.RAIL_COLLISION(ball, "left")
            elif event == ball.col + "RIGHT_RAIL_COL":
                #ball = VERTICAL_RAIL_COLLISION(ball)
                ball = self.RAIL_COLLISION(ball, "right")
            elif event == ball.col + "UP_RAIL_COL":
                #ball = HORIZONTAL_RAIL_COLLISION(ball)
                ball = self.RAIL_COLLISION(ball, "up")
            elif event == ball.col + "DOWN_RAIL_COL":
                #ball = HORIZONTAL_RAIL_COLLISION(ball)
                ball = self.RAIL_COLLISION(ball, "down")
            elif event == ball.col + "END_SPIN":
                ball.spin = False
            elif event == ball.col + "-WHITE-BALLBALL":
                ball, balls[0] = self.BALLS_COLLISION(ball, balls[0])
                if ball.col == "YELLOW":
                    self.yellow_col = 0.5
                elif ball.col == "RED":
                    self.red_col = 0.5
            elif event == ball.col + "-YELLOW-BALLBALL":
                ball, balls[1] = self.BALLS_COLLISION(ball, balls[1])
                if ball.col == "WHITE":
                    self.yellow_col = 0.5
            elif event == ball.col + "-RED-BALLBALL":
                ball, balls[2] = self.BALLS_COLLISION(ball, balls[2])
                if ball.col == "WHITE":
                    self.red_col = 0.5
        return balls[0], balls[1], balls[2]
    
    def RAIL_COLLISION(self, ball, direction):
        if direction == "left":
            n = vector(1,0,0)
        elif direction == "right":
            n = vector(-1,0,0)
        elif direction == "up":
            n = vector(0,-1,0)
        elif direction == "down":
            n = vector(0,1,0)
        v_init = ball.v
        w_init = ball.w
        k = 1 + ELAST
        P = k*BALL_MASS*dot(vector(0,0,0) - v_init,n)
        Vc_init = v_init - vector(0,0,0) - (dot(v_init - vector(0,0,0), n))*n + cross(n,RADIUS*w_init + vector(0,0,0))
        ball.v = v_init + n*P/BALL_MASS - Vc_init/7
        ball.w = w_init + (5/(7*RADIUS))*cross(n,Vc_init/2)
        ball.v.z = v_init.z
        if (mag(ball.u)<1e-6):
            ball.state = "ROLLING"
        else:
            ball.state = "SLIDING"
        return ball

    def BALLS_COLLISION(self,ball1, ball2):
        v1_init = ball1.v
        v2_init = ball2.v
        w1_init = ball1.w
        w2_init = ball2.w
        intersection = (ball1.P + ball2.P)/2
        n = ball1.P - intersection
        k = (1 + ELAST)/2
        P = k*BALL_MASS*dot(v2_init - v1_init,hat(n))
        Vc_init = v1_init - v2_init - (dot(v1_init - v2_init, hat(n)))*hat(n) + cross(hat(n),RADIUS*w1_init + RADIUS*w2_init)
        ball1.v = v1_init + hat(n)*P/BALL_MASS - Vc_init/7
        ball1.w = w1_init + (5/(7*RADIUS))*cross(hat(n),Vc_init/2)
        ball2.v = v2_init + (v1_init - ball1.v)
        ball2.w = w2_init - (w1_init - ball1.w)
        ball1.v.z = v1_init.z
        ball2.v.z = v2_init.z
        ball1.u = ball1.v + RADIUS*cross(e_z,ball1.w)
        ball2.u = ball2.v + RADIUS*cross(e_z,ball2.w)

        if (mag(ball1.u)<1e-6):
            ball1.state = "ROLLING"
        else:
            ball1.state = "SLIDING"
        if (mag(ball2.u)<1e-6):
            ball2.state = "ROLLING"
        else:
            ball2.state = "SLIDING"
        return ball1, ball2