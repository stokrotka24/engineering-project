import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from djongo import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from common.utils import round_float_to_half
from django.apps import apps


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
    name = models.CharField(max_length=64, unique=False)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=8)
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    stars = models.DecimalField(
        default=0.0,
        max_digits=2,
        decimal_places=1)
    review_count = models.PositiveIntegerField(default=0)
    categories = models.ArrayField(
        model_container=Category
    )
    attributes = models.EmbeddedField(
        model_container=Attributes,
        null=True
    )


class Review(models.Model):
    user_id = models.PositiveIntegerField()
    hotel_id = models.PositiveIntegerField()
    stars = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    date = models.DateTimeField(default=datetime.datetime.now)
    content = models.CharField(max_length=5000, blank=True)

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        update_hotel_statistics(self.hotel_id)
        update_user_statistics(self.user_id)

    def delete(self, *args, **kwargs):
        super(Review, self).delete()
        update_hotel_statistics(self.hotel_id)
        update_user_statistics(self.user_id)


class Recommendation(models.Model):
    hotel_id = models.PositiveIntegerField()

    class Meta:
        abstract = True


def update_user_statistics(user_id):
    User = apps.get_model('authorization.User')

    stars_list = list(Review.objects.filter(user_id=user_id).values_list('stars', flat=True))
    stars_sum = sum(stars_list)
    stars_num = len(stars_list)
    user = User.objects.get(pk=user_id)
    if stars_num == 0:
        user.average_stars = 0.0
    else:
        user.average_stars = stars_sum / stars_num
    user.review_count = stars_num
    user.save()


def update_hotel_statistics(hotel_id):
    stars_list = list(Review.objects.filter(hotel_id=hotel_id).values_list('stars', flat=True))
    stars_sum = sum(stars_list)
    stars_num = len(stars_list)
    hotel = Hotel.objects.get(pk=hotel_id)
    hotel.latitude = str(hotel.latitude)
    hotel.longitude = str(hotel.longitude)
    if stars_num == 0:
        hotel.stars = 0.0
    else:
        hotel.stars = round_float_to_half(stars_sum / stars_num)
    hotel.review_count = stars_num
    hotel.save()


def get_recommendations_for_new_user():
    hotel_ids = list(Hotel.objects.order_by('-stars').values_list('id', flat=True))
    return [{"hotel_id": hotel_id} for hotel_id in hotel_ids]
