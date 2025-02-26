from django.shortcuts import render
from django.http import HttpResponse

from.models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Isabella Camacho'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies, 'name':'Isabella Camacho'})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')

    #Obtener todos los años de las películas
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') 
    movie_counts_by_year = {} #Crear un diccionario para almacenar las cantidad de películas por año 
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5 #Ancho de las barras
    bar_spacing = 0.5 #Separación entre las barras
    bar_positions = range(len(movie_counts_by_year)) #Posiciones de las barras

    #Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    #Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    #Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    #Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    #Convertir la gráfica a base 64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')


    # Obtener todos los géneros (solo el primero de cada película)
    movies = Movie.objects.exclude(genre="").exclude(genre=None)
    
    genre_counts = {} # Diccionario para contar géneros
    
    for movie in movies:
        first_genre = movie.genre.split(',')[0].strip()  # Tomar el primer género

        if first_genre in genre_counts:
            genre_counts[first_genre] += 1  # Si ya existe, incrementar el conteo
        else:
            genre_counts[first_genre] = 1  # Si no existe, inicializar en 1

    # Configurar la gráfica de barras
    plt.figure(figsize=(10, 5))  # Ajustar tamaño
    plt.bar(genre_counts.keys(), genre_counts.values(), color='skyblue')
    
    # Personalizar la gráfica
    plt.title('Movies per Genre (First Genre Only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas para mejor visibilidad
    plt.tight_layout()  # Ajustar espaciado

    # Guardar la gráfica en un objeto BytesIO
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    #Convertir la gráfica a base 64
    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic2 = base64.b64encode(image_png2)
    graphic2 = graphic2.decode('utf-8')


    #Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic, 'graphic2': graphic2})