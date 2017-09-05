from rest_framework.views import APIView

class BRAPIView(APIView):
    
    def get_queryset(self, **kwargs):
        return None
        
    def filter_criteria(self, request, queryset):
        return queryset
        
    def get_many(self):
        return False
        
    def get_serializer_class(self, request, queryset, **kwargs):
        return None
        
    def create_response(self, request, queryset):
        return {}

    def get(self, request, format=None):
        queryset = self.get_queryset(**kwargs)
        queryset = self.filter_criteria(request, queryset)
        created_response = self.create_response(request, queryset)
        if created_response:
            return Response(created_response)
        else:
            many = self.get_many()
            serializer_class = self.get_serializer_class()
            rendered_response = serializer_class(queryset=queryset, many=many)
            return Response(rendered_response)