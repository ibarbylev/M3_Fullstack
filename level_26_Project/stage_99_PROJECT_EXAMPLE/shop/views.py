from django.views import generic

from shop.models import Product


class HomeView(generic.ListView):
    model = Product
    template_name = 'home.html'

# Products
class ProductListView(generic.TemplateView):
    pass

class ProductSearchView(generic.TemplateView):
    pass

class ProductDetailView(generic.TemplateView):
    pass

class ProductReviewAddView(generic.TemplateView):
    pass

class ProductReviewListView(generic.TemplateView):
    pass


# Orders
class OrderListView(generic.TemplateView):
    pass

class OrderAddView(generic.TemplateView):
    pass

class OrderRemoveView(generic.TemplateView):
    pass

class OrderUpdateView(generic.TemplateView):
    pass

class OrderCheckoutView(generic.TemplateView):
    pass

class OrderDetailView(generic.TemplateView):
    pass

class OrderHistoryView(generic.TemplateView):
    pass


# Payments
class PaymentProcessView(generic.TemplateView):
    pass

class PaymentConfirmView(generic.TemplateView):
    pass

class PaymentCancelView(generic.TemplateView):
    pass


# Reviews
class ReviewAddView(generic.TemplateView):
    pass

class ReviewUpdateView(generic.TemplateView):
    pass

class ReviewDeleteView(generic.TemplateView):
    pass
