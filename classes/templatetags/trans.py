from django import template
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag(name='trans', takes_context=True)
def trans(context, field, **parameters):
    translations = {
        "es": {
            # Navbar and footer
            "navbar_home": "Inicio",
            "navbar_logout": "Desconectarse",
            "navbar_login": "Iniciar sesión",
            "navbar_register": "Registro",
            "navbar_registered_as": "Registrado como",
            "navbar_cssexample": "Ejemplo css",
            "admin_site": "Administración",
            # Buttons
            "submit_button": "Enviar",
            "search_button": "Buscar",
            # Fields (tabs, forms, tables, lists...)
            "field_name": "Nombre",
            "field_password": "Contraseña",
            "field_username": "Usuario",
            "field_email": "Email",
            "field_confirm_email": "Confirmar contraseña",
            "field_abbr": "Abreviatura",
            "field_stadium": "Estadio",
            "field_manager": "Mánager",
            "field_team": "Equipo",
            "field_league": "Liga",
            "field_contract_length": "Duración del contrato",
            "field_nationality": "Nacionalidad",
            "field_full_name": "Nombre completo",
            "field_info": "Información",
            "field_budget": "Presupuesto",
            "field_elo_points": "Puntuación ELO",            
            "field_calendar": "Calendario",
            "field_youth_team": "Filial",
            "field_salary": "Salario",
            "field_players": "Jugadores",
            "field_career": "Trayectoria",
            "field_results_for": "Resultados de",
            "field_none": "Ninguno",
            "field_abbr_position": "POS",
            "field_abbr_overall": "HAB",
            "field_abbr_age": "ED",
            "field_abbr_defending": "DEF",
            "field_abbr_passing": "PAS",
            "field_abbr_shooting": "TIR",
            "field_abbr_dribbling": "REG",
            "field_abbr_stamina": "RES",
            "field_abbr_strength": "FUE",
            "field_abbr_pace": "VEL",
            "field_abbr_status": "STATUS",
            "field_abbr_team": "EQ",
            "field_position": "Posición",
            "field_team": "Equipo",
            "field_age": "Edad",
            "field_defending": "Defensa",
            "field_passing": "Pase",
            "field_shooting": "Tiro",
            "field_dribbling": "Regate",
            "field_stamina": "Resistencia",
            "field_strength": "Fuerza",
            "field_pace": "Velocidad",
            "field_status": "Situación",
            "field_overall": "Habilidad",
            "field_loaned_by": "Cedido por",
            "field_transferable": "Transferible",
            "field_non_transferable": "Intransferible",
            "field_loan": "Disponible para cesión",
            "field_no_loan": "No disponoible para cesión",
            "field_injured": "Lesionado ({injury_time} día/s)",
            "field_domestic_susp": "Sancionado en competiciones domésticas ({suspension} partido/s)",
            "field_int_susp": "Sancionado en competiciones internacionales de clubes ({suspension} partido/s)",
            "field_nt_susp": "Sancionado con su selección nacional ({suspension} partido/s)",
            "field_loan_length": "Duración de la cesión",
            "field_loan_contribution": "Contribución al sueldo",

            "label_seasons": "temporada/s",
            "label_loaned_by": "Cedido por {loan_team}",
            # Titles
            "title_home": "Inicio",
            "title_league": "Liga",
            "title_players": "Jugadores",
            "title_teams": "Equipos",
            "title_news": "Noticias",
            "title_statistics": "Estadísticas",
            "title_transfers": "Traspasos",
            # Positions
            "GK_position_label": "Portero",
            "CD_position_label": "Central",
            "RD_position_label": "Lateral derecho",
            "LD_position_label": "Lateral izquierdo",
            "RW_position_label": "Carrilero derecho",
            "LW_position_label": "Carrilero izquierdo",
            "DM_position_label": "Mediocentro defensivo",
            "RM_position_label": "Interior derecho",
            "LM_position_label": "Interior izquierdo",
            "CM_position_label": "Centrocampista",
            "OM_position_label": "Mediapunta",
            "CF_position_label": "Delantero centro",
            "LF_position_label": "Extremo izquierdo",
            "RF_position_label": "Extremo derecho",
            "GK_position_abbr": "PT",
            "CD_position_abbr": "DF",
            "RD_position_abbr": "LD",
            "LD_position_abbr": "LI",
            "RW_position_abbr": "CD",
            "LW_position_abbr": "CI",
            "DM_position_abbr": "ME",
            "RM_position_abbr": "MD",
            "LM_position_abbr": "MI",
            "CM_position_abbr": "MC",
            "OM_position_abbr": "MP",
            "CF_position_abbr": "DC",
            "LF_position_abbr": "EI",
            "RF_position_abbr": "ED",
            # Messages
            'message_rotate_to_full_view': "Rota tu dispositivo para visualizar mejor el contenido",
            "message_no_players_found": "No se encontraron jugadores"
        },
        "en": {
            "home": "home",
        }
    }
    

    try:
        trans = translations[context.request.LANGUAGE_CODE][field].format(**parameters)
    except KeyError:
        trans = '[*' + get_language() + "/" + field + '*]'

    return trans