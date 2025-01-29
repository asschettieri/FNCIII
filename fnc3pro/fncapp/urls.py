from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Aziende
    path('aziende/', views.lista_aziende, name='lista_aziende'),
    path('aziende/dettagli/<str:id_azienda>/', views.aziende_details, name='azienda_dettagli'),
    path('aziende/crea/', views.azienda_crud, name='crea_azienda'),
    path('aziende/modifica/<str:id_azienda>/', views.azienda_crud, name='modifica_azienda'),
    path('aziende/<str:id_azienda>/dipendenti/', views.azienda_dipendenti, name='azienda_dipendenti'),
    path('aziende/carica_azienda_openapi/', views.carica_azienda_openapi, name='carica_azienda_openapi'),
    path('aziende/update_azienda_openapi/', views.update_azienda_openapi, name='update_azienda_openapi'),
    path('aziende/elimina/<int:id_azienda>/', views.elimina_azienda, name='elimina_azienda'),

    # Dipendenti
    path('dipendenti/', views.lista_dipendenti, name='lista_dipendenti'),
    path('dipendenti/dettagli/<str:dipendente_id>/', views.dipendenti_details, name='dipendenti_details'),
    path('dipendenti/modifica/<str:dipendente_id>/', views.dipendenti_crud, name='dipendenti_crud'),
    path('dipendenti/crea/', views.dipendenti_crud, name='crea_dipendente'),
    path('dipendenti/allegato2bis_wizard_unapagina/', views.wizard_allegato2bis, name='wizard_allegato2bis'),
    path('dipendenti/elimina/<int:dipendente_id>/', views.dipendenti_delete, name='dipendenti_delete'),

    # Piani Formativi
    path('piani/', views.lista_piani, name='lista_pianiformativi'),
    path('piani/dettagli/<str:id_piano>/', views.piano_details, name='piano_details'),
    path('piani/crea/', views.piano_crud, name='crea_pianoformativo'),
    path('piani/modifica/<str:id_piano>/', views.piano_crud, name='modifica_piano'),
    path('piani/elimina/<str:id_piano>/', views.piano_elimina, name='piano_elimina'),

    # Progetti
    path('progetti/', views.lista_progetti, name='lista_progetti'),
    path('progetti/dettagli/<str:id_progetto>/', views.progetto_details, name='progetto_details'),
    
    path('progetti/create/', views.ProgettoCreateView.as_view(), name='progetto_create'),
    path('progetti/<int:pk>/update/', views.ProgettoUpdateView.as_view(), name='progetto_update'),
    
    path('progetti/elimina/<str:id_progetto>/', views.progetto_elimina, name='progetto_elimina'),
    
    # Wizard
    path('associazioni/wizard-propiani/', views.wizard_propiani, name='wizard_propiani'),
    
    # allegato
    path('allegati/genera-allegato/<str:id_azienda>/', views.genera_allegato_excel, name='genera_allegato2bis'),
    path('allegati/pagina-generazione/<str:id_azienda>/', views.pagina_generazione_allegato, name='pagina_generazione_allegato'),
    
    # MODULI
    path('moduli/', views.ModuloListView.as_view(), name='modulo_list'),
    path('modulo/create/', views.ModuloCreateView.as_view(), name='modulo_create'),
    path('modulo/<int:pk>/update/', views.ModuloUpdateView.as_view(), name='modulo_update'),
    path('modulo/<int:pk>/delete/', views.ModuloDeleteView.as_view(), name='modulo_delete'),
    path('modulo/search/', views.search_modulo, name='modulo_search'),
    
    path('fondo/', views.TipoFondoListView.as_view(), name='tipofondo_list'),
    path('fondo/create/', views.TipoFondoCreateView.as_view(), name='tipofondo_create'),
    path('fondo/<int:pk>/update/', views.TipoFondoUpdateView.as_view(), name='tipofondo_update'),
    path('fondo/<int:pk>/delete/', views.TipoFondoDeleteView.as_view(), name='tipofondo_delete'),
    path('fondo/search/', views.search_tipofondo, name='tipofondo_search'),

    path('search_azienda',views.search_azienda, name="search_azienda"),
    path('search_modulo',views.search_modulo, name="search_modulo"),

]
