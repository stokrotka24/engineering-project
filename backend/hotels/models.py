from django.core.validators import MinValueValidator, MaxValueValidator
from djongo import models
from enumchoicefield import ChoiceEnum, EnumChoiceField

# from django.contrib.postgres.fields import ArrayField

from common.utils.id import ID_LEN, random_id


class AttributeValue(ChoiceEnum):
    null = "null"
    false = "false"
    true = "true"


# Hotel będzie miał w profilu algorytmicznym np. wifi.free = 1 i wifi.paid = wifi.no = wifi.null = 0,
# jeżeli user będzie miał najwyższy wskaźnik dla wifi.null, to znaczy, że dla niego obecność wifi
# lub jego brak nie ma znaczenia
class WifiValue(ChoiceEnum):
    null = "null"
    no = "no"
    free = "free"
    paid = "paid"


class RestaurantsPriceRange(ChoiceEnum):
    null = "null"
    one = "1"
    two = "2"
    three = "3"
    four = "4"


class NoiseLevel(ChoiceEnum):
    null = "null"
    quiet = "quiet"
    average = "average"
    loud = "loud"
    very_loud = "very_loud"


class RestaurantsAttire(ChoiceEnum):
    null = "null"
    dressy = "dressy"
    casual = "casual"
    formal = "formal"


class Music(models.Model):
    dj = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    background_music = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    no_music = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    jukebox = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    live = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    video = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    karaoke = EnumChoiceField(AttributeValue, default=AttributeValue.null)

    class Meta:
        abstract = True


class Parking(models.Model):
    garage = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    street = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    validated = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    lot = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    valet = EnumChoiceField(AttributeValue, default=AttributeValue.null)

    class Meta:
        abstract = True


class GoodForMeal(models.Model):
    breakfast = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    brunch = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    lunch = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    dinner = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    latenight = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    dessert = EnumChoiceField(AttributeValue, default=AttributeValue.null)

    class Meta:
        abstract = True


class BYOBCorkage(ChoiceEnum):
    null = "null"
    no = "no"
    yes_corkage = "yes_corkage"
    yes_free = "yes_free"


class Smoking(ChoiceEnum):
    null = "null"
    outdoor = "outdoor"
    yes = "yes"
    no = "no"


class Alcohol(ChoiceEnum):
    null = "null"
    full_bar = "full_bar"
    beer_and_wine = "beer_and_wine"


class BestNights(models.Model):
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()

    class Meta:
        abstract = True


class Ambience(models.Model):
    touristy = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    hipster = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    romantic = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    divey = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    intimate = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    trendy = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    upscale = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    classy = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    casual = EnumChoiceField(AttributeValue, default=AttributeValue.null)

    class Meta:
        abstract = True


class Attributes(models.Model):
    businessAcceptsCreditCards = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    wiFi = EnumChoiceField(WifiValue, default=WifiValue.null)
    restaurantsPriceRange2 = EnumChoiceField(RestaurantsPriceRange, RestaurantsPriceRange.null)
    byAppointmentOnly = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    restaurantsDelivery = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    restaurantsGoodForGroups = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    goodForKids = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    outdoorSeating = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    restaurantsReservations = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    hasTV = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    restaurantsTakeOut = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    noiseLevel = EnumChoiceField(NoiseLevel, default=NoiseLevel.null)
    restaurantsAttire = EnumChoiceField(RestaurantsAttire, default=RestaurantsAttire.null)
    businessAcceptsBitcoin = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    music = models.EmbeddedField(
        model_container=Music,
        null=True
    )
    businessParking = models.EmbeddedField(
        model_container=Parking,
        null=True
    )
    goodForMeal = models.EmbeddedField(
        model_container=GoodForMeal,
        null=True
    )
    BYOBCorkage = EnumChoiceField(BYOBCorkage, default=BYOBCorkage.null)
    smoking = EnumChoiceField(Smoking, default=Smoking.null)
    BYOB = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    restaurantsTableService = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    caters = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    alcohol = EnumChoiceField(Alcohol, default=AttributeValue.null)
    dogsAllowed = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    wheelchairAccessible = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    happyHour = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    goodForDancing = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    bestNights = models.EmbeddedField(
        model_container=BestNights,
        null=True
    )
    ambience = models.EmbeddedField(
        model_container=Ambience,
        null=True
    )
    coatCheck = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    bikeParking = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    corkage = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    driveThru = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    open24Hours = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    acceptsInsurance = EnumChoiceField(AttributeValue, default=AttributeValue.null)
    restaurantsCounterService = EnumChoiceField(AttributeValue, default=AttributeValue.null)

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
    review_count = models.PositiveIntegerField()
    # categories = ArrayField(models.CharField(max_length=32))
    # hours
    attributes = models.EmbeddedField(
        model_container=Attributes
    )
