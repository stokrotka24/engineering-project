from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField


class AttributeValue(ChoiceEnum):
    no_data = "no_data"
    false = "false"
    true = "true"


# Hotel będzie miał w profilu algorytmicznym np. wifi.free = 1 i wifi.paid = wifi.no = wifi.no_data = 0,
# jeżeli user będzie miał najwyższy wskaźnik dla wifi.no_data, to znaczy, że dla niego obecność wifi
# lub jego brak nie ma znaczenia
class WifiValue(ChoiceEnum):
    no_data = "no_data"
    no = "no"
    free = "free"
    paid = "paid"


class RestaurantsPriceRange(ChoiceEnum):
    no_data = "no_data"
    one = "1"
    two = "2"
    three = "3"
    four = "4"


class NoiseLevel(ChoiceEnum):
    no_data = "no_data"
    quiet = "quiet"
    average = "average"
    loud = "loud"
    very_loud = "very_loud"


class RestaurantsAttire(ChoiceEnum):
    no_data = "no_data"
    dressy = "dressy"
    casual = "casual"
    formal = "formal"


class Music(models.Model):
    dj = models.BooleanField()
    background_music = models.BooleanField()
    no_music = models.BooleanField()
    jukebox = models.BooleanField()
    live = models.BooleanField()
    video = models.BooleanField()
    karaoke = models.BooleanField()


# class Attributes(models.Model):
#     businessAcceptsCreditCards = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     wiFi = EnumChoiceField(WifiValue, default=WifiValue.no_data)
#     restaurantsPriceRange2 = EnumChoiceField(RestaurantsPriceRange, RestaurantsPriceRange.no_data)
#     byAppointmentOnly = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     restaurantsDelivery = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     restaurantsGoodForGroups = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     goodForKids = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     outdoorSeating = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     restaurantsReservations = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     hasTV = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     restaurantsTakeOut = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     noiseLevel = EnumChoiceField(NoiseLevel, default=NoiseLevel.no_data)
#     restaurantsAttire = EnumChoiceField(RestaurantsAttire, default=RestaurantsAttire.no_data)
#     businessAcceptsBitcoin = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     dj = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#
#     backgroundMusic = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     noMusic = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     jukebox = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     live = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     video = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#     karaoke = EnumChoiceField(AttributeValue, default=AttributeValue.no_data)
#
#     parkingGarage
#     parkingStreet
#     parkingValidated
#     parkingLot
#     parkingValet
