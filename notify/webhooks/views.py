from rest_framework import views, response, status
from webhooks.models import Webhook
from webhooks.messages import outflow_message
from services.callmebot import CallMeBot
import json

class WebhookOrderView(views.APIView):

    def post(self, request):
        data = request.data

        # Salvar o evento do webhook
        Webhook.objects.create(
            event_type=data.get('event_type'),
            event=json.dumps(data, ensure_ascii=False)
        )

        product_name = data.get('product')
        quantity = data.get('quantity')
        product_cost_price = data.get('product_cost_price')
        product_selling_price = data.get('product_selling_price')

        # Verificar se os valores não são None
        if product_selling_price is not None and quantity is not None and product_cost_price is not None:
            total_value = product_selling_price * quantity
            profit_value = total_value - (product_cost_price * quantity)

            # print(f'teste2: {product_name} - {quantity} - {product_cost_price} - {product_selling_price} - {total_value} - {profit_value}')

            message = outflow_message.format(
                product_name,
                quantity,
                total_value,
                profit_value
            )
            # print('message', message)
            callmebot = CallMeBot()
            callmebot.send_message(message)

            return response.Response(
                data=data,
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                data={"error": "Valores de produto, quantidade ou preço são inválidos"},
                status=status.HTTP_400_BAD_REQUEST,
            )
