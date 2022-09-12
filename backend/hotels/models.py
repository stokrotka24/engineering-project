from django.core.validators import MinValueValidator, MaxValueValidator
from djongo import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from common.utils.id import ID_LEN, random_id


class WiFi(ChoiceEnum):
    no = "no"
    free = "free"
    paid = "paid"


class NoiseLevel(ChoiceEnum):
    quiet = "quiet"
    average = "average"
    loud = "loud"
    very_loud = "very_loud"


class RestaurantsAttire(ChoiceEnum):
    dressy = "dressy"
    casual = "casual"
    formal = "formal"


class Music(models.Model):
    dj = models.NullBooleanField()
    background_music = models.NullBooleanField()
    no_music = models.NullBooleanField()
    jukebox = models.NullBooleanField()
    live = models.NullBooleanField()
    video = models.NullBooleanField()
    karaoke = models.NullBooleanField()

    class Meta:
        abstract = True


class Parking(models.Model):
    garage = models.NullBooleanField()
    street = models.NullBooleanField()
    validated = models.NullBooleanField()
    lot = models.NullBooleanField()
    valet = models.NullBooleanField()

    class Meta:
        abstract = True


class GoodForMeal(models.Model):
    breakfast = models.NullBooleanField()
    brunch = models.NullBooleanField()
    lunch = models.NullBooleanField()
    dinner = models.NullBooleanField()
    latenight = models.NullBooleanField()
    dessert = models.NullBooleanField()

    class Meta:
        abstract = True


class BYOBCorkage(ChoiceEnum):
    no = "no"
    yes_corkage = "yes_corkage"
    yes_free = "yes_free"


class Smoking(ChoiceEnum):
    outdoor = "outdoor"
    yes = "yes"
    no = "no"


class Alcohol(ChoiceEnum):
    none = "none"
    full_bar = "full_bar"
    beer_and_wine = "beer_and_wine"


class BestNights(models.Model):
    monday = models.NullBooleanField()
    tuesday = models.NullBooleanField()
    wednesday = models.NullBooleanField()
    thursday = models.NullBooleanField()
    friday = models.NullBooleanField()
    saturday = models.NullBooleanField()
    sunday = models.NullBooleanField()

    class Meta:
        abstract = True


class Ambience(models.Model):
    touristy = models.NullBooleanField()
    hipster = models.NullBooleanField()
    romantic = models.NullBooleanField()
    divey = models.NullBooleanField()
    intimate = models.NullBooleanField()
    trendy = models.NullBooleanField()
    upscale = models.NullBooleanField()
    classy = models.NullBooleanField()
    casual = models.NullBooleanField()

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        abstract = True


class Attributes(models.Model):
    businessAcceptsCreditCards = models.NullBooleanField()
    wiFi = EnumChoiceField(WiFi)
    restaurantsPriceRange2 = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)
        ],
        null=True
    )
    byAppointmentOnly = models.NullBooleanField()
    restaurantsDelivery = models.NullBooleanField()
    restaurantsGoodForGroups = models.NullBooleanField()
    goodForKids = models.NullBooleanField()
    outdoorSeating = models.NullBooleanField()
    restaurantsReservations = models.NullBooleanField()
    hasTV = models.NullBooleanField()
    restaurantsTakeOut = models.NullBooleanField()
    noiseLevel = EnumChoiceField(NoiseLevel)
    restaurantsAttire = EnumChoiceField(RestaurantsAttire)
    businessAcceptsBitcoin = models.NullBooleanField()
    music = models.EmbeddedField(
        model_container=Music
    )
    businessParking = models.EmbeddedField(
        model_container=Parking
    )
    goodForMeal = models.EmbeddedField(
        model_container=GoodForMeal
    )
    BYOBCorkage = EnumChoiceField(BYOBCorkage)
    smoking = EnumChoiceField(Smoking)
    BYOB = models.NullBooleanField()
    restaurantsTableService = models.NullBooleanField()
    caters = models.NullBooleanField()
    alcohol = EnumChoiceField(Alcohol)
    dogsAllowed = models.NullBooleanField()
    wheelchairAccessible = models.NullBooleanField()
    happyHour = models.NullBooleanField()
    goodForDancing = models.NullBooleanField()
    bestNights = models.EmbeddedField(
        model_container=BestNights
    )
    ambience = models.EmbeddedField(
        model_container=Ambience
    )
    coatCheck = models.NullBooleanField()
    bikeParking = models.NullBooleanField()
    corkage = models.NullBooleanField()
    driveThru = models.NullBooleanField()
    open24Hours = models.NullBooleanField()
    acceptsInsurance = models.NullBooleanField()
    restaurantsCounterService = models.NullBooleanField()

    class Meta:
        abstract = True


class Hotel(models.Model):
    id = models.CharField(max_length=ID_LEN, default=random_id, unique=True, primary_key=True)
    name = models.CharField(max_length=64, unique=False)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=8)
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    stars = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review_count = models.PositiveIntegerField(default=0)
    categories = models.ArrayField(
        model_container=Category
    )
    attributes = models.EmbeddedField(
        model_container=Attributes,
        null=True
    )


class Review(models.Model):
    id = models.CharField(max_length=ID_LEN, default=random_id, unique=True, primary_key=True)
    user_id = models.CharField(max_length=ID_LEN)
    hotel_id = models.CharField(max_length=ID_LEN)
    stars = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    date = models.DateField()
    content = models.CharField(max_length=5000)
