from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegisterForm, ShippingForm, EditProfileForm, EditAccountForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CartForAuthenticatedUser, get_cart_data
import stripe
from config.settings import STRIPE_SECRET_KEY
from django.contrib.auth.decorators import login_required
from .mixins import CategoryMixin


def get_categories():
    return Category.objects.all()

class ProductList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'digitalstore/main.html'
    extra_context = {
        'title': 'Digitalstore-вся техника с низкими ценами'
    }

    def get_queryset(self):
        return Category.objects.all


class ProductDetail(CategoryMixin, DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        same_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)
        color_variants = Product.objects.filter(title=product.title).exclude(pk=product.pk)

        context['title'] = product.title
        context['products'] = same_products[::-1]
        context['color_variants'] = color_variants
        return context


class ProductByCategory(CategoryMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digitalstore/category_products.html'
    paginate_by = 3

    def get_queryset(self):
        sub = self.request.GET.get('sub')
        color_name = self.request.GET.get('color')
        price_from = self.request.GET.get('from')
        price_to = self.request.GET.get('to')

        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)
        if sub:
            products = products.filter(model__title=sub)
        if color_name:
            products = products.filter(color_name=color_name)
        if price_from:
            products = [i for i in products if int(i.price) >= int(price_from)]
        if price_to:
            products = [i for i in products if int(i.price) <= int(price_to)]
        return products[::-1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_params'] = self.request.GET.urlencode()
        context['categories'] = Category.objects.all()
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)
        models = set(product.model for product in products)
        colors = list(set([i.color_name for i in products]))
        prices = [i for i in range(1000000, 30000000, 1000000)]
        context['title'] = f'DIGITALSTORE - {category.title}'
        context['colors'] = colors
        context['prices'] = prices
        context['current_category'] = category.title
        context['models'] = models
        return context


def login_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('main')
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация',
            'form': form,
            'categories': get_categories(),
        }

        return render(request, 'digitalstore/login.html', context)


def logout_user_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('main')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                image = form.cleaned_data.get('image')
                profile = Profile.objects.create(user=user, image=image)
                profile.save()
                customer = Customer.objects.create(user=user)
                customer.save()
                return redirect('login')

        else:
            form = RegisterForm()

        context = {
            'title': 'Регистрация',
            'form': form,
            'categories': get_categories(),
        }

        return render(request, 'digitalstore/register.html', context)


def save_favorite_product(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        product = Product.objects.get(slug=slug)
        user = request.user
        favorite_products = FavoriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorite_products]:
                fav_product = FavoriteProduct.objects.get(user=user, product=product)
                fav_product.delete()
            else:
                FavoriteProduct.objects.create(user=user, product=product)

        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


class FavoriteListView(LoginRequiredMixin, CategoryMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'digitalstore/product_list.html'
    login_url = 'login'
    extra_context = {
        'title': 'Избранное'
    }

    def get_queryset(self):
        favorites = FavoriteProduct.objects.filter(user=self.request.user)
        products = [i.product for i in favorites]
        return products


def add_or_delete_product_view(request, slug, action):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = CartForAuthenticatedUser(request, slug, action)
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


def my_cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order_info = get_cart_data(request)
        order_products = order_info['order_products']
        context = {
            'title': 'Моя Корзина',
            'order_total_price': order_info['order_total_price'],
            'order_total_quantity': order_info['order_total_quantity'],
            'order_products': order_products,
            'products': Product.objects.all().order_by('-created_at'),
            'categories': get_categories(),
        }

        return render(request, 'digitalstore/my_cart.html', context)


def delete_product(request, pk, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order = Order.objects.get(pk=order_id)
        if order.customer.user == request.user:
            order_product = OrderProduct.objects.get(pk=pk, order=order)
            order_product.delete()
        order_products = order.orderproduct_set.all()
        if not order_products:

            return render(request, 'digitalstore/my_cart.html', {
                'title': 'Моя Корзина',
                'message': 'Ваша корзина пуста',
                'categories': get_categories(),
            })
        return redirect('my_cart')


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order_info = get_cart_data(request)
        if order_info['order_products']:

            context = {
                'title': 'Оформление заказа',
                'order': order_info['order'],
                'items': order_info['order_products'],
                'form': ShippingForm(),
                'categories': get_categories(),
            }

            return render(request, 'digitalstore/checkout.html', context)


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        if request.method == 'POST':
            order_info = get_cart_data(request)
            shipping_form = ShippingForm(data=request.POST)
            shipping_address = ShippingAddress.objects.all()
            if shipping_form.is_valid():
                shipping = shipping_form.save(commit=False)
                shipping.customer = Customer.objects.get(user=request.user)
                shipping.order = order_info['order']
                if order_info['order'] in [i.order for i in shipping_address]:
                    ship_order = ShippingAddress.objects.get(order=order_info['order'])
                    ship_order.delete()

                shipping.save()
            else:
                return redirect('checkout')
            order_price = order_info['order_total_price']
            exchange_rate = 13000
            order_price_usd = order_price / exchange_rate
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Товары магазина Digitalstore'},
                        'unit_amount': int(order_price_usd * 100)
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('checkout'))
            )

            return redirect(session.url)


def success_payment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart = CartForAuthenticatedUser(request)
        if cart.get_cart_info()['order'] and cart.get_cart_info()['order_products']:
            shipping = ShippingAddress.objects.all()
            if cart.get_cart_info()['order'] in [i.order for i in shipping]:
                order = cart.get_cart_info()['order']
                order_save = SaveOrder.objects.create(customer=Customer.objects.get(user=request.user),
                                                      total_price=order.get_order_total_price,
                                                      order_number=order.pk)
                order_save.save()
                order_products = cart.get_cart_info()['order_products']
                for item in order_products:
                    save_order_products = SaveOrderProduct.objects.create(order_id=order_save.pk,
                                                                          product=item.product.title,
                                                                          quantity=item.quantity,
                                                                          product_slug=item.product.slug,
                                                                          price=item.product.get_price(),
                                                                          price_in=item.get_total_price,
                                                                          photo=item.product.get_first_photo(),
                                                                          color_name=item.product.color_name)
                    save_order_products.save()

                cart.make_payment()
                context = {
                    'title': 'Успешная оплата',
                    'categories': get_categories(),
                }

                return render(request, 'digitalstore/success.html', context)

            else:
                return redirect('main')
        else:
            return redirect('main')


class SearchProduct(CategoryMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digitalstore/main.html'

    def get_queryset(self):
        word = self.request.GET.get('q', '').strip()
        if word:

            return Product.objects.filter(title__icontains=word)
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@login_required
def profile_view(request):

    customer = Customer.objects.filter(user=request.user).first()
    orders = SaveOrder.objects.filter(customer=customer).order_by('-created_at')
    context = {
        'title': 'Ваш профиль',
        'orders': orders,
        'categories': get_categories(),
    }

    return render(request, 'digitalstore/profile.html', context)


def orders_list(request):
    customer = Customer.objects.get(user=request.user)
    context = {
        'orders': SaveOrder.objects.filter(customer=customer).order_by('-pk'),
        'title': 'Мои заказы',
        'categories': get_categories(),
    }
    return render(request, 'digitalstore/orders_list.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        account_form = EditAccountForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and account_form.is_valid():
            profile_form.save()
            account_form.save()
            return redirect('profile')
    else:
        account_form = EditAccountForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'title': 'Редактировать профиль',
        'account_form': account_form,
        'profile_form': profile_form,
        'categories': get_categories(),
    }

    return render(request, 'digitalstore/edit_profile.html', context)







