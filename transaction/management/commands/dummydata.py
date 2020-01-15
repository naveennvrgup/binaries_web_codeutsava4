from transaction.models import *
from user.models import *
from django.core.management.base import BaseCommand, CommandError
import random
import math
import lorem
import datetime



class Command(BaseCommand):
    help = 'Creates the dummy data for the project'
    choices = (
        ('FAR', 'Farmer'),
        ('BUY', 'Buyer'),
        ('WHO', 'Warehouse Owner'),
        ('NGO', 'NGO'),
        ('ADM', 'Admin'),
        ('DVR', 'Delivery Partner'),
    )

    users=[]
    admin_users=[]
    farmer_users=[]
    warhouse_owners=[]
    grains=[]
    locations=[]
    farms=[]
    warehouses=[]
    centres=[]
    demands=[]

    def oneword(self):
        return lorem.sentence().split()[0]

    def onenum(self,num):
        return str(math.ceil(random.random()*10**num))

    def inran(self,some):
        return some[random.randint(0,len(some)-1)]


    def create_users(self):
        User.objects.all().delete()
        for  x in self.choices:
            for i in range(10):
                name=self.oneword()+self.onenum(4)+self.oneword()
                if i==0:
                    name="ravi_"+x[0] 
                user = User.objects.create_user(
                    username=name,
                    name=name,
                    password="password",
                    contact=self.onenum(10),
                    address=lorem.sentence(),
                    city=self.oneword(),
                    state=self.oneword(),
                    dob='1998-1-12',
                    adhaar=self.onenum(12),
                    role=x[0]
                )
                if x[0]=='ADM':
                    self.admin_users.append(user)
                if x[0]=='FAR':
                    self.farmer_users.append(user)
                if x[0]=='WHO':
                    self.warhouse_owners.append(user)

                self.users.append(user) 
                print(user)

    def create_foodgrain(self):
        FoodGrain.objects.all().delete()
        for _ in range(30):
            grain = FoodGrain.objects.create(
                type=self.oneword()+self.onenum(3),
                life=random.randint(1,50)
            )
            self.grains.append(grain)
            print(grain)

    def create_location(self):
        Location.objects.all().delete()
        for x in range(100):
            location =  Location.objects.create(
                xloc=round(random.random()*100,2),
                yloc=round(random.random()*100,2),
                centre=self.centres[random.randint(0,9)]
            )
            self.locations.append(location)
            print(location)

    def create_centre(self):
        Centre.objects.all().delete()
        for x in range(10):
            centre = Centre.objects.create(
                cid=self.oneword()+self.onenum(5),
                admin=self.admin_users[x]
            )
            self.centres.append(centre)
            print(centre)

    def create_farms(self):
        Farms.objects.all().delete()

        for x in range(20):
            for i in range(4):
                farm=Farms.objects.create(
                    farmer=self.farmer_users[i],
                    location=self.locations[x*4+i]
                )
                self.farms.append(farm)
                print(farm)

    def create_warehouse(self):
        Warehouse.objects.all().delete()

        for i in range(5):
            warehouse=Warehouse.objects.create(
                owner=self.warhouse_owners[i],
                sector='PVT',
                foodgrain=self.grains[random.randint(0,len(self.grains)-1)],
                location=self.locations[-i],
                free_space=self.onenum(4),
                total_space=self.onenum(5)
            )
            self.warehouses.append(warehouse)
            print(warehouse)
        for i in range(5):
            warehouse=Warehouse.objects.create(
                owner=self.warhouse_owners[i+5],
                sector='PUB',
                foodgrain=self.grains[random.randint(0,len(self.grains)-1)],
                location=self.locations[-i-5],
                free_space=self.onenum(4),
                total_space=self.onenum(5)
            )
            self.warehouses.append(warehouse)
            print(warehouse)

    def create_demand(self):
        Demand.objects.all().delete()

        for grain in self.grains:
            demand=Demand.objects.create(
                foodgrain=grain,
                quantity=self.onenum(4),
                centre=self.centres[random.randint(0,len(self.centres)-1)]
            )
            self.demands.append(demand)
            print(demand)

    produces=[]
    def create_produce(self):
        Produce.objects.all().delete()

        for i in range(80):
            produce=Produce.objects.create(
                type=self.inran(self.grains),
                farmer=self.inran(self.farmer_users),
                grade=self.onenum(20),
                quantity=self.onenum(5),
                price=self.onenum(3),
                location=self.locations[i],
            )
            self.produces.append(produce)
            print(produce)


    bids=[]
    def create_bid(self):
        Bid.objects.all().delete()

        for _ in range(200):
            bid=Bid.objects.create(
                isActive=True if int(self.onenum(1))>3 else False,
                transno=self.oneword()+self.onenum(10)+self.oneword(),
                buyer=self.inran(self.users),
                type=self.inran(self.grains),
                quantity=int(self.onenum(4)),
                nbids=int(self.onenum(2)),
                description=lorem.paragraph(),
                deadline=datetime.datetime.now()+datetime.timedelta(days=int(self.onenum(2)))
            )
            self.bids.append(bid)
            print(bid)

    storageTransactions=[]
    def create_storageTransactions(self):
        StorageTransaction.objects.all().delete()
        
        for _ in range(200):
            st=StorageTransaction.objects.create(
                transno=self.oneword()+self.onenum(12),
                warehouse=self.inran(self.warehouses),
                farmer=self.inran(self.farmer_users),
                produce=self.inran(self.produces),
                quantity=int(self.onenum(3)),
                cost=int(self.onenum(2)),
                date=datetime.datetime.now(),
                valid=True
            )
            self.storageTransactions.append(st)
            print(st)

    def handle(self, *args, **options):
        self.create_users()
        self.create_foodgrain()
        self.create_centre()
        self.create_location()
        self.create_farms()
        self.create_warehouse()
        self.create_demand()
        self.create_produce()
        self.create_bid()
        self.create_storageTransactions()

        su=User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="password"
        )
        print(su.email)
        print()
        print()
        print()
        print()
        print("dummy data created successfully!!!")
    