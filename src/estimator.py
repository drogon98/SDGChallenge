import math,decimal


class Estimator(object):

  def __init__(self,data=None):
    if data:
      self.input_data = data
    else:
      self.input_data = {}

    self.reported_cases = self.input_data.get("reportedCases")

    # sets the day instance variable
    self.period_normaliser_to_days()

    # sets the factor instance variable
    self.period_factor_calculator()

    self.available_beds = math.floor(0.35*self.input_data.get("totalHospitalBeds"))


    self.majority_earning_population_fraction = self.input_data["region"]["avgDailyIncomePopulation"]

    self.average_daily_income = self.input_data["region"]["avgDailyIncomeInUSD"]


  def get_current_infected_estimation(self):
    if self.reported_cases != None:
      return self.reported_cases*10
    return 0


  def get_severe_current_infected_estimation(self):
    if self.reported_cases != None:
      return self.reported_cases*50
    return 0


  def period_normaliser_to_days(self):
    days = "days"
    weeks = "weeks"
    months = "months"
    days_in_a_week = 7
    days_in_a_month = 30

    period_type = self.input_data.get("periodType")
    elapse_time = self.input_data.get("timeToElapse")

    if str(period_type).casefold() == days.casefold():
      self.days = elapse_time
      return self.days
    elif str(period_type).casefold() == weeks.casefold():
      self.days = elapse_time*days_in_a_week
      return self.days
    elif str(period_type).casefold() == months.casefold():
      self.days = elapse_time*days_in_a_month
      return self.days


  def period_factor_calculator(self):
    infections_to_double_period_in_days = 3
    days = self.period_normaliser_to_days()
    self.factor = math.floor(days/infections_to_double_period_in_days)
    return self.factor


  def get_projected_number_of_infections(self):
    current_infections_estimation = self.get_current_infected_estimation()
    return current_infections_estimation*(2**self.factor) 


  def get_projected_number_of_severe_infections(self):
    current_severe_infections_estimation = self.get_severe_current_infected_estimation()
    return current_severe_infections_estimation*(2**self.factor)


  def get_infection_cases_to_hospitalize_estimation(self):
    projected_infections_estimation = self.get_projected_number_of_infections()
    return math.floor(0.15*projected_infections_estimation)


  def get_projected_infection_cases_to_hospitalize_estimation(self):
    projected_severe_infections_estimation = self.get_projected_number_of_severe_infections()
    return math.floor(0.15*projected_severe_infections_estimation)


  def get_available_beds_for_infection_cases(self):
    to_hospitalize_estimation = self.get_infection_cases_to_hospitalize_estimation()
    if self.available_beds >= to_hospitalize_estimation:
      return self.available_beds
    return self.available_beds - to_hospitalize_estimation


  def get_available_beds_for_severe_projected_cases(self):
    to_hospitalize_estimation = self.get_projected_infection_cases_to_hospitalize_estimation()
    if self.available_beds >= to_hospitalize_estimation:
      return self.available_beds
    return self.available_beds - to_hospitalize_estimation

  def get_infection_cases_to_require_icu(self):
    projected_infections_estimation = self.get_projected_number_of_infections()
    return math.floor(0.05*projected_infections_estimation)


  def get_severe_infection_cases_to_require_icu(self):
    projected_severe_infections_estimation = self.get_projected_number_of_severe_infections()
    return math.floor(0.05*projected_severe_infections_estimation)


  def get_infection_cases_to_require_ventilators(self):
    projected_infections_estimation = self.get_projected_number_of_infections()
    return math.floor(0.02*projected_infections_estimation)


  def get_severe_infection_cases_to_require_ventilators(self):
    projected_severe_infections_estimation = self.get_projected_number_of_severe_infections()
    return math.floor(0.02*projected_severe_infections_estimation)


  def get_money_economy_is_likely_to_loose_on_infections(self):
    projected_infections_estimation = self.get_projected_number_of_infections()
    decimal_places = decimal.Decimal("0.01")
    amount = decimal.Decimal(projected_infections_estimation*self.majority_earning_population_fraction*self.average_daily_income*self.days)
    return str(amount.quantize(decimal_places))


  def get_money_economy_is_likely_to_loose_on_projected_infections(self):
    projected_severe_infections_estimation = self.get_projected_number_of_severe_infections()
    decimal_places = decimal.Decimal("0.01")
    amount = decimal.Decimal(projected_severe_infections_estimation*self.majority_earning_population_fraction*self.average_daily_income*self.days)
    return str(amount.quantize(decimal_places))













def estimator(data):
  return data
