from rest_framework.response import Response
from rest_framework.views import APIView


class BRAPIView(APIView):
    
    def get_queryset(self, **kwargs):
        return None
        
    def filter_criteria(self, request, queryset):
        return queryset
        
    def get_many(self):
        return False
        
    def get_serializer_class(self, **kwargs):
        return None
        
    def create_response(self, request, queryset):
        return {}
        
    def is_valid(self, request):
        return True
        
    def create_post_response(self, request, data, *args, **kwargs):
        return {}
        
    def handle_post(self, request):
        return None

    def get(self, request, format=None):
        queryset = self.get_queryset()
        queryset = self.filter_criteria(request, queryset)
        created_response = self.create_response(request, queryset)
        if created_response:
            return Response(created_response)
        else:
            many = self.get_many()
            serializer_class = self.get_serializer_class()
            if serializer_class:
                rendered_response = serializer_class(queryset=queryset, many=many)
                return Response(rendered_response.data)
            return Response({})
            
    def post(self, request):
        valid = self.is_valid(request)
        if valid:
            post_processed = self.handle_post(request)
            if post_processed:
                post_response = self.create_post_response(request, post_processed)
                return Response(post_response)
            else:
                return Response({})
        return Response({ 'status': 'Failure', 'message': 'Validation Failed' })
            