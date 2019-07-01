class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Eold = 0
        self.Etotaal = 0
        self.Edelta = 0

    def Calc_P(self, error):
        return self.Kp * error

    def Calc_I(self, error):
        self.Etotaal = self.Etotaal + error
        return self.Ki * self.Etotaal

    def Calc_D(self, error):
        self.Edelta = error - self.Eold
        self.Eold = error
        return self.Kd * self.Edelta

    def Calc(self, error):
        return self.Calc_P(error) + self.Calc_I(error) + self.Calc_D(error)


