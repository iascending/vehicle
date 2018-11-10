import os
import uuid
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','vehicle.settings')

import django
# Import settings
django.setup()

import random
from cars.models import Car, Driver, DrivingRecord
from faker import Faker

fakegen = Faker()

car_makes = ['Volkswagon', 'Hyundai', 'Mercedes-benz', 'Bmw']
car_years = [str(x) for x in range(2008, 2019)]
car_models = ['Caddy', 'X5', 'Camry', 'Golf', 'Forest']
car_types = ['Van', 'Ute', 'Sedan', 'Truck']
car_colors = ['White', 'Black', 'Red', 'Gray']
car_trans  = ['Automatic', 'Manual']
car_status = ['A', 'I', 'S']
driver_depts = ['BG', 'WG', 'BL', 'AC', 'CC', 'IT', 'MG', 'SP', 'HHP', 'BDM']

def add_file(subfolder):
    media_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
    file_name = str(uuid.uuid4()) + '.txt'
    rltv_name = os.path.join(subfolder, file_name)
    full_name = os.path.join(media_path, rltv_name)
    with open(full_name, 'w') as f:
        f.write(full_name)
    print(rltv_name)
    return str(rltv_name)

def add_car():
    t = Car.objects.get_or_create(
                make = random.choice(car_makes),
                year = random.choice(car_years),
                model = random.choice(car_models),
                type = random.choice(car_types),
                color = random.choice(car_colors),
                rego = ''.join(fakegen.random_letters(6)).upper(),
                engine_no = ''.join(fakegen.random_letters(15)).lower(),
                vin  = ''.join(fakegen.random_letters(15)).lower(),
                transmission = random.choice(car_trans),
                options = fakegen.random_letter(),
                maintenance_status = fakegen.random_letter(),
                lease_start_date = fakegen.date_this_decade(),
                lease_term = fakegen.random_int(),
                rental = fakegen.random_number()/1000,
                distance_restrict = fakegen.random_number()/1000,
                start_odometer = fakegen.random_number()/1000,
                excess_kmcharge = fakegen.random_number()/1000,
                default_interest = fakegen.random_number()/1000,
                lessor = fakegen.company(),
                status = random.choice(car_status),
                rego_exp = fakegen.date_this_month(),
                insurer = fakegen.company(),
                policy_num = fakegen.random_int(),
                insurance_exp = fakegen.date_this_month(),
                fuel_efficiency = fakegen.random_number()/1000,
                contract = add_file('contracts')
                # file_upload_date = fakegen.date_this_year()
        )[0]

    t.save()
    return t

def add_driver():
    t = Driver.objects.get_or_create(
        name = fakegen.first_name() + ' ' + fakegen.last_name(),
        mobile = fakegen.random_number(11),
        license = fakegen.random_number(10),
        email  = fakegen.email(),
        dept = random.choice(driver_depts) )[0]

    t.save()
    return t


def populate(N=2):
    '''
    Create N Entries of Dates Accessed
    '''
    for entry in range(N):
        # car_obj = add_car()
        # driver_obj = add_driver()

if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate(20)
    print('Populating Complete')
