from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SubscriptionPlan

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionPlansView(TemplateView):
    template_name = 'subscriptions/plans.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = SubscriptionPlan.objects.filter(is_active=True)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        return context

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plan_id = self.kwargs["plan_id"]
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': plan.stripe_price_id,
                        'quantity': 1,
                    }
                ],
                mode='subscription',
                success_url=request.build_absolute_uri(
                    reverse('subscription_success')
                ) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('subscription_cancel')),
                metadata={
                    "user_id": request.user.id,
                    "plan_id": plan.id
                }
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return redirect(reverse('subscription_error'))