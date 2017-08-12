from rest_framework.reverse import reverse
from rest_framework.views import APIView


class FitBitLoginView(APIView):
    def get(self, request):
        return reverse('fitbit-login')
