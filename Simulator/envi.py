from Parameters import*

class Envi:
    
    def __init__(self):
        Envi.build_table()
        self.white_ball, self.yellow_ball, self.red_ball = Envi.build_balls()
        self.white_ball.P = P0_WHITE
        self.yellow_ball.P = P0_YELLOW
        self.red_ball.P = P0_RED
        self.yellow_ball.v = V0_YELLOW
        self.red_ball.v = V0_RED
        self.yellow_ball.w = W0_YELLOW
        self.red_ball.w = W0_RED
        self.set_ball_u(self.yellow_ball)
        self.set_ball_u(self.red_ball)
        self.set_ball_state(self.yellow_ball)
        self.set_ball_state(self.red_ball)
        self.set_ball_color(self.white_ball, "WHITE")
        self.set_ball_color(self.yellow_ball, "YELLOW")
        self.set_ball_color(self.red_ball, "RED")
        self.set_ball_spin(self.yellow_ball)
        self.set_ball_spin(self.red_ball)
        

   
    def step(self, a, b, thetha, phi, V):
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

    def reset(self):
        print("ok")

    def render(self):
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
    def build_balls():
        white_ball = sphere(canvas=scene, pos=P0_WHITE, radius=RADIUS, color=color.white, make_trail = True)
        yellow_ball = sphere(canvas=scene, pos=P0_YELLOW, radius=RADIUS, color=color.yellow, make_trail = True)
        red_ball = sphere(canvas=scene, pos=P0_RED, radius=RADIUS, color=color.red, make_trail = True)
        return white_ball, yellow_ball, red_ball

# class Physics():
#     def __init__(self):
#         pass

    def get_init(self, ball):
        ball_init = [ball.P, ball.v, ball.w, ball.u]
        return ball_init

    def FIND_DELTAT_NBSTEPS(self, time_start,time_end, print_ = False):
        nb_time_steps = math.ceil((time_end - time_start)/0.01)
        deltat = (time_end - time_start)/nb_time_steps
        if print_:
            print("Deltat : %f, nbtimestep :%d, ts + product:%f, time_end: %f"
            %(deltat,nb_time_steps, time_start + nb_time_steps*deltat,time_end))
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
