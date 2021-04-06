from database import Batiment
from open_data import IrisConsumption

def ratio_for_iris(dispatch,consumption_by_housing_type,dict_iris_consumption):
    total_theo_consumption = 0
    for key,number_housing in dispatch.items():
        total_theo_consumption += number_housing * consumption_by_housing_type[key]
    print(total_theo_consumption,dict_iris_consumption[iris_code])
    if total_theo_consumption != 0:
        return dict_iris_consumption[iris_code] / total_theo_consumption
    else:
        return 0

if __name__ == '__main__':

    consumption_by_housing_type = {
        'h_new' : 23.5,
        'h_old' : 26.0,
        'c_new' : 13.0,
        'c_old' : 17.0,

    }

    iris_consumption = IrisConsumption(75,2019)
    dict_iris_consumption = iris_consumption.consumption_by_iris()

    batiment = Batiment("Energy")
    dict_dispatch = batiment.housing_by_iris2()
    for iris_code,dispatch in dict_dispatch.items():
        dict_dispatch[iris_code]['ratio'] = ratio_for_iris(dispatch,consumption_by_housing_type,dict_iris_consumption)

    print(dict_dispatch)
    print(batiment.get_batiments_consumption(consumption_by_housing_type,dict_dispatch)[0])
    list_batiments = batiment.get_batiments_consumption(consumption_by_housing_type,dict_dispatch)




