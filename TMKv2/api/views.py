from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, TeamSerializer, MatchSerializer
from users.models import Profile, User
from sportsdb.models import Team, Match
from datetime import date
from django.db.models import Q
from django.shortcuts import get_object_or_404

class UserView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            profile = Profile.objects.filter(id=pk).first()
            if profile:
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)    

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                team_ids = request.data.pop('teams', [])
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    profile = Profile.objects.get(user=user)
                    profile.teams.set(team_ids)
                    return Response({"message": "User created successfully"}, status=201)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
            
    def put(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, id=pk)        
        with transaction.atomic():
            try:
                team_ids = request.data.pop('teams', [])
                serializer = UserSerializer(instance=user, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    profile = Profile.objects.get(user=user)
                    profile.teams.set(team_ids)
                    return Response({"message": "User updated successfully"}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        with transaction.atomic():
            if not pk:
                return Response({"message": "Method DELETE is not allowed without an ID."}, status=status.HTTP_400_BAD_REQUEST)
            profile = Profile.objects.filter(id=pk).first()
            if profile:
                profile.delete()
                return Response({"message": "User deleted."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class TeamView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                team = Team.objects.get(teamid=pk)
            except:
                return Response({"error": "Team not found"}, status=404)
            last_10_matches = Match.objects.filter(
                (Q(hometeamid=pk) | Q(awayteamid=pk)) & Q(date__lt=date.today())
                ).order_by('-date')[:10]

            team_serializer = TeamSerializer(team, many=False)
            matches_serializer = MatchSerializer(last_10_matches, many=True)
            response_data = {
                'team': team_serializer.data,
                'last_10_matches': matches_serializer.data
            }
            return Response(response_data)
        else:
            teams = Team.objects.filter(primaryleague__teamdata=True)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)