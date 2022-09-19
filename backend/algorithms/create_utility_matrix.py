import numpy as np
from hotels.models import Hotel, Review
from authorization.models import User

# rows - users
# cols - hotels
no_users = User.objects.count()
no_hotels = Hotel.objects.count()
reviews = Review.objects.all()

print(no_users)
print(no_hotels)
utility_matrix = np.zeros([no_users, no_hotels])
utility_matrix[0][0] = 5
# utility_matrix = np.random.random((no_users, no_hotels))
print(utility_matrix)

