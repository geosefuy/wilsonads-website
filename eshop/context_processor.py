from .models import *

# Used in rendering categories/subcategories in navbar 
def product_categories(req):
	categories = Category.objects.all()
	return {'categories': categories}
