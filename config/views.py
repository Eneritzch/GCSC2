import subprocess
import json
import re
from django.shortcuts import render
from django.http import JsonResponse


def git_history_view(request):
    """Vista principal del historial de Git con grafo interactivo."""
    return render(request, 'git_graph.html')


def git_history_api(request):
    """API que devuelve los datos del grafo de Git en formato JSON para Vis.js."""
    try:
        # Obtener todos los commits con sus padres, rama, autor, fecha y mensaje
        cmd = [
            'git', 'log', '--all',
            '--pretty=format:%H|%P|%an|%ar|%s|%D',
            '--date=short'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')

        nodes = []
        edges = []
        seen_edges = set()

        # Colores para las ramas
        branch_colors = {
            'main': '#4f46e5',
            'feature/v2-busqueda-reportes': '#f59e0b',
            'feature/config-editor': '#10b981',
            'feature/v3-modulo-cursos-front': '#ef4444',
        }
        default_color = '#6366f1'

        # Determinar a que rama pertenece cada commit
        branch_cmd = ['git', 'branch', '-a', '--contains']

        for line in lines:
            if not line.strip():
                continue

            parts = line.split('|', 5)
            if len(parts) < 6:
                continue

            commit_hash = parts[0].strip()
            parents = parts[1].strip().split() if parts[1].strip() else []
            author = parts[2].strip()
            date = parts[3].strip()
            message = parts[4].strip()
            refs = parts[5].strip()

            short_hash = commit_hash[:7]

            # Determinar color basado en refs o en el mensaje
            color = default_color
            is_merge = len(parents) > 1
            shape = 'diamond' if is_merge else 'dot'
            size = 18 if is_merge else 12

            # Asignar color por rama
            for branch_name, branch_color in branch_colors.items():
                if branch_name in refs or branch_name in message:
                    color = branch_color
                    break

            # Si es HEAD/main, darle color especial
            if 'HEAD' in refs or 'main' in refs:
                color = '#4f46e5'
                size = 22

            # Etiqueta limpia con nombre de autor (formateado)
            label_parts = []
            if refs:
                # Limpiar refs de origin/ prefixes
                clean_refs = refs.replace('origin/', '').replace('HEAD -> ', '')
                clean_refs = ', '.join(set(r.strip() for r in clean_refs.split(',') if r.strip()))
                if clean_refs:
                    label_parts.append(f"<b>[{clean_refs}]</b>")
            
            label_parts.append(f"<b>{author}</b>  <i style='color:#94a3b8'>({short_hash})</i>")
            
            # Agregar mensaje truncado
            short_msg = message[:40] + ('...' if len(message) > 40 else '')
            label_parts.append(short_msg)
            label = '\n'.join(label_parts)

            node = {
                'id': commit_hash,
                'label': label,
                'title': f"{short_hash} — {author} ({date})\n{message}",
                '_author': author,
                '_date': date,
                '_message': message,
                '_hash': short_hash,
                '_original_color': color, # Guardamos el color original para el filtro
                'color': {
                    'background': color,
                    'border': color,
                    'highlight': {'background': '#ffffff', 'border': color},
                    'hover': {'background': '#ffffff', 'border': color},
                },
                'shape': shape,
                'size': size,
                'font': {
                    'color': '#e2e8f0',
                    'size': 12,
                    'face': 'Inter, system-ui, sans-serif',
                    'multi': 'html',
                },
                'borderWidth': 2,
                'borderWidthSelected': 3,
            }
            nodes.append(node)

            # Crear aristas desde los padres
            for parent in parents:
                edge_id = f"{parent}->{commit_hash}"
                if edge_id not in seen_edges:
                    edge = {
                        'from': parent,
                        'to': commit_hash,
                        'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}},
                        'color': {
                            'color': '#475569',
                            'highlight': color,
                            'hover': color,
                        },
                        'width': 1.5,
                        'smooth': {
                            'type': 'cubicBezier',
                            'forceDirection': 'vertical',
                            'roundness': 0.4,
                        },
                    }
                    edges.append(edge)
                    seen_edges.add(edge_id)

        # Extraer lista única de autores
        authors = sorted(list(set(node['_author'] for node in nodes)))

        return JsonResponse({'nodes': nodes, 'edges': edges, 'authors': authors})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
