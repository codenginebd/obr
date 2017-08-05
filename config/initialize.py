# Initialize Book Languages
from book_rental.models.language import BookLanguage

BOOK_LANGUAGES = [ 
    {
        'short_name': 'en',
        'long_name': 'English'
    },
    {
        'short_name': 'bn',
        'long_name': 'Bangla'
    }
]

def init_book_languages():
    for lang in BOOK_LANGUAGES:
        blang_objects = BookLanguage.objects.filter(short_name=lang['short_name'])
        if blang_objects.exists():
            blang_object = blang_objects.first()
        else:
            blang_object = BookLanguage(short_name=lang['short_name'])
            
        blang_object.name = lang['long_name']
        blang_object.save()
        
#init_book_languages()

# Initialize Book Rental Plans
from generics.models.sales.rent_plan import RentPlan

def init_rent_plans():

    RENT_DAYS = [ 7, 10, 15, 20, 30, 45, 60, 75, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360 ]

    RENT_PLANS = []

    for rday in RENT_DAYS:
        name = '%s_DAY_PLAN' % rday
        rent_plan_objects = RentPlan.objects.filter(days=rday)
        if rent_plan_objects.exists():
            rent_plan_object = rent_plan_objects.first()
        else:
            rent_plan_object = RentPlan(days=rday)
        rent_plan_object.name = name
        rent_plan_object.save()

#init_rent_plans()


