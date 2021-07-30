

class UserProfile:
    def __init__(self, user_profile):
        self.profile = user_profile
        self.__user_amount_spent_money = int(user_profile.amount_spent_money)
        self.user_status = ''
        self.user_percent_render_progress = 0
        self.__user_status_processing()

    def __user_status_processing(self):
        if self.profile.amount_spent_money < 250:
            self.user_status = 'Beginner'
            self.user_percent_render_progress = self.__get_percent_on_cut(self.__user_amount_spent_money, 250)

        elif self.profile.amount_spent_money < 700:
            self.user_status = 'Beginner' + '+'
            self.user_percent_render_progress = 25 + self.__get_percent_on_cut(self.__user_amount_spent_money - 250,
                                                                               700 - 250)

        elif self.profile.amount_spent_money < 1500:
            self.user_status = 'Regular'
            self.user_percent_render_progress = 50 + self.__get_percent_on_cut(self.__user_amount_spent_money - 700,
                                                                               1500 - 700)

        elif self.profile.amount_spent_money < 2500:
            self.user_status = 'Regular' + '+'
            self.user_percent_render_progress = 75 + self.__get_percent_on_cut(self.__user_amount_spent_money - 1500,
                                                                               2500 - 1500)

        else:
            self.user_status = 'VIP'
            self.user_percent_render_progress = 100

    @staticmethod
    def __get_percent_on_cut(num1, num2) -> int:
        percent_between_nums = (num1/num2)*100
        return int(25*(percent_between_nums/100))
