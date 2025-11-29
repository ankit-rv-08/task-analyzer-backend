
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskInputSerializer, TaskOutputSerializer
from .scoring import STRATEGIES

class AnalyzeTasksView(APIView):
    def post(self, request):
        strategy = request.data.get('strategy', 'smart_balance')
        if strategy not in STRATEGIES:
            return Response({"error": f"Invalid strategy. Choose: {list(STRATEGIES.keys())}"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        tasks_data = request.data.get('tasks', [])
        serializer = TaskInputSerializer(data=tasks_data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = serializer.validated_data
        dependents_count = {t.get('id', str(idx)): 0 for idx, t in enumerate(tasks)}
        for t in tasks:
            for dep in t.get('dependencies', []):
                if dep in dependents_count:
                    dependents_count[dep] += 1

        score_fn = STRATEGIES[strategy]
        scored_tasks = []
        for idx, t in enumerate(tasks):
            tid = t.get('id', str(idx))
            score = score_fn(t, dependents_count[tid])
            t_out = dict(t)
            t_out['score'] = score
            t_out['strategy'] = strategy
            t_out['explanation'] = f"Scored using {strategy.replace('_', ' ').title()} strategy."
            t_out['id'] = tid
            scored_tasks.append(t_out)

        scored_tasks.sort(key=lambda x: x['score'], reverse=True)
        out_ser = TaskOutputSerializer(scored_tasks, many=True)
        return Response({
            'strategy': strategy,
            'tasks': out_ser.data
        }, status=status.HTTP_200_OK)

class SuggestTasksView(APIView):
    def post(self, request):
        strategy = request.data.get('strategy', 'smart_balance')
        if strategy not in STRATEGIES:
            return Response({"error": f"Invalid strategy. Choose: {list(STRATEGIES.keys())}"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        tasks_data = request.data.get('tasks', [])
        serializer = TaskInputSerializer(data=tasks_data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = serializer.validated_data
        dependents_count = {t.get('id', str(idx)): 0 for idx, t in enumerate(tasks)}
        for t in tasks:
            for dep in t.get('dependencies', []):
                if dep in dependents_count:
                    dependents_count[dep] += 1

        score_fn = STRATEGIES[strategy]
        scored_tasks = []
        for idx, t in enumerate(tasks):
            tid = t.get('id', str(idx))
            score = score_fn(t, dependents_count[tid])
            scored_tasks.append({
                'id': tid,
                'title': t['title'],
                'score': score,
                'strategy': strategy
            })

        # Return TOP 3 tasks only
        top_tasks = sorted(scored_tasks, key=lambda x: x['score'], reverse=True)[:3]
        return Response({
            'strategy': strategy,
            'top_tasks': top_tasks,
            'message': f"Top 3 tasks prioritized using {strategy.replace('_', ' ').title()} strategy."
        }, status=status.HTTP_200_OK)
