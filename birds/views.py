from rest_framework.response import Response
from rest_framework import generics, status

from .models import *
from .serializers import *


class Birds(generics.GenericAPIView):
    serializer_class = BirdSerializer
    queryset = Bird.objects.all()

    def get(self, request):
        """
        Получение записей Bird
        """

        page_num = int(request.GET.get('page', 1))
        limit_num = int(request.GET.get('limit', 10))

        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num

        name_param = request.GET.get('name')

        birds = Bird.objects.all()

        if name_param:
            birds = birds.filter(name__icontains=name_param)
        serializer = self.serializer_class(birds[start_num:end_num], many=True)

        return Response({
            "status": "success",
            "page": page_num,
            "birds": serializer.data
        })

    def post(self, request):
        """
        Добавление записи Bird
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"bird": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BirdDetail(generics.GenericAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer

    def get_bird(self, bird_id):
        try:
            bird = Bird.objects.get(id=bird_id)
            return bird
        except:
            return None

    def get(self, request, bird_id):
        """
        Получение записи Bird
        """
        bird = self.get_bird(bird_id)
        if bird is None:
            return Response({"status": "fail", "message": f"Bird with Id: {bird_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bird)
        return Response({"status": "success", "data": {"bird": serializer.data}})

    def patch(self, request, bird_id):
        """
        Обновление записи Bird
        """
        bird = self.get_bird(bird_id)
        if bird is None:
            return Response({"status": "fail", "message": f"Bird with Id: {bird_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bird, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"bird": serializer.data}})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bird_id):
        """
        Удаление записи Bird
        """
        bird = self.get_bird(bird_id)
        if bird is None:
            return Response({"status": "fail", "message": f"Bird with Id: {bird_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        bird.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BirdSeenTotal(generics.GenericAPIView):
    def get_bird(self, bird_id):
        try:
            bird = Bird.objects.get(id=bird_id)
            return bird
        except:
            return None

    def get(self, request, bird_id):
        """
        Получение количества записей BirdSeen по bird_id
        """

        bird = self.get_bird(bird_id=bird_id)

        if bird is not None:
            seen_total = BirdSeen.objects.filter(bird_id=bird_id).count()

            return Response({
                "status": "success",
                "bird_id": bird_id,
                "seen_total": seen_total
            })

        return Response({"status": "fail", "message": f"Bird with Id: {bird_id} not found"},
                        status=status.HTTP_404_NOT_FOUND)


class BirdSeens(generics.GenericAPIView):
    serializer_class = BirdSeenSerializer
    queryset = Bird.objects.all()

    def get(self, request):
        """
        Получение записей BirdSaw
        """

        page_num = int(request.GET.get('page', 1))
        limit_num = int(request.GET.get('limit', 10))

        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num

        user_param = request.GET.get('user')

        birdseens = BirdSeen.objects.all()

        if user_param:
            birdseens = birdseens.filter(user_id=user_param)
        serializer = self.serializer_class(birdseens[start_num:end_num], many=True)

        return Response({
            "status": "success",
            "page": page_num,
            "bird_seens": serializer.data
        })

    def post(self, request):
        """
        Добавление записи BirdSaw
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"bird_seen": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BirdSeenDetail(generics.GenericAPIView):
    queryset = BirdSeen.objects.all()
    serializer_class = BirdSeenSerializer

    def get_birdseen(self, birdseen_id):
        try:
            return BirdSeen.objects.get(id=birdseen_id)
        except:
            return None

    def get(self, request, birdseen_id):
        """
        Получение записи BirdSeen
        """
        birdseen = self.get_birdseen(birdseen_id)
        if birdseen is None:
            return Response({"status": "fail", "message": f"Bird seen with Id: {birdseen_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(birdseen)
        return Response({"status": "success", "data": {"bird_seen": serializer.data}})

    def patch(self, request, birdseen_id):
        """
        Обновление записи BirdSeen
        """
        birdseen = self.get_birdseen(birdseen_id)
        if birdseen is None:
            return Response({"status": "fail", "message": f"Bird Seen with Id: {birdseen_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(birdseen, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"bird_seen": serializer.data}})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, birdseen_id):
        """
        Удаление записи BirdSeen
        """
        birdseen = self.get_birdseen(birdseen_id)
        if birdseen is None:
            return Response({"status": "fail", "message": f"Bird Seen with Id: {birdseen_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        birdseen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
