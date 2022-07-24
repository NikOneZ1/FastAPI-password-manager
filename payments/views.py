from datetime import datetime

import stripe
from fastapi import APIRouter, HTTPException, status, Header, Depends
from fastapi.responses import RedirectResponse

from core.settings import STRIPE_API_KEY, BASE_URL, STRIPE_WEBHOOK_SECRET
from payments.models import MemberAccount
from user.dependencies import get_current_user
from user.models import User

router = APIRouter()
stripe.api_key = STRIPE_API_KEY


@router.post("/create-checkout-session")
async def create_checkout_session(price_id: str, user: User = Depends(get_current_user)):
    try:
        price = stripe.Price.retrieve(price_id)
        member_account = await MemberAccount.objects.first(user=user)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=BASE_URL + '/payments/result?success=true&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=BASE_URL + '/payments/result?canceled=true',
            client_reference_id=member_account.id,
        )
        return checkout_session.url
        # return RedirectResponse(checkout_session.url)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )


@router.get("/result")
def result(success: bool, session_id: str | None = None):
    if success:
        return {"success": True, "session_id": session_id}
    else:
        return {"success": False}


@router.post("/create-portal-session")
async def customer_portal(user: User = Depends(get_current_user)):
    member_account = await MemberAccount.objects.first(user=user)
    portal_session = stripe.billing_portal.Session.create(
        customer=member_account.customer_id,
        return_url=BASE_URL + '/users/me'
    )
    # return RedirectResponse(portal_session.url)
    return portal_session.url


@router.post("/webhook")
async def webhook(data: dict, stripe_signature: str | None = Header(default=None)):
    webhook_secret = STRIPE_WEBHOOK_SECRET

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = stripe_signature
        print(signature)
        try:
            event = stripe.Webhook.construct_event(
                payload=data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        event_type = data['type']
    data_object = data['data']['object']

    if event_type == 'checkout.session.completed':
        client_reference_id = data_object['client_reference_id']
        member_account = await MemberAccount.objects.get(id=int(client_reference_id))
        customer_id = data_object['customer']
        subscription_id = data_object['subscription']
        await member_account.update(customer_id=customer_id, subscription_id=subscription_id, is_member=True)

    if event_type == 'customer.subscription.deleted':
        subscription_id = data_object['id']
        member_account = await MemberAccount.objects.get(subscription_id=subscription_id)
        await member_account.update(is_member=False, subscription_id=None, membership_end_date=None)

    if event_type == 'customer.subscription.updated':
        subscription_current_period_end = datetime.fromtimestamp(data_object.get('current_period_end'))
        subscription_id = data_object['id']
        member_account = await MemberAccount.objects.get(subscription_id=subscription_id)
        customer_id = data_object['customer']
        await member_account.update(customer_id=customer_id, subscription_id=subscription_id, is_member=True,
                                    membership_end_date=subscription_current_period_end)
