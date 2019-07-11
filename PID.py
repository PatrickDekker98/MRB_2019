class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Eold = 0
        self.Etotaal = 0
        self.Edelta = 0
        self.dt = 0.008333333

    def Calc_P(self, error):
        return self.Kp * error

    def Calc_I(self, error):
        self.Etotaal = self.Etotaal + error
        return self.Ki * (self.Etotaal / self.dt)

    def Calc_D(self, error):
        self.Edelta = error - self.Eold
        self.Eold = error
        return self.Kd * (self.Edelta * self.dt)

    def Calc(self, error):
        return self.Calc_P(error) + self.Calc_I(error) + self.Calc_D(error)

    def resetError():
        self.Eold = 0
        self.Etotaal = 0
        self.Edelta = 0
    
    def set_Kp(self, x):
        self.Kp = x

    def set_Ki(self, x):
        self.Ki = x

    def set_Kd(self, x):
        self.Kd = x 

